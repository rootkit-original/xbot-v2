"""
XBot v2 - Use Cases (Application Layer)

Casos de uso que orquestram a lógica de negócio do sistema de trading.
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.entities import (
    TradingBot,
    Market,
    Order,
    Position,
    Pattern,
    MarketAnalysis,
    TradingSignal,
    Candle,
    BotStatus,
    OrderSide,
    OrderType,
    PatternType,
)
from domain.interfaces import (
    IMarketDataRepository,
    ITradingRepository,
    IPortfolioRepository,
    IBotRepository,
    IPatternDetectionService,
    ITechnicalAnalysisService,
    IRiskAnalysisService,
    ISignalGenerationService,
    INotificationService,
    IComplianceService,
    IMarketDataStream,
    IAIService,
)


logger = logging.getLogger(__name__)


class AnalyzeMarketUseCase:
    """Caso de uso para análise completa do mercado"""

    def __init__(
        self,
        market_data_repo: IMarketDataRepository,
        pattern_detector: IPatternDetectionService,
        technical_analysis: ITechnicalAnalysisService,
        ai_service: Optional[IAIService] = None,
    ):
        self.market_data_repo = market_data_repo
        self.pattern_detector = pattern_detector
        self.technical_analysis = technical_analysis
        self.ai_service = ai_service

    async def execute(
        self, symbol: str, timeframes: List[str] = ["1h", "4h", "1d"]
    ) -> MarketAnalysis:
        """Executa análise completa do mercado"""
        logger.info(f"Iniciando análise de mercado para {symbol}")

        # Obtém dados básicos
        current_price = await self.market_data_repo.get_current_price(symbol)
        stats_24h = await self.market_data_repo.get_24h_stats(symbol)

        if not current_price:
            raise ValueError(f"Não foi possível obter preço para {symbol}")

        # Análise em múltiplos timeframes
        all_patterns = []
        all_candles = {}

        for timeframe in timeframes:
            candles = await self.market_data_repo.get_candles(symbol, timeframe, limit=200)
            if candles:
                all_candles[timeframe] = candles
                patterns = await self.pattern_detector.detect_patterns(candles)
                all_patterns.extend(patterns)

        # Análise técnica principal (timeframe maior)
        main_candles = all_candles.get("4h", all_candles.get("1h", []))
        if not main_candles:
            raise ValueError(f"Não foi possível obter candlesticks para {symbol}")

        # Indicadores técnicos
        rsi_values = await self.technical_analysis.calculate_rsi(main_candles)
        rsi = rsi_values[-1] if rsi_values else None

        macd_data = await self.technical_analysis.calculate_macd(main_candles)
        macd_signal = self._interpret_macd(macd_data)

        moving_averages = await self.technical_analysis.calculate_moving_averages(
            main_candles, [20, 50, 200]
        )
        ma_dict = {
            f"MA{period}": values[-1] for period, values in moving_averages.items() if values
        }

        bollinger_data = await self.technical_analysis.calculate_bollinger_bands(main_candles)
        bb_dict = {k: v[-1] for k, v in bollinger_data.items() if v}

        # Suporte e resistência
        support_resistance = await self.technical_analysis.find_support_resistance(main_candles)
        support_levels = support_resistance.get("support", [])
        resistance_levels = support_resistance.get("resistance", [])

        # Sentiment analysis com AI (se disponível)
        market_sentiment = "NEUTRAL"
        sentiment_score = Decimal("0.5")

        if self.ai_service:
            try:
                sentiment_result = await self.ai_service.analyze_market_sentiment(symbol)
                market_sentiment, sentiment_score = sentiment_result
            except Exception as e:
                logger.warning(f"Erro na análise de sentiment: {e}")

        # Calcula volatilidade
        volatility = self._calculate_volatility(main_candles)

        # Liquidity score baseado no volume
        liquidity_score = self._calculate_liquidity_score(
            main_candles, stats_24h.get("volume", Decimal("0"))
        )

        analysis = MarketAnalysis(
            symbol=symbol,
            timestamp=datetime.now(),
            current_price=current_price,
            price_change_24h=stats_24h.get("priceChangePercent", Decimal("0")),
            volume_24h=stats_24h.get("volume", Decimal("0")),
            detected_patterns=all_patterns,
            support_levels=support_levels,
            resistance_levels=resistance_levels,
            rsi=rsi,
            macd_signal=macd_signal,
            moving_averages=ma_dict,
            bollinger_bands=bb_dict,
            market_sentiment=market_sentiment,
            sentiment_score=sentiment_score,
            volatility=volatility,
            liquidity_score=liquidity_score,
        )

        logger.info(f"Análise concluída para {symbol}: {len(all_patterns)} padrões detectados")
        return analysis

    def _interpret_macd(self, macd_data: Dict[str, List[Decimal]]) -> str:
        """Interpreta sinal do MACD"""
        if not macd_data or "macd" not in macd_data or "signal" not in macd_data:
            return "NEUTRAL"

        macd_line = macd_data["macd"]
        signal_line = macd_data["signal"]

        if len(macd_line) < 2 or len(signal_line) < 2:
            return "NEUTRAL"

        # Cross over/under
        if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
            return "BUY"
        elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
            return "SELL"

        return "NEUTRAL"

    def _calculate_volatility(self, candles: List[Candle]) -> Decimal:
        """Calcula volatilidade baseada no ATR"""
        if len(candles) < 14:
            return Decimal("0")

        true_ranges = []
        for i in range(1, len(candles)):
            high = candles[i].high_price
            low = candles[i].low_price
            prev_close = candles[i - 1].close_price

            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            true_ranges.append(tr)

        # ATR de 14 períodos
        atr = sum(true_ranges[-14:]) / 14
        current_price = candles[-1].close_price

        return (atr / current_price) * 100 if current_price > 0 else Decimal("0")

    def _calculate_liquidity_score(self, candles: List[Candle], volume_24h: Decimal) -> Decimal:
        """Calcula score de liquidez"""
        if not candles or volume_24h == 0:
            return Decimal("0")

        # Volume médio dos últimos candles
        recent_volumes = [c.volume for c in candles[-24:]]  # últimas 24 horas se for 1h
        avg_volume = sum(recent_volumes) / len(recent_volumes) if recent_volumes else Decimal("0")

        # Spread estimado baseado na volatilidade
        volatility = self._calculate_volatility(candles)

        # Score simples: volume alto e volatilidade baixa = liquidez alta
        if volatility > 0:
            liquidity = min(Decimal("1"), (avg_volume / volume_24h) / (volatility / 100))
        else:
            liquidity = Decimal("0.5")

        return liquidity


class DetectPatternsUseCase:
    """Caso de uso para detecção de padrões avançados"""

    def __init__(
        self,
        market_data_repo: IMarketDataRepository,
        pattern_detector: IPatternDetectionService,
        ai_service: Optional[IAIService] = None,
    ):
        self.market_data_repo = market_data_repo
        self.pattern_detector = pattern_detector
        self.ai_service = ai_service

    async def execute(
        self,
        symbol: str,
        pattern_types: Optional[List[PatternType]] = None,
        timeframes: List[str] = ["1h", "4h"],
    ) -> List[Pattern]:
        """Detecta padrões em múltiplos timeframes"""
        logger.info(f"Detectando padrões para {symbol}")

        all_patterns = []

        for timeframe in timeframes:
            candles = await self.market_data_repo.get_candles(symbol, timeframe, limit=100)
            if not candles:
                continue

            patterns = await self.pattern_detector.detect_patterns(candles, pattern_types)

            # Ajusta informações dos padrões
            for pattern in patterns:
                pattern.timeframe = timeframe

                # Análise de força do padrão
                strength = await self.pattern_detector.analyze_pattern_strength(pattern)
                pattern.confidence = strength

                # Targets do padrão
                targets = await self.pattern_detector.get_pattern_targets(pattern)
                pattern.take_profit, pattern.stop_loss_price = targets

            all_patterns.extend(patterns)

        # Filtra padrões por confiança
        high_confidence_patterns = [p for p in all_patterns if p.confidence >= Decimal("0.7")]

        logger.info(f"Detectados {len(high_confidence_patterns)} padrões de alta confiança")
        return high_confidence_patterns


class GenerateSignalUseCase:
    """Caso de uso para geração de sinais de trading"""

    def __init__(
        self,
        signal_generator: ISignalGenerationService,
        compliance_service: IComplianceService,
        risk_analyzer: IRiskAnalysisService,
    ):
        self.signal_generator = signal_generator
        self.compliance_service = compliance_service
        self.risk_analyzer = risk_analyzer

    async def execute(
        self, market_analysis: MarketAnalysis, bot: TradingBot
    ) -> Optional[TradingSignal]:
        """Gera sinal de trading baseado na análise"""
        logger.info(f"Gerando sinal para {market_analysis.symbol}")

        # Gera sinal baseado na estratégia
        signal = await self.signal_generator.generate_signal(market_analysis, bot.strategy)

        if not signal:
            return None

        # Valida sinal
        is_valid = await self.signal_generator.validate_signal(signal)
        if not is_valid:
            logger.warning("Sinal inválido gerado")
            return None

        # Análise de risco
        risk_score = await self.risk_analyzer.assess_market_risk(market_analysis)
        signal.risk_score = risk_score

        # Calcula tamanho da posição
        if signal.entry_price and signal.stop_loss:
            position_size = await self.risk_analyzer.calculate_position_size(
                bot.available_capital,
                bot.strategy.risk_profile,
                signal.entry_price,
                signal.stop_loss,
            )
            signal.position_size_suggestion = position_size

        # Compliance check
        dummy_order = Order(
            symbol=signal.symbol,
            side=OrderSide.BUY if signal.signal_type == "BUY" else OrderSide.SELL,
            order_type=OrderType.LIMIT,
            quantity=signal.position_size_suggestion or Decimal("0"),
            price=signal.entry_price,
        )

        compliance_ok, compliance_msg = await self.compliance_service.validate_trade(
            dummy_order, bot.active_positions
        )

        if not compliance_ok:
            logger.warning(f"Sinal rejeitado por compliance: {compliance_msg}")
            return None

        logger.info(f"Sinal gerado: {signal.signal_type} {signal.symbol} @ {signal.entry_price}")
        return signal


class ExecuteTradeUseCase:
    """Caso de uso para execução de trades"""

    def __init__(
        self,
        trading_repo: ITradingRepository,
        portfolio_repo: IPortfolioRepository,
        compliance_service: IComplianceService,
        notification_service: INotificationService,
    ):
        self.trading_repo = trading_repo
        self.portfolio_repo = portfolio_repo
        self.compliance_service = compliance_service
        self.notification_service = notification_service

    async def execute(
        self, signal: TradingSignal, bot: TradingBot
    ) -> Tuple[bool, Optional[Order], str]:
        """Executa trade baseado no sinal"""
        logger.info(f"Executando trade: {signal.signal_type} {signal.symbol}")

        if not signal.is_actionable:
            return False, None, "Sinal não acionável"

        # Verifica limites de posição
        position_limits_ok, limit_msg = await self.compliance_service.check_position_limits(bot)
        if not position_limits_ok:
            return False, None, f"Limite de posição excedido: {limit_msg}"

        # Verifica limite de perda diária
        daily_loss_ok, loss_msg = await self.compliance_service.check_daily_loss_limit(bot)
        if not daily_loss_ok:
            return False, None, f"Limite de perda diária excedido: {loss_msg}"

        # Cria ordem
        order = Order(
            symbol=signal.symbol,
            side=OrderSide.BUY if signal.signal_type == "BUY" else OrderSide.SELL,
            order_type=OrderType.LIMIT,
            quantity=signal.position_size_suggestion or Decimal("0.001"),
            price=signal.entry_price,
            client_order_id=f"{bot.id}_{signal.symbol}_{int(datetime.now().timestamp())}",
        )

        # Validação final
        trade_valid, trade_msg = await self.compliance_service.validate_trade(
            order, bot.active_positions
        )

        if not trade_valid:
            return False, None, f"Trade inválido: {trade_msg}"

        try:
            # Executa ordem
            executed_order = await self.trading_repo.place_order(order)

            # Atualiza estatísticas do bot
            bot.total_trades += 1
            bot.last_trade_at = datetime.now()

            # Log de auditoria
            await self.compliance_service.generate_audit_log(
                bot,
                "TRADE_EXECUTED",
                {
                    "order_id": executed_order.order_id,
                    "signal_confidence": str(signal.confidence),
                    "risk_score": str(signal.risk_score),
                },
            )

            # Notificação
            await self.notification_service.send_trade_notification(
                bot.id, executed_order, f"Trade executado: {signal.signal_type} {signal.symbol}"
            )

            logger.info(f"Trade executado com sucesso: {executed_order.order_id}")
            return True, executed_order, "Trade executado com sucesso"

        except Exception as e:
            error_msg = f"Erro ao executar trade: {str(e)}"
            logger.error(error_msg)

            await self.notification_service.send_alert(
                "Erro de Execução", f"Bot {bot.name}: {error_msg}", "high"
            )

            return False, None, error_msg


class MonitorPositionsUseCase:
    """Caso de uso para monitoramento de posições"""

    def __init__(
        self,
        portfolio_repo: IPortfolioRepository,
        trading_repo: ITradingRepository,
        market_data_repo: IMarketDataRepository,
        risk_analyzer: IRiskAnalysisService,
        notification_service: INotificationService,
    ):
        self.portfolio_repo = portfolio_repo
        self.trading_repo = trading_repo
        self.market_data_repo = market_data_repo
        self.risk_analyzer = risk_analyzer
        self.notification_service = notification_service

    async def execute(self, bot: TradingBot) -> List[Tuple[Position, bool, str]]:
        """Monitora posições e determina ações necessárias"""
        logger.info(f"Monitorando posições do bot {bot.name}")

        positions = await self.portfolio_repo.get_positions()
        actions = []

        for position in positions:
            # Atualiza preço atual
            current_price = await self.market_data_repo.get_current_price(position.symbol)
            if current_price:
                position.current_price = current_price

                # Recalcula P&L
                if position.side == OrderSide.BUY:
                    position.unrealized_pnl = (
                        current_price - position.entry_price
                    ) * position.quantity
                else:
                    position.unrealized_pnl = (
                        position.entry_price - current_price
                    ) * position.quantity

            # Análise de mercado para decisão
            candles = await self.market_data_repo.get_candles(position.symbol, "1h", limit=50)
            if candles:
                analysis = MarketAnalysis(
                    symbol=position.symbol,
                    timestamp=datetime.now(),
                    current_price=current_price or position.current_price,
                    price_change_24h=Decimal("0"),
                    volume_24h=Decimal("0"),
                    detected_patterns=[],
                    support_levels=[],
                    resistance_levels=[],
                )

                # Deve fechar posição?
                should_close, reason = await self.risk_analyzer.should_close_position(
                    position, analysis
                )

                if should_close:
                    actions.append((position, True, reason))

                    # Notificação de fechamento
                    await self.notification_service.send_alert(
                        "Posição a Fechar",
                        f"Bot {bot.name}: {reason} - {position.symbol}",
                        "normal",
                    )
                else:
                    actions.append((position, False, "Manter posição"))

        return actions


class RunTradingBotUseCase:
    """Caso de uso principal para executar bot de trading"""

    def __init__(
        self,
        analyze_market: AnalyzeMarketUseCase,
        detect_patterns: DetectPatternsUseCase,
        generate_signal: GenerateSignalUseCase,
        execute_trade: ExecuteTradeUseCase,
        monitor_positions: MonitorPositionsUseCase,
        bot_repo: IBotRepository,
        notification_service: INotificationService,
    ):
        self.analyze_market = analyze_market
        self.detect_patterns = detect_patterns
        self.generate_signal = generate_signal
        self.execute_trade = execute_trade
        self.monitor_positions = monitor_positions
        self.bot_repo = bot_repo
        self.notification_service = notification_service

    async def execute(self, bot_id: str) -> Dict[str, any]:
        """Executa ciclo completo do bot de trading"""
        logger.info(f"Iniciando ciclo do bot {bot_id}")

        # Carrega bot
        bot = await self.bot_repo.load_bot(bot_id)
        if not bot:
            raise ValueError(f"Bot {bot_id} não encontrado")

        if not bot.is_active:
            return {"status": "inactive", "message": "Bot não está ativo"}

        try:
            # Atualiza status
            bot.status = BotStatus.ANALYZING
            await self.bot_repo.save_bot(bot)

            results = {
                "bot_id": bot_id,
                "cycle_start": datetime.now(),
                "actions_taken": [],
                "analysis_results": {},
                "signals_generated": [],
                "trades_executed": [],
                "positions_monitored": [],
            }

            # 1. Monitora posições existentes
            position_actions = await self.monitor_positions.execute(bot)
            results["positions_monitored"] = len(position_actions)

            # Executa fechamentos necessários
            for position, should_close, reason in position_actions:
                if should_close:
                    # Cria ordem de fechamento
                    close_order = Order(
                        symbol=position.symbol,
                        side=OrderSide.SELL if position.side == OrderSide.BUY else OrderSide.BUY,
                        order_type=OrderType.MARKET,
                        quantity=position.quantity,
                    )

                    # Aqui executaria o fechamento
                    results["actions_taken"].append(f"Fechando posição {position.symbol}: {reason}")

            # 2. Análise de mercado para símbolos da estratégia
            symbols = getattr(bot.strategy, "symbols", ["BTCUSDT"])  # Default

            for symbol in symbols:
                try:
                    # Análise de mercado
                    bot.status = BotStatus.ANALYZING
                    analysis = await self.analyze_market.execute(symbol)
                    results["analysis_results"][symbol] = {
                        "patterns_found": len(analysis.detected_patterns),
                        "sentiment": analysis.market_sentiment,
                        "volatility": str(analysis.volatility),
                    }

                    # Geração de sinal
                    signal = await self.generate_signal.execute(analysis, bot)

                    if signal and signal.is_actionable:
                        results["signals_generated"].append(
                            {
                                "symbol": signal.symbol,
                                "type": signal.signal_type,
                                "confidence": str(signal.confidence),
                            }
                        )

                        # Execução de trade
                        if bot.position_count < bot.strategy.risk_profile.max_concurrent_positions:
                            bot.status = BotStatus.TRADING
                            success, order, message = await self.execute_trade.execute(signal, bot)

                            if success and order:
                                results["trades_executed"].append(
                                    {
                                        "order_id": order.order_id,
                                        "symbol": order.symbol,
                                        "side": order.side.value,
                                        "quantity": str(order.quantity),
                                    }
                                )

                                # Atualiza estatísticas
                                if order.is_filled:
                                    bot.winning_trades += 1  # Será ajustado quando a posição fechar
                            else:
                                results["actions_taken"].append(f"Trade rejeitado: {message}")

                except Exception as e:
                    logger.error(f"Erro processando {symbol}: {e}")
                    results["actions_taken"].append(f"Erro em {symbol}: {str(e)}")

            # 3. Finalização
            bot.status = BotStatus.IDLE
            bot.last_analysis_at = datetime.now()
            await self.bot_repo.save_bot(bot)

            results["cycle_end"] = datetime.now()
            results["duration"] = (results["cycle_end"] - results["cycle_start"]).total_seconds()

            # Relatório de performance (diário)
            if self._should_send_performance_report(bot):
                await self.notification_service.send_performance_report(bot)

            logger.info(f"Ciclo do bot {bot_id} concluído em {results['duration']:.2f}s")
            return results

        except Exception as e:
            bot.status = BotStatus.ERROR
            await self.bot_repo.save_bot(bot)

            await self.notification_service.send_risk_alert(bot, f"Erro crítico no bot: {str(e)}")

            raise

    def _should_send_performance_report(self, bot: TradingBot) -> bool:
        """Determina se deve enviar relatório de performance"""
        if not bot.last_trade_at:
            return False

        # Envia relatório uma vez por dia
        now = datetime.now()
        last_report = getattr(bot, "last_performance_report", datetime.min)

        return (now - last_report).days >= 1
