#!/usr/bin/env python3
"""
XBot v2 - Strategy Usage Example
Exemplo prático de como usar as estratégias de trading
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from domain.entities import TradingBot, RiskProfile, PatternType
from strategies.predefined_strategies import TradingStrategies


def create_scalping_bot_example():
    """Exemplo de criação de bot com estratégia scalping"""
    
    print("⚡ Scalping Bot Example")
    print("=" * 40)
    
    # 1. Define risk profile for scalping
    scalping_risk = RiskProfile(
        max_risk_percentage=0.5,  # Conservative for scalping
        max_daily_loss=200.0,
        max_open_positions=5,     # Multiple quick positions
        stop_loss_percentage=1.0, # Tight stop loss
        take_profit_percentage=1.5 # Quick profits
    )
    
    # 2. Create scalping bot
    scalping_bot = TradingBot(
        name="Scalper Pro",
        symbol="BTCUSDT",
        timeframe="1m",
        strategy_name="scalping_conservative",
        risk_profile=scalping_risk,
        is_active=True,
        balance=1000.0
    )
    
    print(f"✅ Created scalping bot: {scalping_bot.name}")
    print(f"   - Symbol: {scalping_bot.symbol}")
    print(f"   - Timeframe: {scalping_bot.timeframe}")
    print(f"   - Strategy: {scalping_bot.strategy_name}")
    print(f"   - Max risk: {scalping_bot.risk_profile.max_risk_percentage}%")
    
    return scalping_bot


def create_swing_trading_bot_example():
    """Exemplo de criação de bot para swing trading"""
    
    print("\n📈 Swing Trading Bot Example")
    print("=" * 40)
    
    # 1. Define risk profile for swing trading
    swing_risk = RiskProfile(
        max_risk_percentage=2.0,   # Higher risk for longer holds
        max_daily_loss=500.0,
        max_open_positions=3,      # Fewer, longer positions
        stop_loss_percentage=3.0,  # Wider stop loss
        take_profit_percentage=8.0 # Larger profit targets
    )
    
    # 2. Create swing trading bot
    swing_bot = TradingBot(
        name="Swing Master",
        symbol="ETHUSDT",
        timeframe="4h",
        strategy_name="mean_reversion",
        risk_profile=swing_risk,
        is_active=True,
        balance=2000.0
    )
    
    print(f"✅ Created swing bot: {swing_bot.name}")
    print(f"   - Symbol: {swing_bot.symbol}")
    print(f"   - Timeframe: {swing_bot.timeframe}")
    print(f"   - Strategy: {swing_bot.strategy_name}")
    print(f"   - Max positions: {swing_bot.risk_profile.max_open_positions}")
    
    return swing_bot


def pattern_detection_example():
    """Exemplo de detecção de padrões"""
    
    print("\n🔍 Pattern Detection Example")
    print("=" * 40)
    
    # Available pattern types
    patterns = [
        PatternType.BREAKOUT,
        PatternType.REVERSAL,
        PatternType.CONTINUATION,
        PatternType.SUPPORT_RESISTANCE
    ]
    
    print("📋 Available Pattern Types:")
    for pattern in patterns:
        print(f"   - {pattern.value}")
    
    # Example usage
    print(f"\n💡 Usage Example:")
    print(f"   pattern_service.detect_patterns(candles, PatternType.BREAKOUT)")
    print(f"   risk_service.calculate_position_size(balance, risk_profile)")


def strategy_combinations_example():
    """Exemplo de combinações de estratégias"""
    
    print("\n🎯 Strategy Combinations Example")
    print("=" * 40)
    
    combinations = [
        {
            "name": "Conservative Portfolio",
            "strategies": ["scalping_conservative", "mean_reversion"],
            "allocation": [0.3, 0.7],
            "total_risk": 1.5
        },
        {
            "name": "Aggressive Portfolio", 
            "strategies": ["breakout_momentum", "trend_following"],
            "allocation": [0.6, 0.4],
            "total_risk": 3.0
        },
        {
            "name": "Balanced Portfolio",
            "strategies": ["scalping_conservative", "mean_reversion", "trend_following"],
            "allocation": [0.2, 0.5, 0.3],
            "total_risk": 2.0
        }
    ]
    
    print("📊 Strategy Portfolio Examples:")
    for combo in combinations:
        print(f"\n   🎯 {combo['name']}:")
        for i, strategy in enumerate(combo['strategies']):
            allocation = combo['allocation'][i] * 100
            print(f"      - {strategy}: {allocation}%")
        print(f"      - Total Risk: {combo['total_risk']}%")


def main():
    """Função principal do exemplo"""
    try:
        print("🚀 XBot v2 - Strategy Usage Examples")
        print("=" * 50)
        
        scalping_bot = create_scalping_bot_example()
        swing_bot = create_swing_trading_bot_example()
        pattern_detection_example()
        strategy_combinations_example()
        
        print(f"\n🎉 Strategy examples completed successfully!")
        print(f"💡 Bots created: {scalping_bot.name}, {swing_bot.name}")
        print(f"💡 Check examples/advanced/ for more complex scenarios")
        
    except Exception as e:
        print(f"❌ Error in strategy example: {e}")
        print(f"💡 Make sure all dependencies are installed")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())