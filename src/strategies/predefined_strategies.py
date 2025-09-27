"""
XBot v2 - Estratégias Pré-definidas

Coleção de estratégias de trading testadas e otimizadas.
"""

from decimal import Decimal
from typing import Dict, Any, List

from src.domain.entities import TradingStrategy, RiskProfile, RiskLevel


class TradingStrategies:
    """Coleção de estratégias de trading pré-definidas"""

    @staticmethod
    def scalping_conservative() -> TradingStrategy:
        """Estratégia de scalping conservadora"""
        return TradingStrategy(
            name="Scalping Conservador",
            description="Estratégia de scalping com foco em trades rápidos e baixo risco",
            target_symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT"],
            indicators={
                "rsi_period": 14,
                "rsi_oversold": 30,
                "rsi_overbought": 70,
                "ema_short": 5,
                "ema_long": 13,
                "bb_period": 20,
                "bb_std_dev": 2,
                "volume_sma": 20,
            },
            entry_conditions={
                "rsi_range": [25, 75],
                "ema_cross": True,
                "bb_squeeze": False,
                "volume_above_avg": True,
                "min_profit_target": 0.3,
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.CONSERVATIVE,
                max_position_size=Decimal("5.0"),
                max_concurrent_positions=2,
                stop_loss_percentage=Decimal("1.0"),
                take_profit_percentage=Decimal("2.0"),
                max_daily_loss=Decimal("3.0"),
            ),
        )

    @staticmethod
    def swing_trading_moderate() -> TradingStrategy:
        """Estratégia de swing trading moderada"""
        return TradingStrategy(
            name="Swing Trading Moderado",
            description="Estratégia de swing trading com holding de 1-7 dias",
            target_symbols=["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "LINKUSDT"],
            indicators={
                "rsi_period": 14,
                "rsi_oversold": 35,
                "rsi_overbought": 65,
                "ema_short": 9,
                "ema_long": 21,
                "sma_trend": 50,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "bb_period": 20,
            },
            entry_conditions={
                "rsi_range": [30, 70],
                "ema_cross": True,
                "macd_cross": True,
                "price_above_sma": True,
                "min_profit_target": 2.0,
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.MODERATE,
                max_position_size=Decimal("10.0"),
                max_concurrent_positions=3,
                stop_loss_percentage=Decimal("3.0"),
                take_profit_percentage=Decimal("6.0"),
                max_daily_loss=Decimal("5.0"),
            ),
        )

    @staticmethod
    def trend_following_aggressive() -> TradingStrategy:
        """Estratégia de trend following agressiva"""
        return TradingStrategy(
            name="Trend Following Agressivo",
            description="Estratégia agressiva de seguimento de tendência",
            target_symbols=["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT"],
            indicators={
                "rsi_period": 14,
                "ema_short": 8,
                "ema_medium": 21,
                "ema_long": 55,
                "atr_period": 14,
                "adx_period": 14,
                "adx_threshold": 25,
                "bb_period": 20,
            },
            entry_conditions={
                "trend_strength": "strong",
                "ema_alignment": True,
                "adx_above_threshold": True,
                "atr_filter": True,
                "min_profit_target": 4.0,
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.AGGRESSIVE,
                max_position_size=Decimal("15.0"),
                max_concurrent_positions=4,
                stop_loss_percentage=Decimal("5.0"),
                take_profit_percentage=Decimal("12.0"),
                max_daily_loss=Decimal("8.0"),
            ),
        )

    @staticmethod
    def breakout_strategy() -> TradingStrategy:
        """Estratégia de breakout de níveis"""
        return TradingStrategy(
            name="Breakout Strategy",
            description="Estratégia baseada em rompimento de níveis de suporte/resistência",
            target_symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT"],
            indicators={
                "bb_period": 20,
                "bb_std_dev": 2,
                "volume_sma": 20,
                "atr_period": 14,
                "rsi_period": 14,
                "support_resistance_period": 50,
            },
            entry_conditions={
                "breakout_confirmation": True,
                "volume_spike": True,
                "atr_expansion": True,
                "false_breakout_filter": True,
                "min_profit_target": 3.0,
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.MODERATE,
                max_position_size=Decimal("12.0"),
                max_concurrent_positions=3,
                stop_loss_percentage=Decimal("4.0"),
                take_profit_percentage=Decimal("8.0"),
                max_daily_loss=Decimal("6.0"),
            ),
        )

    @staticmethod
    def mean_reversion_strategy() -> TradingStrategy:
        """Estratégia de reversão à média"""
        return TradingStrategy(
            name="Mean Reversion",
            description="Estratégia baseada em reversão à média com Bollinger Bands",
            target_symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT"],
            indicators={
                "bb_period": 20,
                "bb_std_dev": 2,
                "rsi_period": 14,
                "stoch_k": 14,
                "stoch_d": 3,
                "volume_sma": 20,
                "price_sma": 20,
            },
            entry_conditions={
                "bb_oversold": True,
                "rsi_oversold": True,
                "stoch_oversold": True,
                "volume_confirmation": True,
                "mean_reversion_signal": True,
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.MODERATE,
                max_position_size=Decimal("8.0"),
                max_concurrent_positions=3,
                stop_loss_percentage=Decimal("2.5"),
                take_profit_percentage=Decimal("5.0"),
                max_daily_loss=Decimal("4.0"),
            ),
        )

    @staticmethod
    def grid_trading_strategy() -> TradingStrategy:
        """Estratégia de grid trading"""
        return TradingStrategy(
            name="Grid Trading",
            description="Estratégia de grid trading para mercados laterais",
            target_symbols=["BTCUSDT", "ETHUSDT"],
            indicators={
                "grid_levels": 8,
                "grid_spacing_percentage": 1.5,
                "atr_period": 14,
                "volatility_threshold": 0.02,
                "trend_filter": True,
                "range_detection": True,
            },
            entry_conditions={
                "sideways_market": True,
                "low_volatility": True,
                "grid_level_hit": True,
                "no_strong_trend": True,
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.CONSERVATIVE,
                max_position_size=Decimal("6.0"),
                max_concurrent_positions=8,  # Múltiplas posições pequenas
                stop_loss_percentage=Decimal("8.0"),  # Stop amplo para grid
                take_profit_percentage=Decimal("1.5"),  # Take pequeno por posição
                max_daily_loss=Decimal("3.0"),
            ),
        )

    @staticmethod
    def dca_strategy() -> TradingStrategy:
        """Estratégia DCA (Dollar Cost Averaging)"""
        return TradingStrategy(
            name="DCA Strategy",
            description="Estratégia de compra programada com DCA em quedas",
            target_symbols=["BTCUSDT", "ETHUSDT"],
            indicators={
                "price_drop_threshold": 5.0,  # % de queda para ativar DCA
                "sma_long": 200,
                "rsi_period": 14,
                "dca_levels": 5,
                "dca_multiplier": 1.5,
            },
            entry_conditions={
                "price_below_sma": True,
                "significant_drop": True,
                "oversold_condition": True,
                "no_knife_falling": True,  # Evitar quedas muito rápidas
            },
            risk_profile=RiskProfile(
                risk_level=RiskLevel.CONSERVATIVE,
                max_position_size=Decimal("20.0"),  # Posição maior para DCA
                max_concurrent_positions=2,
                stop_loss_percentage=Decimal("25.0"),  # Stop muito amplo
                take_profit_percentage=Decimal("15.0"),
                max_daily_loss=Decimal("5.0"),
            ),
        )

    @staticmethod
    def get_all_strategies() -> Dict[str, TradingStrategy]:
        """Retorna todas as estratégias disponíveis"""
        return {
            "scalping_conservative": TradingStrategies.scalping_conservative(),
            "swing_trading_moderate": TradingStrategies.swing_trading_moderate(),
            "trend_following_aggressive": TradingStrategies.trend_following_aggressive(),
            "breakout_strategy": TradingStrategies.breakout_strategy(),
            "mean_reversion_strategy": TradingStrategies.mean_reversion_strategy(),
            "grid_trading_strategy": TradingStrategies.grid_trading_strategy(),
            "dca_strategy": TradingStrategies.dca_strategy(),
        }

    @staticmethod
    def get_strategy_by_risk_level(risk_level: RiskLevel) -> List[TradingStrategy]:
        """Retorna estratégias filtradas por nível de risco"""
        all_strategies = TradingStrategies.get_all_strategies()

        return [
            strategy
            for strategy in all_strategies.values()
            if strategy.risk_profile.risk_level == risk_level
        ]

    @staticmethod
    def get_strategy_recommendations(
        capital: Decimal, experience_level: str, time_availability: str
    ) -> List[str]:
        """Recomenda estratégias baseadas no perfil do usuário"""
        recommendations = []

        # Baseado no capital
        if capital < Decimal("500"):
            recommendations.extend(["scalping_conservative", "grid_trading_strategy"])
        elif capital < Decimal("2000"):
            recommendations.extend(["swing_trading_moderate", "breakout_strategy"])
        else:
            recommendations.extend(["trend_following_aggressive", "dca_strategy"])

        # Baseado na experiência
        if experience_level.lower() == "beginner":
            recommendations = [r for r in recommendations if "conservative" in r or "grid" in r]
        elif experience_level.lower() == "advanced":
            recommendations.extend(["trend_following_aggressive", "breakout_strategy"])

        # Baseado no tempo disponível
        if time_availability.lower() == "low":
            recommendations = [r for r in recommendations if "swing" in r or "dca" in r]
        elif time_availability.lower() == "high":
            recommendations.extend(["scalping_conservative"])

        return list(set(recommendations))  # Remove duplicatas


# Exemplo de uso das estratégias
if __name__ == "__main__":
    # Listar todas as estratégias
    all_strategies = TradingStrategies.get_all_strategies()

    print("🎯 Estratégias Disponíveis:")
    for name, strategy in all_strategies.items():
        print(f"\n📊 {strategy.name}")
        print(f"   Descrição: {strategy.description}")
        print(f"   Nível de Risco: {strategy.risk_profile.risk_level.value}")
        print(f"   Símbolos: {', '.join(strategy.target_symbols)}")
        print(f"   Stop Loss: {strategy.risk_profile.stop_loss_percentage}%")
        print(f"   Take Profit: {strategy.risk_profile.take_profit_percentage}%")

    # Exemplo de recomendação
    print("\n\n🎯 Recomendações para iniciante com $1000:")
    recommendations = TradingStrategies.get_strategy_recommendations(
        capital=Decimal("1000"), experience_level="beginner", time_availability="medium"
    )

    for rec in recommendations:
        strategy = all_strategies.get(rec)
        if strategy:
            print(f"   ✅ {strategy.name}")
