#!/usr/bin/env python3
"""
Teste de importação dos serviços
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    print("🧪 Testando importações...")
    print("=" * 50)
    
    try:
        print("📦 Importando config...")
        from src.infrastructure.config import XBotConfig
        print("✅ XBotConfig importado com sucesso")
        
        print("📦 Criando config...")
        config = XBotConfig()
        print("✅ Config criado com sucesso")
        
        print("📦 Importando BinanceService...")
        from src.infrastructure.binance_service import BinanceService
        print("✅ BinanceService importado com sucesso")
        
        print("📦 Criando BinanceService...")
        binance_service = BinanceService(config.binance)
        print("✅ BinanceService criado com sucesso")
        
        print("📦 Importando TelegramService...")
        from src.infrastructure.telegram_service import TelegramNotificationService as TelegramService
        print("✅ TelegramService importado com sucesso")
        
        print("📦 Criando TelegramService...")
        telegram_service = TelegramService(
            bot_token=config.telegram.bot_token,
            admin_chat_id=config.telegram.admin_chat_id,
            group_chat_id=config.telegram.group_chat_id
        )
        print("✅ TelegramService criado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    print("\n" + "=" * 50)
    if success:
        print("🎉 Todas as importações funcionaram!")
    else:
        print("💥 Erro nas importações!")
    print("=" * 50)