#!/usr/bin/env python3
import os
import sys
from pathlib import Path

print("=== Antes de importar config ===")
print(f"BINANCE_API_KEY: {bool(os.getenv('BINANCE_API_KEY'))}")
print(f"BINANCE_SECRET_KEY: {bool(os.getenv('BINANCE_SECRET_KEY'))}")

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("\n=== Importando config ===")
from infrastructure.config import XBotConfig

print(f"BINANCE_API_KEY após import: {bool(os.getenv('BINANCE_API_KEY'))}")
print(f"BINANCE_SECRET_KEY após import: {bool(os.getenv('BINANCE_SECRET_KEY'))}")

print("\n=== Instanciando config ===")
config = XBotConfig()

print(f"config.binance.api_key: {bool(config.binance.api_key)}")
print(f"config.binance.api_secret: {bool(config.binance.api_secret)}")

print("\n=== Testando os.getenv diretamente ===")
print(f"os.getenv('BINANCE_API_KEY'): {repr(os.getenv('BINANCE_API_KEY'))}")
print(f"os.getenv('BINANCE_SECRET_KEY'): {repr(os.getenv('BINANCE_SECRET_KEY'))}")

print("\n=== Forçando reload do .env ===")
from dotenv import load_dotenv
env_path = Path('.env')
if env_path.exists():
    result = load_dotenv(env_path, override=True)
    print(f"load_dotenv resultado: {result}")
    print(f"BINANCE_API_KEY após reload: {bool(os.getenv('BINANCE_API_KEY'))}")
    print(f"BINANCE_SECRET_KEY após reload: {bool(os.getenv('BINANCE_SECRET_KEY'))}")
    
    # Criar novo config após reload
    config2 = XBotConfig()
    print(f"config2.binance.api_key: {bool(config2.binance.api_key)}")
    print(f"config2.binance.api_secret: {bool(config2.binance.api_secret)}")