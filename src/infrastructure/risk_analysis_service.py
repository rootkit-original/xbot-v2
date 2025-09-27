"""
XBot v2 - Risk Analysis Service (Infrastructure Layer)

Serviço avançado para análise de riscos, cálculo de posições e gestão de capital.
"""

import math
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
import logging

from ..domain.entities import (
    Position,
    MarketAnalysis,
    RiskProfile,
    RiskLevel,
    OrderSide,
    TradingBot,
    Candle,
)
from ..domain.interfaces import IRiskAnalysisService


logger = logging.getLogger(__name__)


class RiskAnalysisService(IRiskAnalysisService):
    """Serviço para análise avançada de riscos"""

    def __init__(self):
        self.risk_metrics = {}
        self.volatility_cache = {}

    async def calculate_position_size(
        self, capital: Decimal, risk_profile: RiskProfile, entry_price: Decimal, stop_loss: Decimal
    ) -> Decimal:
        """Calcula tamanho ótimo da posição"""
        logger.info("Calculando tamanho da posição")

        if entry_price <= 0 or stop_loss <= 0:
            logger.warning("Preços inválidos para cálculo de posição")
            return Decimal("0")

        # Risco por trade (% do capital)
        risk_per_trade = risk_profile.max_position_size / Decimal("100")  # Convert percentage
        max_loss_amount = capital * risk_per_trade

        # Risco por unidade
        price_risk = abs(entry_price - stop_loss)

        if price_risk == 0:
            logger.warning("Risco zero detectado")
            return Decimal("0")

        # Position sizing methods

        if risk_profile.use_kelly_criterion:
            # Kelly Criterion (requer histórico de performance)
            position_size = await self._kelly_position_size(
                max_loss_amount, price_risk, risk_profile
            )
        else:
            # Fixed fractional position sizing
            position_size = max_loss_amount / price_risk

        # Aplica limites máximos
        max_position_value = capital * (risk_profile.max_position_size / Decimal("100"))
        max_quantity = max_position_value / entry_price

        final_size = min(position_size, max_quantity)

        # Tamanho mínimo
        if final_size < Decimal("0.001"):
            logger.warning("Tamanho de posição muito pequeno")
            return Decimal("0")

        logger.info(f"Tamanho calculado: {final_size}")
        return final_size

    async def assess_market_risk(self, analysis: MarketAnalysis) -> Decimal:
        """Avalia risco do mercado (0.0 = baixo, 1.0 = alto)"""
        logger.info(f"Avaliando risco de mercado para {analysis.symbol}")

        risk_factors = []

        # 1. Volatilidade
        volatility_risk = min(analysis.volatility / Decimal("10"), Decimal("1.0"))  # Cap at 10%
        risk_factors.append(("volatility", volatility_risk, Decimal("0.25")))

        # 2. Liquidez
        liquidity_risk = Decimal("1.0") - analysis.liquidity_score
        risk_factors.append(("liquidity", liquidity_risk, Decimal("0.20")))

        # 3. Padrões conflitantes
        pattern_risk = await self._assess_pattern_risk(analysis.detected_patterns)
        risk_factors.append(("patterns", pattern_risk, Decimal("0.15")))

        # 4. Sentiment extremo
        sentiment_risk = await self._assess_sentiment_risk(analysis.sentiment_score)
        risk_factors.append(("sentiment", sentiment_risk, Decimal("0.15")))

        # 5. Indicadores técnicos
        technical_risk = await self._assess_technical_risk(analysis)
        risk_factors.append(("technical", technical_risk, Decimal("0.15")))

        # 6. Volume
        volume_risk = await self._assess_volume_risk(analysis.volume_24h)
        risk_factors.append(("volume", volume_risk, Decimal("0.10")))

        # Weighted average
        total_risk = sum(risk * weight for _, risk, weight in risk_factors)

        # Normaliza entre 0 e 1
        normalized_risk = max(Decimal("0"), min(total_risk, Decimal("1.0")))

        logger.info(f"Risco de mercado calculado: {normalized_risk}")
        return normalized_risk

    async def calculate_var(
        self, positions: List[Position], confidence: Decimal = Decimal("0.95")
    ) -> Decimal:
        """Calcula Value at Risk do portfólio"""
        if not positions:
            return Decimal("0")

        # Simplified VaR calculation
        # In practice, you'd want historical price data and correlation matrices

        total_value = sum(pos.market_value for pos in positions)
        if total_value == 0:
            return Decimal("0")

        # Assume 2% daily volatility (this should be calculated from historical data)
        daily_volatility = Decimal("0.02")

        # Standard normal distribution z-score for confidence level
        z_scores = {
            Decimal("0.90"): Decimal("1.28"),
            Decimal("0.95"): Decimal("1.65"),
            Decimal("0.99"): Decimal("2.33"),
        }

        z_score = z_scores.get(confidence, Decimal("1.65"))

        # VaR = Portfolio Value × Volatility × Z-Score
        var = total_value * daily_volatility * z_score

        logger.info(f"VaR calculado: {var} (confiança: {confidence})")
        return var

    async def should_close_position(
        self, position: Position, current_analysis: MarketAnalysis
    ) -> Tuple[bool, str]:
        """Determina se deve fechar posição"""

        # 1. Stop Loss atingido
        if position.stop_loss:
            if position.side == OrderSide.BUY and position.current_price <= position.stop_loss:
                return True, "Stop Loss atingido"
            elif position.side == OrderSide.SELL and position.current_price >= position.stop_loss:
                return True, "Stop Loss atingido"

        # 2. Take Profit atingido
        if position.take_profit:
            if position.side == OrderSide.BUY and position.current_price >= position.take_profit:
                return True, "Take Profit atingido"
            elif position.side == OrderSide.SELL and position.current_price <= position.take_profit:
                return True, "Take Profit atingido"

        # 3. Análise de risco elevado
        market_risk = await self.assess_market_risk(current_analysis)
        if market_risk > Decimal("0.8"):
            return True, "Risco de mercado elevado"

        # 4. Reversão de tendência
        if current_analysis.detected_patterns:
            for pattern in current_analysis.detected_patterns:
                if pattern.is_high_confidence:
                    # Se posição long e padrão bearish
                    if position.side == OrderSide.BUY and pattern.is_bearish:
                        return True, f"Padrão bearish detectado: {pattern.pattern_type.value}"
                    # Se posição short e padrão bullish
                    elif position.side == OrderSide.SELL and pattern.is_bullish:
                        return True, f"Padrão bullish detectado: {pattern.pattern_type.value}"

        # 5. Tempo limite (posições muito antigas)
        if position.opened_at:
            days_held = (datetime.now() - position.opened_at).days
            if days_held > 30:  # Posições antigas
                if position.pnl_percentage < Decimal("5"):  # Sem performance
                    return True, "Posição antiga sem performance"

        # 6. Drawdown excessivo
        if position.pnl_percentage < Decimal("-10"):  # 10% de perda
            return True, "Drawdown excessivo"

        return False, "Manter posição"

    # ========================================
    # Private Helper Methods
    # ========================================

    async def _kelly_position_size(
        self, max_loss: Decimal, price_risk: Decimal, risk_profile: RiskProfile
    ) -> Decimal:
        """Calcula tamanho usando Kelly Criterion"""
        # Kelly % = (bp - q) / b
        # Onde: b = odds recebidas, p = probabilidade de ganhar, q = probabilidade de perder

        # Valores default (devem vir do backtest da estratégia)
        win_probability = Decimal("0.6")  # 60% win rate
        avg_win = Decimal("3.0")  # Average win is 3x the risk
        avg_loss = Decimal("1.0")  # Average loss is 1x the risk

        if avg_loss == 0:
            return max_loss / price_risk

        # Kelly fraction
        kelly_fraction = (
            win_probability * avg_win - (Decimal("1") - win_probability) * avg_loss
        ) / avg_win

        # Cap Kelly at 25% to avoid over-leveraging
        kelly_fraction = min(kelly_fraction, Decimal("0.25"))
        kelly_fraction = max(kelly_fraction, Decimal("0.01"))  # Minimum 1%

        return (max_loss * kelly_fraction) / price_risk

    async def _assess_pattern_risk(self, patterns: List) -> Decimal:
        """Avalia risco baseado em padrões conflitantes"""
        if not patterns:
            return Decimal("0.3")  # Moderate risk when no patterns

        bullish_count = sum(1 for p in patterns if p.is_bullish and p.is_high_confidence)
        bearish_count = sum(1 for p in patterns if p.is_bearish and p.is_high_confidence)

        if bullish_count > 0 and bearish_count > 0:
            return Decimal("0.8")  # High risk: conflicting signals
        elif bullish_count > bearish_count or bearish_count > bullish_count:
            return Decimal("0.2")  # Low risk: clear direction
        else:
            return Decimal("0.5")  # Medium risk: unclear signals

    async def _assess_sentiment_risk(self, sentiment_score: Decimal) -> Decimal:
        """Avalia risco baseado em sentiment extremo"""
        # Sentiment extremo (muito bullish ou muito bearish) pode indicar reversão
        center = Decimal("0.5")
        distance_from_center = abs(sentiment_score - center)

        # Risk increases as sentiment becomes more extreme
        return distance_from_center * Decimal("2")  # Scale to 0-1

    async def _assess_technical_risk(self, analysis: MarketAnalysis) -> Decimal:
        """Avalia risco baseado em indicadores técnicos"""
        risk_factors = []

        # RSI extremo
        if analysis.rsi:
            if analysis.rsi > Decimal("80") or analysis.rsi < Decimal("20"):
                risk_factors.append(Decimal("0.7"))  # High risk in extreme zones
            else:
                risk_factors.append(Decimal("0.3"))

        # MACD divergence (simplificado)
        if analysis.macd_signal:
            if analysis.macd_signal in ["BUY", "SELL"]:
                risk_factors.append(Decimal("0.2"))  # Lower risk with clear signals
            else:
                risk_factors.append(Decimal("0.5"))  # Higher risk with neutral signals

        # Bollinger Bands
        if (
            analysis.bollinger_bands
            and "upper" in analysis.bollinger_bands
            and "lower" in analysis.bollinger_bands
        ):
            bb_upper = analysis.bollinger_bands["upper"]
            bb_lower = analysis.bollinger_bands["lower"]
            current_price = analysis.current_price

            # Risk increases near bands
            if current_price > bb_upper or current_price < bb_lower:
                risk_factors.append(Decimal("0.6"))
            else:
                risk_factors.append(Decimal("0.3"))

        if not risk_factors:
            return Decimal("0.5")

        return sum(risk_factors) / len(risk_factors)

    async def _assess_volume_risk(self, volume_24h: Decimal) -> Decimal:
        """Avalia risco baseado no volume"""
        # Low volume = higher risk (harder to exit)
        # This is a simplified approach - should compare with historical averages

        if volume_24h < Decimal("1000000"):  # Low volume threshold
            return Decimal("0.7")
        elif volume_24h < Decimal("10000000"):  # Medium volume
            return Decimal("0.4")
        else:  # High volume
            return Decimal("0.2")

    async def calculate_risk_adjusted_return(
        self, returns: List[Decimal], risk_free_rate: Decimal = Decimal("0.02")
    ) -> Dict[str, Decimal]:
        """Calcula métricas de retorno ajustadas ao risco"""
        if not returns:
            return {}

        # Convert to float for numpy operations
        returns_float = [float(r) for r in returns]

        # Basic statistics
        avg_return = sum(returns) / len(returns)

        # Volatility (standard deviation)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        volatility = Decimal(str(math.sqrt(float(variance))))

        # Sharpe Ratio
        if volatility > 0:
            sharpe_ratio = (avg_return - risk_free_rate) / volatility
        else:
            sharpe_ratio = Decimal("0")

        # Maximum Drawdown
        peak = returns[0]
        max_dd = Decimal("0")

        for ret in returns:
            if ret > peak:
                peak = ret
            drawdown = (peak - ret) / peak if peak > 0 else Decimal("0")
            max_dd = max(max_dd, drawdown)

        # Calmar Ratio (Annual Return / Max Drawdown)
        calmar_ratio = avg_return / max_dd if max_dd > 0 else Decimal("0")

        return {
            "avg_return": avg_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_dd,
            "calmar_ratio": calmar_ratio,
        }

    async def calculate_correlation_matrix(
        self, positions: List[Position]
    ) -> Dict[str, Dict[str, Decimal]]:
        """Calcula matriz de correlação entre posições"""
        # Simplified correlation calculation
        # In practice, you'd need historical price data

        symbols = [pos.symbol for pos in positions]
        correlation_matrix = {}

        for symbol1 in symbols:
            correlation_matrix[symbol1] = {}
            for symbol2 in symbols:
                if symbol1 == symbol2:
                    correlation_matrix[symbol1][symbol2] = Decimal("1.0")
                else:
                    # Simplified: assume some correlation based on asset types
                    # This should be calculated from historical price data
                    if self._are_correlated_assets(symbol1, symbol2):
                        correlation_matrix[symbol1][symbol2] = Decimal("0.7")
                    else:
                        correlation_matrix[symbol1][symbol2] = Decimal("0.3")

        return correlation_matrix

    def _are_correlated_assets(self, symbol1: str, symbol2: str) -> bool:
        """Determina se dois assets são correlacionados"""
        # Simplified logic - should be based on actual correlation analysis
        crypto_majors = ["BTC", "ETH"]

        base1 = symbol1.replace("USDT", "").replace("BTC", "").replace("ETH", "")
        base2 = symbol2.replace("USDT", "").replace("BTC", "").replace("ETH", "")

        # Major cryptos are highly correlated
        if base1 in crypto_majors and base2 in crypto_majors:
            return True

        # Altcoins are moderately correlated with majors
        return False

    async def calculate_portfolio_beta(
        self, positions: List[Position], market_returns: List[Decimal] = None
    ) -> Decimal:
        """Calcula beta do portfólio em relação ao mercado"""
        # Simplified beta calculation
        # In practice, you'd need historical returns data

        if not positions or not market_returns:
            return Decimal("1.0")  # Default beta

        # Weighted average beta based on position sizes
        total_value = sum(pos.market_value for pos in positions)
        if total_value == 0:
            return Decimal("1.0")

        weighted_beta = Decimal("0")
        for position in positions:
            weight = position.market_value / total_value
            asset_beta = self._estimate_asset_beta(position.symbol)
            weighted_beta += weight * asset_beta

        return weighted_beta

    def _estimate_asset_beta(self, symbol: str) -> Decimal:
        """Estima beta de um asset individual"""
        # Simplified beta estimation
        # Should be calculated from historical data vs market index

        if "BTC" in symbol:
            return Decimal("1.2")  # BTC typically has higher volatility
        elif "ETH" in symbol:
            return Decimal("1.1")
        elif "USDT" in symbol or "BUSD" in symbol:
            return Decimal("0.1")  # Stablecoins have very low beta
        else:
            return Decimal("1.5")  # Altcoins typically have higher beta
