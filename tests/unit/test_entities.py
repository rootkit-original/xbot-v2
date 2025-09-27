"""
XBot v2 - Domain Entities Unit Tests
Testes unitários completos para as entidades do domínio
"""

import pytest
from decimal import Decimal
from datetime import datetime
from typing import List

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.domain.entities import (
    RiskProfile, TradingBot, TradingStrategy, Order, Position, Market,
    Candle, Pattern, OrderType, OrderSide, OrderStatus,
    PatternType, RiskLevel, BotStatus
)


class TestRiskProfile:
    """Testes para RiskProfile"""

    def test_risk_profile_creation(self):
        """Testa criação básica de perfil de risco"""
        risk_profile = RiskProfile(
            max_position_size=Decimal("2.0"),
            max_daily_loss=Decimal("500.0"),
            max_concurrent_positions=5,
            stop_loss_percentage=Decimal("2.5"),
            take_profit_percentage=Decimal("5.0")
        )
        
        assert risk_profile.max_position_size == Decimal("2.0")
        assert risk_profile.max_daily_loss == Decimal("500.0")
        assert risk_profile.max_concurrent_positions == 5
        assert risk_profile.stop_loss_percentage == Decimal("2.5")
        assert risk_profile.take_profit_percentage == Decimal("5.0")

    def test_risk_profile_validation(self):
        """Testa validação de valores do perfil de risco"""
        # Test valid values
        risk_profile = RiskProfile(
            max_position_size=Decimal("1.0"),
            max_daily_loss=Decimal("100.0"),
            max_concurrent_positions=3,
            stop_loss_percentage=Decimal("1.5"),
            take_profit_percentage=Decimal("3.0")
        )
        
        assert risk_profile.max_position_size > Decimal("0")
        assert risk_profile.max_daily_loss > Decimal("0")
        assert risk_profile.max_concurrent_positions > 0

    def test_conservative_risk_profile(self):
        """Testa perfil conservador"""
        conservative = RiskProfile(
            max_position_size=Decimal("0.5"),
            max_daily_loss=Decimal("100.0"),
            max_concurrent_positions=2,
            stop_loss_percentage=Decimal("1.0"),
            take_profit_percentage=Decimal("2.0")
        )
        
        assert conservative.max_position_size <= Decimal("1.0")
        assert conservative.max_concurrent_positions <= 3

    def test_aggressive_risk_profile(self):
        """Testa perfil agressivo"""
        aggressive = RiskProfile(
            max_position_size=Decimal("5.0"),
            max_daily_loss=Decimal("2000.0"),
            max_concurrent_positions=10,
            stop_loss_percentage=Decimal("3.0"),
            take_profit_percentage=Decimal("10.0")
        )
        
        assert aggressive.max_position_size >= Decimal("3.0")
        assert aggressive.max_concurrent_positions >= 5


class TestTradingBot:
    """Testes para TradingBot"""

    def test_trading_bot_creation(self):
        """Testa criação básica do bot"""
        risk_profile = RiskProfile(
            max_position_size=Decimal("2.0"),
            max_daily_loss=Decimal("500.0"),
            max_concurrent_positions=5,
            stop_loss_percentage=Decimal("2.0"),
            take_profit_percentage=Decimal("4.0")
        )
        
        strategy = TradingStrategy(
            name="test_strategy",
            description="Test strategy"
        )
        
        bot = TradingBot(
            id="test-bot-1",
            name="Test Bot",
            strategy=strategy,
            initial_capital=Decimal("1000.0")
        )
        
        assert bot.id == "test-bot-1"
        assert bot.name == "Test Bot"
        assert bot.strategy.name == "test_strategy"
        assert bot.initial_capital == Decimal("1000.0")
        assert bot.status == BotStatus.IDLE

    def test_bot_status_management(self):
        """Testa gerenciamento de status do bot"""
        risk_profile = RiskProfile(
            max_position_size=Decimal("1.0"),
            max_daily_loss=Decimal("100.0"),
            max_concurrent_positions=3,
            stop_loss_percentage=Decimal("1.0"),
            take_profit_percentage=Decimal("2.0")
        )
        
        strategy = TradingStrategy(name="status_test_strategy")
        
        bot = TradingBot(
            id="status-test-bot",
            name="Status Test Bot",
            strategy=strategy,
            initial_capital=Decimal("500.0"),
            status=BotStatus.IDLE
        )
        
        # Test initial status
        assert bot.status == BotStatus.IDLE
        assert bot.name == "Status Test Bot"
        assert bot.initial_capital == Decimal("500.0")

    def test_bot_with_multiple_symbols(self):
        """Testa bot com diferentes símbolos"""
        risk_profile = RiskProfile(
            max_position_size=Decimal("1.5"),
            max_daily_loss=Decimal("200.0"),
            max_concurrent_positions=4,
            stop_loss_percentage=Decimal("1.5"),
            take_profit_percentage=Decimal("3.0")
        )
        
        symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT"]
        bots = []
        
        for i, symbol in enumerate(symbols):
            strategy = TradingStrategy(
                name=f"multi_symbol_strategy_{symbol}",
                description=f"Strategy for {symbol}"
            )
            
            bot = TradingBot(
                id=f"bot-{symbol.lower()}-{i}",
                name=f"Bot {symbol}",
                strategy=strategy,
                initial_capital=Decimal("250.0")  # 1000 / 4 symbols
            )
            bots.append(bot)
        
        assert len(bots) == 4
        assert all(bot.initial_capital == Decimal("250.0") for bot in bots)
        assert all(bot.status == BotStatus.IDLE for bot in bots)


class TestOrder:
    """Testes para Order"""

    def test_order_creation(self):
        """Testa criação básica de ordem"""
        order = Order(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=Decimal("0.001"),
            price=Decimal("50000.00"),
            status=OrderStatus.NEW
        )
        
        assert order.symbol == "BTCUSDT"
        assert order.side == OrderSide.BUY
        assert order.order_type == OrderType.MARKET
        assert order.quantity == Decimal("0.001")
        assert order.price == Decimal("50000.00")
        assert order.status == OrderStatus.NEW

    def test_buy_order(self):
        """Testa ordem de compra"""
        buy_order = Order(
            symbol="ETHUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Decimal("1.0"),
            price=Decimal("3000.00"),
            status=OrderStatus.FILLED
        )
        
        assert buy_order.side == OrderSide.BUY
        assert buy_order.order_type == OrderType.LIMIT
        assert buy_order.status == OrderStatus.FILLED

    def test_sell_order(self):
        """Testa ordem de venda"""
        sell_order = Order(
            symbol="ADAUSDT",
            side=OrderSide.SELL,
            order_type=OrderType.STOP,
            quantity=Decimal("1000.0"),
            price=Decimal("0.50"),
            status=OrderStatus.CANCELED
        )
        
        assert sell_order.side == OrderSide.SELL
        assert sell_order.order_type == OrderType.STOP
        assert sell_order.status == OrderStatus.CANCELED

    def test_order_calculations(self):
        """Testa cálculos da ordem"""
        order = Order(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=Decimal("0.1"),
            price=Decimal("45000.00"),
            status=OrderStatus.FILLED
        )
        
        total_value = order.quantity * order.price
        assert total_value == Decimal("4500.00")


class TestPosition:
    """Testes para Position"""

    def test_position_creation(self):
        """Testa criação de posição"""
        position = Position(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            quantity=Decimal("0.05"),
            entry_price=Decimal("48000.00"),
            current_price=Decimal("49000.00"),
            unrealized_pnl=Decimal("50.00"),
            realized_pnl=Decimal("0.00")
        )
        
        assert position.symbol == "BTCUSDT"
        assert position.side == OrderSide.BUY
        assert position.quantity == Decimal("0.05")
        assert position.entry_price == Decimal("48000.00")
        assert position.current_price == Decimal("49000.00")

    def test_position_pnl_calculation(self):
        """Testa cálculo de PnL"""
        position = Position(
            symbol="ETHUSDT",
            side=OrderSide.BUY,
            quantity=Decimal("2.0"),
            entry_price=Decimal("3000.00"),
            current_price=Decimal("3200.00"),
            unrealized_pnl=Decimal("400.00"),
            realized_pnl=Decimal("0.00")
        )
        
        expected_pnl = (position.current_price - position.entry_price) * position.quantity
        assert expected_pnl == Decimal("400.00")
        assert position.unrealized_pnl == expected_pnl

    def test_long_position(self):
        """Testa posição comprada (long)"""
        long_position = Position(
            symbol="ADAUSDT",
            side=OrderSide.BUY,
            quantity=Decimal("1000.0"),
            entry_price=Decimal("0.40"),
            current_price=Decimal("0.45"),
            unrealized_pnl=Decimal("50.00"),
            realized_pnl=Decimal("0.00")
        )
        
        assert long_position.side == OrderSide.BUY
        assert long_position.unrealized_pnl > 0  # Profitable long position

    def test_short_position(self):
        """Testa posição vendida (short)"""
        short_position = Position(
            symbol="BTCUSDT",
            side=OrderSide.SELL,
            quantity=Decimal("0.1"),
            entry_price=Decimal("50000.00"),
            current_price=Decimal("48000.00"),
            unrealized_pnl=Decimal("200.00"),
            realized_pnl=Decimal("0.00")
        )
        
        assert short_position.side == OrderSide.SELL
        assert short_position.unrealized_pnl > 0  # Profitable short position


class TestCandle:
    """Testes para Candle"""

    def test_candle_creation(self):
        """Testa criação de candle"""
        candle = Candle(
            symbol="BTCUSDT",
            timestamp=datetime.now(),
            open_price=Decimal("48000.00"),
            high_price=Decimal("49000.00"),
            low_price=Decimal("47500.00"),
            close_price=Decimal("48500.00"),
            volume=Decimal("100.0")
        )
        
        assert candle.symbol == "BTCUSDT"
        assert candle.open_price == Decimal("48000.00")
        assert candle.high_price == Decimal("49000.00")
        assert candle.low_price == Decimal("47500.00")
        assert candle.close_price == Decimal("48500.00")

    def test_candle_ohlc_validation(self):
        """Testa validação OHLC"""
        candle = Candle(
            symbol="ETHUSDT",
            timestamp=datetime.now(),
            open_price=Decimal("3000.00"),
            high_price=Decimal("3200.00"),  # Highest
            low_price=Decimal("2900.00"),   # Lowest
            close_price=Decimal("3100.00"),
            volume=Decimal("50.0")
        )
        
        assert candle.high_price >= candle.open_price
        assert candle.high_price >= candle.close_price
        assert candle.low_price <= candle.open_price
        assert candle.low_price <= candle.close_price

    def test_bullish_candle(self):
        """Testa candle de alta"""
        bullish_candle = Candle(
            symbol="ADAUSDT",
            timestamp=datetime.now(),
            open_price=Decimal("0.40"),
            high_price=Decimal("0.45"),
            low_price=Decimal("0.39"),
            close_price=Decimal("0.44"),  # Close > Open = Bullish
            volume=Decimal("1000.0")
        )
        
        assert bullish_candle.close_price > bullish_candle.open_price

    def test_bearish_candle(self):
        """Testa candle de baixa"""
        bearish_candle = Candle(
            symbol="DOTUSDT",
            timestamp=datetime.now(),
            open_price=Decimal("25.00"),
            high_price=Decimal("25.50"),
            low_price=Decimal("24.00"),
            close_price=Decimal("24.20"),  # Close < Open = Bearish
            volume=Decimal("200.0")
        )
        
        assert bearish_candle.close_price < bearish_candle.open_price


class TestPattern:
    """Testes para Pattern"""

    def test_pattern_creation(self):
        """Testa criação de padrão"""
        pattern = Pattern(
            pattern_type=PatternType.BREAKOUT,
            symbol="BTCUSDT",
            timeframe="1h",
            confidence=Decimal("0.85"),
            detected_at=datetime.now(),
            candles_analyzed=20,
            target_price=Decimal("52000.00"),
            stop_loss_price=Decimal("46000.00")
        )
        
        assert pattern.pattern_type == PatternType.BREAKOUT
        assert pattern.symbol == "BTCUSDT"
        assert pattern.confidence == Decimal("0.85")
        assert pattern.timeframe == "1h"
        assert pattern.target_price == Decimal("52000.00")

    def test_high_confidence_pattern(self):
        """Testa padrão de alta confiança"""
        high_confidence = Pattern(
            pattern_type=PatternType.TREND_REVERSAL,
            symbol="ETHUSDT",
            timeframe="4h",
            confidence=Decimal("0.95"),
            detected_at=datetime.now(),
            candles_analyzed=50,
            target_price=Decimal("3500.00"),
            stop_loss_price=Decimal("2800.00")
        )
        
        assert high_confidence.confidence >= 0.9

    def test_low_confidence_pattern(self):
        """Testa padrão de baixa confiança"""
        low_confidence = Pattern(
            pattern_type=PatternType.DOJI,
            symbol="ADAUSDT",
            timeframe="15m",
            confidence=Decimal("0.65"),
            detected_at=datetime.now(),
            candles_analyzed=10,
            target_price=Decimal("0.50"),
            stop_loss_price=Decimal("0.42")
        )
        
        assert low_confidence.confidence < 0.7

    def test_pattern_risk_reward(self):
        """Testa risk/reward do padrão"""
        pattern = Pattern(
            pattern_type=PatternType.SUPPORT_RESISTANCE,
            symbol="DOTUSDT",
            timeframe="1h",
            confidence=Decimal("0.80"),
            detected_at=datetime.now(),
            candles_analyzed=30,
            target_price=Decimal("120.00"),  # +20%
            stop_loss_price=Decimal("90.00")  # -10%
        )
        
        # Test pattern properties
        assert pattern.pattern_type == PatternType.SUPPORT_RESISTANCE
        assert pattern.confidence == Decimal("0.80")
        assert pattern.target_price == Decimal("120.00")
        assert pattern.stop_loss_price == Decimal("90.00")
        assert pattern.is_high_confidence is True  # confidence >= 0.8


if __name__ == "__main__":
    pytest.main([__file__])