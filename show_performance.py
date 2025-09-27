#!/usr/bin/env python3
"""
Dashboard de Performance dos Bots
"""

import sys
import json
from pathlib import Path
from decimal import Decimal
from datetime import datetime

def show_performance():
    """Mostra performance detalhada dos bots"""
    
    bots_file = Path("data/bots.json")
    
    print("📊 Dashboard de Performance XBot v2")
    print("=" * 60)
    
    if not bots_file.exists():
        print("❌ Nenhum bot encontrado")
        return
    
    try:
        with open(bots_file, 'r') as f:
            bots_data = json.load(f)
        
        if not bots_data:
            print("❌ Nenhum bot ativo")
            return
        
        print(f"🤖 Total de Bots: {len(bots_data)}")
        print()
        
        total_capital = Decimal("0")
        total_profit = Decimal("0")
        
        for i, bot in enumerate(bots_data, 1):
            name = bot['name']
            initial = Decimal(bot['initial_capital'])
            current = Decimal(bot['current_capital'])
            profit = current - initial
            profit_pct = (profit / initial * 100) if initial > 0 else 0
            status = bot['status']
            strategy = bot.get('strategy_name', 'N/A')
            
            total_capital += current
            total_profit += profit
            
            # Status emoji
            status_emoji = "🟢" if status == "ACTIVE" else "🔴" if status == "ERROR" else "🟡"
            
            # Profit emoji
            if profit > 0:
                profit_emoji = "📈"
                profit_color = "+"
            elif profit < 0:
                profit_emoji = "📉"
                profit_color = ""
            else:
                profit_emoji = "➖"
                profit_color = ""
            
            print(f"{i}. {status_emoji} {name}")
            print(f"   💰 Capital: ${initial} → ${current}")
            print(f"   {profit_emoji} P&L: {profit_color}${profit} ({profit_color}{profit_pct:.2f}%)")
            print(f"   📊 Status: {status}")
            print(f"   🎯 Estratégia: {strategy}")
            print()
        
        # Resumo geral
        total_profit_pct = (total_profit / sum(Decimal(b['initial_capital']) for b in bots_data) * 100) if bots_data else 0
        
        print("=" * 60)
        print("📈 RESUMO GERAL")
        print("=" * 60)
        print(f"💰 Capital Total: ${total_capital}")
        print(f"📊 P&L Total: ${total_profit} ({total_profit_pct:.2f}%)")
        print(f"🤖 Bots Ativos: {len([b for b in bots_data if b['status'] == 'ACTIVE'])}")
        print(f"🛑 Bots Parados: {len([b for b in bots_data if b['status'] == 'IDLE'])}")
        
        # Performance hoje (simulado - você pode implementar com dados reais)
        print()
        print("📅 PERFORMANCE HOJE")
        print("-" * 30)
        print("🔄 Trades: 0")
        print("💹 Volume: $0.00")
        print("⏱️ Última atividade: Aguardando sinais...")
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")

if __name__ == "__main__":
    show_performance()