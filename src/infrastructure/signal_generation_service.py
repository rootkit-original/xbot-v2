"""
XBot v2 - Signal Generation Service (Infrastructure Layer)

Serviço para geração de sinais de trading baseados em análise técnica e padrões.
"""

from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
import logging

from ..domain.entities import MarketAnalysis, TradingSignal, TradingStrategy, PatternType
from ..domain.interfaces import (
    ISignalGenerationService,
    IPatternDetectionService,
    ITechnicalAnalysisService,
)


logger = logging.getLogger(__name__)


class SignalGenerationService(ISignalGenerationService):
    """Serviço para geração de sinais de trading"""

    def __init__(
        self,
        pattern_detector: IPatternDetectionService,
        technical_analysis: ITechnicalAnalysisService,
    ):
        self.pattern_detector = pattern_detector
        self.technical_analysis = technical_analysis

    async def generate_signal(
        self, market_analysis: MarketAnalysis, strategy: TradingStrategy
    ) -> Optional[TradingSignal]:
        """Gera sinal de trading baseado na análise"""
        logger.info(f"Gerando sinal para {market_analysis.symbol}")

        # Filter patterns by strategy preferences
        relevant_patterns = [
            p
            for p in market_analysis.detected_patterns
            if p.pattern_type in strategy.preferred_patterns
            and p.confidence >= strategy.min_pattern_confidence
        ]

        if not relevant_patterns:
            logger.debug("Nenhum padrão relevante encontrado")
            return None

        # Determine signal direction and strength
        bullish_signals = [p for p in relevant_patterns if p.is_bullish]
        bearish_signals = [p for p in relevant_patterns if p.is_bearish]

        signal_type = "HOLD"
        confidence = Decimal("0.5")

        if len(bullish_signals) > len(bearish_signals):
            signal_type = "BUY"
            confidence = sum(p.confidence for p in bullish_signals) / len(bullish_signals)
        elif len(bearish_signals) > len(bullish_signals):
            signal_type = "SELL"
            confidence = sum(p.confidence for p in bearish_signals) / len(bearish_signals)

        # Technical indicators confirmation
        technical_score = await self._calculate_technical_score(market_analysis)

        # Adjust confidence based on technical indicators
        final_confidence = (confidence + technical_score) / Decimal("2")

        # Generate entry/exit points
        entry_price = market_analysis.current_price
        stop_loss, take_profit = await self._calculate_targets(
            entry_price, signal_type, market_analysis, strategy
        )

        signal = TradingSignal(
            symbol=market_analysis.symbol,
            signal_type=signal_type,
            confidence=final_confidence,
            generated_at=datetime.now(),
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            source_patterns=relevant_patterns,
            source_analysis=market_analysis,
        )

        logger.info(
            f"Sinal gerado: {signal_type} {market_analysis.symbol} - Confiança: {final_confidence:.2%}"
        )
        return signal

    async def validate_signal(self, signal: TradingSignal) -> bool:
        """Valida sinal antes da execução"""
        # Basic validation checks
        if not signal.is_actionable:
            return False

        if not signal.entry_price or signal.entry_price <= 0:
            return False

        # Risk/reward ratio check
        if signal.risk_reward_ratio:
            if signal.risk_reward_ratio < Decimal("1.5"):  # Minimum 1:1.5
                logger.warning(f"Risk/reward ratio baixo: {signal.risk_reward_ratio}")
                return False

        return True

    async def combine_signals(self, signals: List[TradingSignal]) -> Optional[TradingSignal]:
        """Combina múltiplos sinais em um consenso"""
        if not signals:
            return None

        if len(signals) == 1:
            return signals[0]

        # Simple consensus mechanism
        buy_signals = [s for s in signals if s.signal_type == "BUY"]
        sell_signals = [s for s in signals if s.signal_type == "SELL"]

        if len(buy_signals) > len(sell_signals):
            # Combine buy signals
            avg_confidence = sum(s.confidence for s in buy_signals) / len(buy_signals)
            combined_patterns = []
            for s in buy_signals:
                combined_patterns.extend(s.source_patterns)

            return TradingSignal(
                symbol=signals[0].symbol,
                signal_type="BUY",
                confidence=avg_confidence,
                generated_at=datetime.now(),
                entry_price=signals[0].entry_price,
                source_patterns=combined_patterns,
            )

        elif len(sell_signals) > len(buy_signals):
            # Combine sell signals
            avg_confidence = sum(s.confidence for s in sell_signals) / len(sell_signals)
            combined_patterns = []
            for s in sell_signals:
                combined_patterns.extend(s.source_patterns)

            return TradingSignal(
                symbol=signals[0].symbol,
                signal_type="SELL",
                confidence=avg_confidence,
                generated_at=datetime.now(),
                entry_price=signals[0].entry_price,
                source_patterns=combined_patterns,
            )

        # Conflicting signals - return None
        return None

    async def _calculate_technical_score(self, analysis: MarketAnalysis) -> Decimal:
        """Calcula score baseado em indicadores técnicos"""
        score = Decimal("0.5")  # Neutral base
        factors = []

        # RSI
        if analysis.rsi:
            if analysis.rsi < Decimal("30"):  # Oversold - bullish
                factors.append(Decimal("0.7"))
            elif analysis.rsi > Decimal("70"):  # Overbought - bearish
                factors.append(Decimal("0.3"))
            else:
                factors.append(Decimal("0.5"))  # Neutral

        # MACD
        if analysis.macd_signal:
            if analysis.macd_signal == "BUY":
                factors.append(Decimal("0.8"))
            elif analysis.macd_signal == "SELL":
                factors.append(Decimal("0.2"))
            else:
                factors.append(Decimal("0.5"))

        # Moving averages
        if analysis.moving_averages:
            ma_score = self._evaluate_moving_averages(
                analysis.moving_averages, analysis.current_price
            )
            factors.append(ma_score)

        # Calculate weighted average
        if factors:
            score = sum(factors) / len(factors)

        return min(max(score, Decimal("0")), Decimal("1"))

    def _evaluate_moving_averages(self, mas: Dict[str, Decimal], current_price: Decimal) -> Decimal:
        """Avalia alinhamento das médias móveis"""
        # Simple evaluation: price above short MA = bullish
        if "MA20" in mas:
            if current_price > mas["MA20"]:
                return Decimal("0.7")  # Bullish
            else:
                return Decimal("0.3")  # Bearish

        return Decimal("0.5")  # Neutral

    async def _calculate_targets(
        self,
        entry_price: Decimal,
        signal_type: str,
        analysis: MarketAnalysis,
        strategy: TradingStrategy,
    ) -> tuple[Optional[Decimal], Optional[Decimal]]:
        """Calcula stop loss e take profit"""
        risk_percentage = strategy.risk_profile.default_stop_loss_percentage / 100
        reward_ratio = strategy.risk_profile.min_risk_reward_ratio

        if signal_type == "BUY":
            stop_loss = entry_price * (Decimal("1") - risk_percentage)
            take_profit = entry_price * (Decimal("1") + risk_percentage * reward_ratio)
        elif signal_type == "SELL":
            stop_loss = entry_price * (Decimal("1") + risk_percentage)
            take_profit = entry_price * (Decimal("1") - risk_percentage * reward_ratio)
        else:
            return None, None

        return stop_loss, take_profit
