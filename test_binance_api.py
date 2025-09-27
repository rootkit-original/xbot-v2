#!/usr/bin/env python3
"""
Teste direto da API da Binance com credenciais reais
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

# Carregar variáveis de ambiente
load_dotenv()

def test_binance_connection():
    """Testa conexão direta com a API da Binance"""
    
    print("🧪 Testando conexão com API da Binance...")
    print("=" * 50)
    
    # Obter credenciais
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_SECRET_KEY')
    testnet = os.getenv('BINANCE_TESTNET', 'false').lower() == 'true'
    
    print(f"📋 API Key: {'✅ Configurada' if api_key else '❌ Não encontrada'}")
    print(f"🔑 Secret Key: {'✅ Configurada' if api_secret else '❌ Não encontrada'}")
    print(f"🧪 Testnet: {'✅ Ativo' if testnet else '❌ Desativo (Produção)'}")
    
    if not api_key or not api_secret:
        print("\n❌ Credenciais não encontradas no .env")
        return False
    
    # URLs da API
    if testnet:
        base_url = "https://testnet.binance.vision"
    else:
        base_url = "https://api.binance.com"
    
    print(f"🌐 URL Base: {base_url}")
    
    try:
        # Teste 1: Server Time (público)
        print("\n🕒 Testando Server Time...")
        response = requests.get(f"{base_url}/api/v3/time", timeout=10)
        if response.status_code == 200:
            print("✅ Server Time: OK")
        else:
            print(f"❌ Server Time: Erro {response.status_code}")
            return False
        
        # Teste 2: Account Info (privado)
        print("\n👤 Testando Account Info...")
        
        import hmac
        import hashlib
        import time
        
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        signature = hmac.new(
            api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-MBX-APIKEY': api_key
        }
        
        url = f"{base_url}/api/v3/account?{query_string}&signature={signature}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            account_data = response.json()
            print("✅ Account Info: OK")
            print(f"📊 Account Type: {account_data.get('accountType', 'N/A')}")
            print(f"💰 Balances: {len(account_data.get('balances', []))} assets")
            
            # Mostrar alguns balances não-zero
            balances = account_data.get('balances', [])
            non_zero_balances = [b for b in balances if float(b['free']) > 0 or float(b['locked']) > 0]
            
            if non_zero_balances:
                print("💵 Saldos não-zero:")
                for balance in non_zero_balances[:5]:  # Mostrar apenas os primeiros 5
                    free = float(balance['free'])
                    locked = float(balance['locked'])
                    if free > 0 or locked > 0:
                        print(f"   • {balance['asset']}: {free:.8f} (livre) + {locked:.8f} (bloqueado)")
            
            return True
            
        else:
            print(f"❌ Account Info: Erro {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_binance_connection()
    print("\n" + "=" * 50)
    if success:
        print("🎉 Teste concluído com sucesso!")
        print("✅ API da Binance está funcionando corretamente")
    else:
        print("💥 Teste falhou!")
        print("❌ Verifique suas credenciais e conexão")
    print("=" * 50)