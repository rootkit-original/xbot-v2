#!/usr/bin/env python3
"""
Teste de notificação para simular um trade
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

def send_trade_notification():
    """Simula uma notificação de trade"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ Telegram não configurado")
        return False
    
    # Simular dados de um trade
    message = """
🤖 **XBot v2 - Trade Executado**

📊 **Bot:** TestBot-Baixo
💹 **Par:** BTCUSDT
📈 **Tipo:** BUY (Long)
💰 **Valor:** $10.00
💵 **Preço:** $65,432.50
📊 **Quantidade:** 0.00015 BTC

⏰ **Horário:** 15:58:32
🎯 **Take Profit:** $66,500 (+1.63%)
🛑 **Stop Loss:** $64,200 (-1.89%)

📈 **Performance Total:**
💰 Capital: $20.00
📊 P&L Hoje: +$0.00 (0.00%)
🎯 Trades: 1 (1 Win / 0 Loss)
    """.strip()
    
    try:
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
                print("✅ Notificação de trade enviada!")
                return True
            else:
                print(f"❌ Erro: {result.get('description', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    print("📱 Simulando notificação de trade...")
    success = send_trade_notification()
    if success:
        print("🎉 Verifique seu Telegram!")
    else:
        print("💥 Falha na notificação!")