#!/usr/bin/env python3
"""
Teste direto do Telegram Bot
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

def test_telegram():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print("🧪 Testando Telegram Bot...")
    print("=" * 50)
    print(f"📋 Bot Token: {'✅ Configurado' if bot_token else '❌ Não encontrado'}")
    print(f"💬 Chat ID: {'✅ Configurado' if chat_id else '❌ Não encontrado'}")
    
    if not bot_token or not chat_id:
        print("\n❌ Credenciais do Telegram não configuradas")
        return False
    
    try:
        # Teste 1: Get Bot Info
        print(f"\n🤖 Testando informações do bot...")
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                print(f"✅ Bot Info: @{bot_info['result']['username']}")
            else:
                print(f"❌ Erro: {bot_info.get('description', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
        
        # Teste 2: Send Test Message
        print(f"\n📤 Enviando mensagem de teste...")
        message = "🧪 **Teste XBot v2**\n\n✅ Sistema funcionando!\n💰 API Binance: Conectada\n🤖 Bots: 2 ativos"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result['ok']:
                print("✅ Mensagem enviada com sucesso!")
                print(f"📨 Message ID: {result['result']['message_id']}")
                return True
            else:
                print(f"❌ Erro ao enviar: {result.get('description', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_telegram()
    print("\n" + "=" * 50)
    if success:
        print("🎉 Telegram funcionando!")
        print("📱 Verifique seu celular para a mensagem de teste")
    else:
        print("💥 Problema no Telegram!")
        print("🔧 Verifique as configurações no .env")
    print("=" * 50)