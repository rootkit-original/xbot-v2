import sys
from pathlib import Path

# Adiciona src ao path (como no config.py)
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importa e testa config
from infrastructure.config import XBotConfig

config = XBotConfig()
print(f'API Key loaded: {bool(config.binance.api_key)}')
print(f'API Key length: {len(config.binance.api_key) if config.binance.api_key else 0}')
print(f'Secret Key loaded: {bool(config.binance.api_secret)}')
print(f'Secret Key length: {len(config.binance.api_secret) if config.binance.api_secret else 0}')
print(f'Testnet: {config.binance.testnet}')