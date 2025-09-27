"""
XBot v2 - Pattern Detection Service (Infrastructure Layer)

Serviço avançado para detecção de padrões de candlesticks e análise técnica.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import logging

from ..domain.entities import Candle, Pattern, PatternType
from ..domain.interfaces import IPatternDetectionService


logger = logging.getLogger(__name__)


class PatternDetectionService(IPatternDetectionService):
    """Serviço para detecção de padrões de candlesticks"""

    def __init__(self):
        self.pattern_detectors = {
            PatternType.BULLISH_ENGULFING: self._detect_bullish_engulfing,
            PatternType.BEARISH_ENGULFING: self._detect_bearish_engulfing,
            PatternType.HAMMER: self._detect_hammer,
            PatternType.DOJI: self._detect_doji,
            PatternType.SUPPORT_RESISTANCE: self._detect_support_resistance,
            PatternType.TREND_REVERSAL: self._detect_trend_reversal,
            PatternType.BREAKOUT: self._detect_breakout,
            PatternType.GOLDEN_CROSS: self._detect_golden_cross,
            PatternType.DEATH_CROSS: self._detect_death_cross,
        }

    async def detect_patterns(
        self, candles: List[Candle], pattern_types: Optional[List[PatternType]] = None
    ) -> List[Pattern]:
        """Detecta padrões nos candlesticks"""
        if len(candles) < 10:
            logger.warning("Poucos candles para análise de padrões")
            return []

        patterns = []
        types_to_check = pattern_types or list(PatternType)

        for pattern_type in types_to_check:
            if pattern_type in self.pattern_detectors:
                try:
                    detected = await self.pattern_detectors[pattern_type](candles)
                    if detected:
                        patterns.extend(detected)
                except Exception as e:
                    logger.error(f"Erro detectando padrão {pattern_type}: {e}")

        # Ordena por confiança
        patterns.sort(key=lambda p: p.confidence, reverse=True)
        return patterns

    async def analyze_pattern_strength(self, pattern: Pattern) -> Decimal:
        """Analisa força do padrão"""
        # Fatores que afetam a força do padrão
        base_confidence = pattern.confidence

        # Volume: padrões com volume alto são mais confiáveis
        volume_factor = Decimal("1.0")
        if hasattr(pattern, "volume_ratio") and pattern.volume_ratio:
            volume_factor = min(
                Decimal("1.2"),
                Decimal("1.0") + (pattern.volume_ratio - Decimal("1.0")) * Decimal("0.5"),
            )

        # Posição no contexto: padrões em níveis chave são mais fortes
        level_factor = Decimal("1.0")
        if pattern.key_levels:
            level_factor = Decimal("1.1")  # 10% bonus

        # Múltiplos timeframes: consenso entre timeframes
        timeframe_factor = Decimal("1.0")
        if hasattr(pattern, "timeframe_consensus"):
            timeframe_factor = Decimal("1.15")

        adjusted_confidence = base_confidence * volume_factor * level_factor * timeframe_factor
        return min(adjusted_confidence, Decimal("1.0"))

    async def get_pattern_targets(
        self, pattern: Pattern
    ) -> Tuple[Optional[Decimal], Optional[Decimal]]:
        """Obtém alvos do padrão (take profit, stop loss)"""
        if not pattern.key_levels:
            return None, None

        current_price = pattern.key_levels[-1] if pattern.key_levels else None
        if not current_price:
            return None, None

        # Estratégias de target baseadas no tipo de padrão
        if pattern.pattern_type in [PatternType.BULLISH_ENGULFING, PatternType.HAMMER]:
            # Padrões de reversão bullish
            risk = current_price * Decimal("0.02")  # 2% de risco
            reward = current_price * Decimal("0.06")  # 6% de recompensa (1:3)

            take_profit = current_price + reward
            stop_loss = current_price - risk

        elif pattern.pattern_type in [PatternType.BEARISH_ENGULFING]:
            # Padrões de reversão bearish
            risk = current_price * Decimal("0.02")
            reward = current_price * Decimal("0.06")

            take_profit = current_price - reward
            stop_loss = current_price + risk

        elif pattern.pattern_type == PatternType.BREAKOUT:
            # Breakout patterns
            risk = current_price * Decimal("0.015")  # 1.5% de risco
            reward = current_price * Decimal("0.045")  # 4.5% de recompensa

            if pattern.is_bullish:
                take_profit = current_price + reward
                stop_loss = current_price - risk
            else:
                take_profit = current_price - reward
                stop_loss = current_price + risk

        else:
            # Default: 1:2 risk/reward
            risk = current_price * Decimal("0.025")
            reward = current_price * Decimal("0.05")

            if pattern.is_bullish:
                take_profit = current_price + reward
                stop_loss = current_price - risk
            else:
                take_profit = current_price - reward
                stop_loss = current_price + risk

        return take_profit, stop_loss

    # ========================================
    # Pattern Detection Methods
    # ========================================

    async def _detect_bullish_engulfing(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta padrão Bullish Engulfing"""
        patterns = []

        for i in range(1, len(candles)):
            prev_candle = candles[i - 1]
            curr_candle = candles[i]

            # Condições para Bullish Engulfing
            if (
                prev_candle.is_bearish
                and curr_candle.is_bullish
                and curr_candle.open_price < prev_candle.close_price
                and curr_candle.close_price > prev_candle.open_price
                and curr_candle.body_size > prev_candle.body_size * Decimal("1.2")
            ):  # Corpo 20% maior

                # Calcula confiança baseada no engolfamento
                engulfment_ratio = curr_candle.body_size / prev_candle.body_size
                confidence = min(
                    Decimal("0.9"),
                    Decimal("0.6") + (engulfment_ratio - Decimal("1.0")) * Decimal("0.1"),
                )

                # Volume confirmation
                volume_ratio = (
                    curr_candle.volume / prev_candle.volume
                    if prev_candle.volume > 0
                    else Decimal("1.0")
                )
                if volume_ratio > Decimal("1.5"):  # Volume 50% maior
                    confidence += Decimal("0.1")

                pattern = Pattern(
                    pattern_type=PatternType.BULLISH_ENGULFING,
                    symbol=curr_candle.symbol,
                    timeframe="",
                    confidence=min(confidence, Decimal("1.0")),
                    detected_at=curr_candle.timestamp,
                    candles_analyzed=2,
                    key_levels=[
                        prev_candle.low_price,
                        curr_candle.high_price,
                        curr_candle.close_price,
                    ],
                    is_bullish=True,
                )

                patterns.append(pattern)

        return patterns

    async def _detect_bearish_engulfing(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta padrão Bearish Engulfing"""
        patterns = []

        for i in range(1, len(candles)):
            prev_candle = candles[i - 1]
            curr_candle = candles[i]

            # Condições para Bearish Engulfing
            if (
                prev_candle.is_bullish
                and curr_candle.is_bearish
                and curr_candle.open_price > prev_candle.close_price
                and curr_candle.close_price < prev_candle.open_price
                and curr_candle.body_size > prev_candle.body_size * Decimal("1.2")
            ):

                engulfment_ratio = curr_candle.body_size / prev_candle.body_size
                confidence = min(
                    Decimal("0.9"),
                    Decimal("0.6") + (engulfment_ratio - Decimal("1.0")) * Decimal("0.1"),
                )

                volume_ratio = (
                    curr_candle.volume / prev_candle.volume
                    if prev_candle.volume > 0
                    else Decimal("1.0")
                )
                if volume_ratio > Decimal("1.5"):
                    confidence += Decimal("0.1")

                pattern = Pattern(
                    pattern_type=PatternType.BEARISH_ENGULFING,
                    symbol=curr_candle.symbol,
                    timeframe="",
                    confidence=min(confidence, Decimal("1.0")),
                    detected_at=curr_candle.timestamp,
                    candles_analyzed=2,
                    key_levels=[
                        prev_candle.high_price,
                        curr_candle.low_price,
                        curr_candle.close_price,
                    ],
                    is_bearish=True,
                )

                patterns.append(pattern)

        return patterns

    async def _detect_hammer(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta padrão Hammer"""
        patterns = []

        for candle in candles[-10:]:  # Últimos 10 candles
            body_size = candle.body_size
            lower_shadow = candle.lower_shadow
            upper_shadow = candle.upper_shadow

            # Condições para Hammer
            if (
                lower_shadow >= body_size * Decimal("2.0")  # Sombra inferior >= 2x corpo
                and upper_shadow <= body_size * Decimal("0.5")  # Sombra superior <= 0.5x corpo
                and body_size > Decimal("0")
            ):  # Tem corpo

                # Confiança baseada na proporção das sombras
                shadow_ratio = lower_shadow / body_size if body_size > 0 else Decimal("0")
                confidence = min(Decimal("0.85"), Decimal("0.5") + shadow_ratio * Decimal("0.1"))

                # Tendência anterior (precisa estar em downtrend)
                if len(candles) >= 5:
                    recent_candles = candles[-5:-1]
                    downtrend_count = sum(1 for c in recent_candles if c.is_bearish)
                    if downtrend_count >= 3:
                        confidence += Decimal("0.15")

                pattern = Pattern(
                    pattern_type=PatternType.HAMMER,
                    symbol=candle.symbol,
                    timeframe="",
                    confidence=min(confidence, Decimal("1.0")),
                    detected_at=candle.timestamp,
                    candles_analyzed=1,
                    key_levels=[candle.low_price, candle.close_price],
                    is_bullish=True,
                )

                patterns.append(pattern)

        return patterns

    async def _detect_doji(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta padrão Doji"""
        patterns = []

        for candle in candles[-5:]:  # Últimos 5 candles
            body_size = candle.body_size
            total_range = candle.high_price - candle.low_price

            # Condições para Doji
            if total_range > 0 and body_size <= total_range * Decimal(
                "0.1"
            ):  # Corpo <= 10% do range total

                # Confiança baseada na simetria das sombras
                upper_shadow = candle.upper_shadow
                lower_shadow = candle.lower_shadow

                if upper_shadow > 0 and lower_shadow > 0:
                    shadow_symmetry = min(upper_shadow, lower_shadow) / max(
                        upper_shadow, lower_shadow
                    )
                    confidence = Decimal("0.6") + shadow_symmetry * Decimal("0.3")
                else:
                    confidence = Decimal("0.5")

                # Volume baixo confirma indecisão
                if len(candles) >= 3:
                    avg_volume = sum(c.volume for c in candles[-3:-1]) / Decimal("2")
                    if candle.volume < avg_volume * Decimal("0.8"):
                        confidence += Decimal("0.1")

                pattern = Pattern(
                    pattern_type=PatternType.DOJI,
                    symbol=candle.symbol,
                    timeframe="",
                    confidence=min(confidence, Decimal("1.0")),
                    detected_at=candle.timestamp,
                    candles_analyzed=1,
                    key_levels=[candle.close_price],
                    is_bullish=False,
                    is_bearish=False,  # Doji é neutro
                )

                patterns.append(pattern)

        return patterns

    async def _detect_support_resistance(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta níveis de suporte e resistência"""
        if len(candles) < 20:
            return []

        patterns = []

        # Extrai highs e lows
        highs = [c.high_price for c in candles]
        lows = [c.low_price for c in candles]

        # Encontra pivôs
        resistance_levels = self._find_pivot_points(highs, is_high=True)
        support_levels = self._find_pivot_points(lows, is_high=False)

        current_price = candles[-1].close_price

        # Resistência próxima
        nearby_resistance = [
            r
            for r in resistance_levels
            if r > current_price and r <= current_price * Decimal("1.05")
        ]

        if nearby_resistance:
            pattern = Pattern(
                pattern_type=PatternType.SUPPORT_RESISTANCE,
                symbol=candles[-1].symbol,
                timeframe="",
                confidence=Decimal("0.75"),
                detected_at=candles[-1].timestamp,
                candles_analyzed=len(candles),
                key_levels=nearby_resistance,
                is_bearish=True,  # Resistência é bearish
            )
            patterns.append(pattern)

        # Suporte próximo
        nearby_support = [
            s for s in support_levels if s < current_price and s >= current_price * Decimal("0.95")
        ]

        if nearby_support:
            pattern = Pattern(
                pattern_type=PatternType.SUPPORT_RESISTANCE,
                symbol=candles[-1].symbol,
                timeframe="",
                confidence=Decimal("0.75"),
                detected_at=candles[-1].timestamp,
                candles_analyzed=len(candles),
                key_levels=nearby_support,
                is_bullish=True,  # Suporte é bullish
            )
            patterns.append(pattern)

        return patterns

    async def _detect_trend_reversal(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta reversão de tendência"""
        if len(candles) < 10:
            return []

        patterns = []

        # Calcula EMAs para identificar tendência
        ema_short = self._calculate_ema([c.close_price for c in candles], 5)
        ema_long = self._calculate_ema([c.close_price for c in candles], 10)

        if len(ema_short) < 3 or len(ema_long) < 3:
            return patterns

        # Detecta cruzamento de EMAs
        prev_short, prev_long = ema_short[-2], ema_long[-2]
        curr_short, curr_long = ema_short[-1], ema_long[-1]

        # Bullish reversal (EMA curta cruza acima da longa)
        if prev_short <= prev_long and curr_short > curr_long:
            confidence = Decimal("0.7")

            # Volume confirmation
            if len(candles) >= 2:
                volume_ratio = candles[-1].volume / candles[-2].volume
                if volume_ratio > Decimal("1.3"):
                    confidence += Decimal("0.15")

            pattern = Pattern(
                pattern_type=PatternType.TREND_REVERSAL,
                symbol=candles[-1].symbol,
                timeframe="",
                confidence=min(confidence, Decimal("1.0")),
                detected_at=candles[-1].timestamp,
                candles_analyzed=10,
                key_levels=[curr_short, curr_long],
                is_bullish=True,
            )
            patterns.append(pattern)

        # Bearish reversal (EMA curta cruza abaixo da longa)
        elif prev_short >= prev_long and curr_short < curr_long:
            confidence = Decimal("0.7")

            if len(candles) >= 2:
                volume_ratio = candles[-1].volume / candles[-2].volume
                if volume_ratio > Decimal("1.3"):
                    confidence += Decimal("0.15")

            pattern = Pattern(
                pattern_type=PatternType.TREND_REVERSAL,
                symbol=candles[-1].symbol,
                timeframe="",
                confidence=min(confidence, Decimal("1.0")),
                detected_at=candles[-1].timestamp,
                candles_analyzed=10,
                key_levels=[curr_short, curr_long],
                is_bearish=True,
            )
            patterns.append(pattern)

        return patterns

    async def _detect_breakout(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta breakouts de consolidação"""
        if len(candles) < 20:
            return []

        patterns = []

        # Analisa últimos 15 candles para consolidação
        consolidation_candles = candles[-15:-1]
        recent_highs = [c.high_price for c in consolidation_candles]
        recent_lows = [c.low_price for c in consolidation_candles]

        resistance_level = max(recent_highs)
        support_level = min(recent_lows)
        range_size = resistance_level - support_level

        # Verifica se estava em consolidação (range pequeno)
        avg_price = (resistance_level + support_level) / Decimal("2")
        if range_size < avg_price * Decimal("0.05"):  # Range < 5% do preço médio

            current_candle = candles[-1]

            # Breakout bullish (acima da resistência)
            if current_candle.close_price > resistance_level and current_candle.volume > sum(
                c.volume for c in consolidation_candles[-5:]
            ) / Decimal("5") * Decimal("1.5"):

                confidence = Decimal("0.75")
                if current_candle.close_price > resistance_level * Decimal("1.01"):  # 1% acima
                    confidence += Decimal("0.1")

                pattern = Pattern(
                    pattern_type=PatternType.BREAKOUT,
                    symbol=current_candle.symbol,
                    timeframe="",
                    confidence=min(confidence, Decimal("1.0")),
                    detected_at=current_candle.timestamp,
                    candles_analyzed=16,
                    key_levels=[support_level, resistance_level, current_candle.close_price],
                    is_bullish=True,
                )
                patterns.append(pattern)

            # Breakout bearish (abaixo do suporte)
            elif current_candle.close_price < support_level and current_candle.volume > sum(
                c.volume for c in consolidation_candles[-5:]
            ) / Decimal("5") * Decimal("1.5"):

                confidence = Decimal("0.75")
                if current_candle.close_price < support_level * Decimal("0.99"):  # 1% abaixo
                    confidence += Decimal("0.1")

                pattern = Pattern(
                    pattern_type=PatternType.BREAKOUT,
                    symbol=current_candle.symbol,
                    timeframe="",
                    confidence=min(confidence, Decimal("1.0")),
                    detected_at=current_candle.timestamp,
                    candles_analyzed=16,
                    key_levels=[support_level, resistance_level, current_candle.close_price],
                    is_bearish=True,
                )
                patterns.append(pattern)

        return patterns

    async def _detect_golden_cross(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta Golden Cross (MA50 cruza acima MA200)"""
        if len(candles) < 200:
            return []

        patterns = []

        # Calcula MAs
        closes = [c.close_price for c in candles]
        ma50 = self._calculate_sma(closes, 50)
        ma200 = self._calculate_sma(closes, 200)

        if len(ma50) >= 2 and len(ma200) >= 2:
            # Verifica cruzamento
            if ma50[-2] <= ma200[-2] and ma50[-1] > ma200[-1]:
                pattern = Pattern(
                    pattern_type=PatternType.GOLDEN_CROSS,
                    symbol=candles[-1].symbol,
                    timeframe="",
                    confidence=Decimal("0.8"),
                    detected_at=candles[-1].timestamp,
                    candles_analyzed=200,
                    key_levels=[ma50[-1], ma200[-1]],
                    is_bullish=True,
                )
                patterns.append(pattern)

        return patterns

    async def _detect_death_cross(self, candles: List[Candle]) -> List[Pattern]:
        """Detecta Death Cross (MA50 cruza abaixo MA200)"""
        if len(candles) < 200:
            return []

        patterns = []

        closes = [c.close_price for c in candles]
        ma50 = self._calculate_sma(closes, 50)
        ma200 = self._calculate_sma(closes, 200)

        if len(ma50) >= 2 and len(ma200) >= 2:
            if ma50[-2] >= ma200[-2] and ma50[-1] < ma200[-1]:
                pattern = Pattern(
                    pattern_type=PatternType.DEATH_CROSS,
                    symbol=candles[-1].symbol,
                    timeframe="",
                    confidence=Decimal("0.8"),
                    detected_at=candles[-1].timestamp,
                    candles_analyzed=200,
                    key_levels=[ma50[-1], ma200[-1]],
                    is_bearish=True,
                )
                patterns.append(pattern)

        return patterns

    # ========================================
    # Helper Methods
    # ========================================

    def _find_pivot_points(
        self, values: List[Decimal], is_high: bool, window: int = 5
    ) -> List[Decimal]:
        """Encontra pontos de pivô"""
        pivots = []

        for i in range(window, len(values) - window):
            if is_high:
                # Pivot high: valor é máximo local
                if all(values[i] >= values[j] for j in range(i - window, i + window + 1) if j != i):
                    pivots.append(values[i])
            else:
                # Pivot low: valor é mínimo local
                if all(values[i] <= values[j] for j in range(i - window, i + window + 1) if j != i):
                    pivots.append(values[i])

        # Remove duplicatas e ordena
        return sorted(list(set(pivots)))

    def _calculate_sma(self, values: List[Decimal], period: int) -> List[Decimal]:
        """Calcula Simple Moving Average"""
        if len(values) < period:
            return []

        sma = []
        for i in range(period - 1, len(values)):
            avg = sum(values[i - period + 1 : i + 1]) / Decimal(period)
            sma.append(avg)

        return sma

    def _calculate_ema(self, values: List[Decimal], period: int) -> List[Decimal]:
        """Calcula Exponential Moving Average"""
        if len(values) < period:
            return []

        ema = []
        multiplier = Decimal("2") / (Decimal(period) + Decimal("1"))

        # Primeira EMA é uma SMA
        first_ema = sum(values[:period]) / Decimal(period)
        ema.append(first_ema)

        for i in range(period, len(values)):
            current_ema = (values[i] * multiplier) + (ema[-1] * (Decimal("1") - multiplier))
            ema.append(current_ema)

        return ema
