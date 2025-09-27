#!/usr/bin/env python3
"""
XBot v2 - Basic Configuration Example
Exemplo básico de configuração e inicialização do XBot v2
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from infrastructure.config import XBotConfig
from domain.entities import RiskProfile, TradingStrategy


def basic_configuration_example():
    """Exemplo básico de configuração do XBot v2"""
    
    print("🔧 XBot v2 - Basic Configuration Example")
    print("=" * 50)
    
    # 1. Create basic configuration
    config = XBotConfig()
    
    print("✅ Configuration loaded successfully")
    print(f"   - Environment: {'Testnet' if config.binance.testnet else 'Production'}")
    print(f"   - Max position size: {config.risk.max_position_size}")
    print(f"   - Risk percentage: {config.risk.risk_percentage}%")
    
    # 2. Example risk profile
    conservative_risk = RiskProfile(
        max_risk_percentage=1.0,
        max_daily_loss=500.0,
        max_open_positions=3,
        stop_loss_percentage=2.0,
        take_profit_percentage=4.0
    )
    
    print(f"✅ Conservative risk profile created")
    print(f"   - Max risk: {conservative_risk.max_risk_percentage}%")
    print(f"   - Max daily loss: ${conservative_risk.max_daily_loss}")
    print(f"   - Max positions: {conservative_risk.max_open_positions}")
    
    # 3. Example trading strategy configuration
    print(f"✅ Available strategies: {len(config.get_available_strategies())}")
    
    return config


def environment_setup_example():
    """Exemplo de configuração de ambiente"""
    
    print("\n🌍 Environment Setup Example")
    print("=" * 50)
    
    # Check environment variables
    env_vars = {
        "BYBIT_API_KEY": os.getenv("BYBIT_API_KEY", "Not set"),
        "BYBIT_API_SECRET": os.getenv("BYBIT_API_SECRET", "Not set"),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", "Not set"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO")
    }
    
    print("📋 Environment Variables:")
    for key, value in env_vars.items():
        masked_value = "***" if "SECRET" in key or "TOKEN" in key else value
        status = "✅" if value != "Not set" else "⚠️"
        print(f"   {status} {key}: {masked_value}")
    
    # Configuration recommendations
    print("\n💡 Configuration Recommendations:")
    print("   1. Set BYBIT_API_KEY and BYBIT_API_SECRET for trading")
    print("   2. Configure TELEGRAM_BOT_TOKEN for notifications")
    print("   3. Use BYBIT_TESTNET=True for development")
    print("   4. Set LOG_LEVEL=DEBUG for detailed logging")


def main():
    """Função principal do exemplo"""
    try:
        config = basic_configuration_example()
        environment_setup_example()
        
        print(f"\n🎉 Basic configuration example completed successfully!")
        print(f"💡 Next: Check examples/advanced/ for more complex examples")
        
    except Exception as e:
        print(f"❌ Error in configuration example: {e}")
        print(f"💡 Make sure to run the installation script first")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())