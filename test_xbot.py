#!/usr/bin/env python3
"""
XBot v2 - Test Script

Script simples para testar o sistema.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

print("🧪 Testando XBot v2...")
print(f"Diretório atual: {current_dir}")
print(f"Diretório src: {src_dir}")

try:
    # Test basic imports
    print("\n📦 Testando imports básicos...")
    from domain.entities import TradingBot, Order, Position
    print("  ✅ Entidades de domínio")
    
    from domain.interfaces import IMarketDataRepository
    print("  ✅ Interfaces de domínio")
    
    from infrastructure.config import XBotConfig
    print("  ✅ Configuração")
    
    from strategies.predefined_strategies import TradingStrategies
    print("  ✅ Estratégias pré-definidas")
    
    # Test config
    print("\n⚙️  Testando configuração...")
    config = XBotConfig()
    print(f"  ✅ Config carregada - Testnet: {config.binance_testnet}")
    
    # Test strategies
    print("\n🎯 Testando estratégias...")
    strategies = TradingStrategies.get_all_strategies()
    print(f"  ✅ {len(strategies)} estratégias disponíveis:")
    for name, strategy in strategies.items():
        print(f"    • {strategy.name} ({strategy.risk_profile.risk_level.value})")
    
    print("\n🎉 Todos os testes passaram!")
    print("\n📋 Para usar o sistema:")
    print("1. Configure o arquivo .env com suas credenciais")
    print("2. Execute: python test_xbot.py --demo")
    print("3. Ou use: python -m src.main --help")
    
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("Verifique se todos os arquivos estão no lugar correto")
except Exception as e:
    print(f"❌ Erro: {e}")
    print("Erro inesperado durante o teste")

if len(sys.argv) > 1 and sys.argv[1] == '--demo':
    print("\n🚀 Executando demo simplificado...")
    
    try:
        from decimal import Decimal
        
        # Create demo trading strategy
        demo_strategy = TradingStrategies.scalping_conservative()
        
        print(f"\n📊 Estratégia Demo: {demo_strategy.name}")
        print(f"   Símbolos: {', '.join(demo_strategy.target_symbols)}")
        print(f"   Nível de Risco: {demo_strategy.risk_profile.risk_level.value}")
        print(f"   Stop Loss: {demo_strategy.risk_profile.stop_loss_percentage}%")
        print(f"   Take Profit: {demo_strategy.risk_profile.take_profit_percentage}%")
        
        # Create demo bot (without actual trading)
        demo_bot = TradingBot(
            id="demo-bot-001",
            name="Demo Bot",
            strategy=demo_strategy,
            initial_capital=Decimal("1000")
        )
        
        print(f"\n🤖 Bot Demo Criado:")
        print(f"   ID: {demo_bot.id}")
        print(f"   Nome: {demo_bot.name}")
        print(f"   Capital Inicial: ${demo_bot.initial_capital}")
        print(f"   Status: {demo_bot.status.value}")
        
        print("\n✨ Demo concluído com sucesso!")
        print("O sistema está pronto para uso real com credenciais da Binance.")
        
    except Exception as e:
        print(f"❌ Erro no demo: {e}")
        print("Verifique a implementação das classes")