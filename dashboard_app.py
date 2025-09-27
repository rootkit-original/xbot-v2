#!/usr/bin/env python3
"""
XBot v2 - Dashboard Web
========================

Dashboard interativo em tempo real para monitoramento dos bots
"""

import os
import json
import threading
import webbrowser
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Carregar .env
load_dotenv()

app = Flask(__name__)

class DashboardData:
    """Classe para gerenciar dados do dashboard"""
    
    def __init__(self):
        self.bots_file = Path("data/bots.json")
        self.logs_file = Path("logs/xbot.log")
        self.binance_client = None
        self._init_binance_client()
        
    def _init_binance_client(self):
        """Inicializa o cliente da Binance"""
        try:
            api_key = os.getenv('BINANCE_API_KEY')
            api_secret = os.getenv('BINANCE_SECRET_KEY')
            
            if api_key and api_secret:
                self.binance_client = Client(api_key, api_secret)
                # Testar conexão
                self.binance_client.get_account()
                print("✅ Cliente Binance conectado com sucesso")
            else:
                print("⚠️ Credenciais da Binance não encontradas")
        except Exception as e:
            print(f"❌ Erro ao conectar com Binance: {e}")
            self.binance_client = None
        
    def get_bots_data(self):
        """Retorna dados dos bots"""
        if not self.bots_file.exists():
            return []
        
        try:
            with open(self.bots_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def get_binance_account_info(self):
        """Obtém informações da conta Binance"""
        if not self.binance_client:
            return None
            
        try:
            account = self.binance_client.get_account()
            return {
                'balances': [
                    {
                        'asset': balance['asset'],
                        'free': float(balance['free']),
                        'locked': float(balance['locked']),
                        'total': float(balance['free']) + float(balance['locked'])
                    }
                    for balance in account['balances']
                    if float(balance['free']) > 0 or float(balance['locked']) > 0
                ],
                'maker_commission': account['makerCommission'],
                'taker_commission': account['takerCommission'],
                'can_trade': account['canTrade'],
                'can_withdraw': account['canWithdraw'],
                'can_deposit': account['canDeposit']
            }
        except Exception as e:
            print(f"Erro ao obter info da conta: {e}")
            return None
    
    def get_open_orders(self):
        """Obtém ordens em aberto"""
        if not self.binance_client:
            return []
            
        try:
            orders = self.binance_client.get_open_orders()
            return [
                {
                    'symbol': order['symbol'],
                    'orderId': order['orderId'],
                    'side': order['side'],
                    'type': order['type'],
                    'origQty': float(order['origQty']),
                    'price': float(order['price']),
                    'stopPrice': float(order.get('stopPrice', 0)),
                    'time': datetime.fromtimestamp(order['time'] / 1000).strftime('%H:%M:%S'),
                    'timeInForce': order['timeInForce'],
                    'status': order['status']
                }
                for order in orders
            ]
        except Exception as e:
            print(f"Erro ao obter ordens: {e}")
            return []
    
    def get_market_data(self):
        """Obtém dados de mercado em tempo real"""
        if not self.binance_client:
            return {}
            
        try:
            # Símbolos principais
            symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT', 'SOLUSDT']
            tickers = self.binance_client.get_ticker()
            
            market_data = {}
            for ticker in tickers:
                if ticker['symbol'] in symbols:
                    market_data[ticker['symbol']] = {
                        'price': float(ticker['lastPrice']),
                        'change': float(ticker['priceChangePercent'])
                    }
            
            return market_data
        except Exception as e:
            print(f"Erro ao obter dados de mercado: {e}")
            return {}

    def get_system_status(self):
        """Retorna status do sistema"""
        bots = self.get_bots_data()
        account_info = self.get_binance_account_info()
        market_data = self.get_market_data()
        
        # Calcular capital total real da Binance
        total_usdt = 0
        if account_info:
            for balance in account_info['balances']:
                if balance['asset'] == 'USDT':
                    total_usdt = balance['total']
                    break
        
        # Dados dos bots
        total_capital = sum(Decimal(bot['current_capital']) for bot in bots) if bots else Decimal(total_usdt)
        total_initial = sum(Decimal(bot['initial_capital']) for bot in bots) if bots else Decimal(total_usdt)
        total_pnl = total_capital - total_initial
        
        return {
            'total_bots': len(bots),
            'active_bots': len([b for b in bots if b['status'] == 'ACTIVE']),
            'idle_bots': len([b for b in bots if b['status'] == 'IDLE']),
            'total_capital': float(total_capital),
            'total_pnl': float(total_pnl),
            'pnl_percentage': float((total_pnl / total_initial * 100)) if total_initial > 0 else 0,
            'binance_connected': self.binance_client is not None,
            'telegram_connected': bool(os.getenv('TELEGRAM_BOT_TOKEN')),
            'market_data': market_data,
            'account_info': account_info,
            'usdt_balance': total_usdt,
            'last_update': datetime.now().strftime('%H:%M:%S')
        }
    
    def get_performance_data(self):
        """Retorna dados de performance para gráficos"""
        # Simular dados históricos (você pode implementar com dados reais)
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
        
        return {
            'dates': dates,
            'pnl_history': [0, 5, -2, 8, 12, 15, 18],  # Exemplo de P&L diário
            'trades_history': [0, 2, 1, 3, 4, 2, 5],   # Exemplo de trades por dia
            'volume_history': [0, 150, 80, 220, 180, 320, 280]  # Exemplo de volume
        }

dashboard_data = DashboardData()

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard.html')

@app.route('/api/system-status')
def api_system_status():
    """API para status do sistema"""
    return jsonify(dashboard_data.get_system_status())

@app.route('/api/bots')
def api_bots():
    """API para dados dos bots"""
    return jsonify(dashboard_data.get_bots_data())

@app.route('/api/performance')
def api_performance():
    """API para dados de performance"""
    return jsonify(dashboard_data.get_performance_data())

@app.route('/api/open-orders')
def api_open_orders():
    """API para ordens em aberto"""
    return jsonify(dashboard_data.get_open_orders())

@app.route('/api/account-info')
def api_account_info():
    """API para informações da conta"""
    return jsonify(dashboard_data.get_binance_account_info())

@app.route('/api/market-data')
def api_market_data():
    """API para dados de mercado"""
    return jsonify(dashboard_data.get_market_data())

def run_dashboard():
    """Executa o dashboard"""
    print("🚀 Iniciando Dashboard XBot v2...")
    print("📊 Acesse: http://localhost:5000")
    print("⏹️  Para parar: Ctrl+C")
    
    # Abrir browser automaticamente
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000')).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    run_dashboard()