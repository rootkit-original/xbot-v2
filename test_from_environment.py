#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from infrastructure.config import XBotConfig

print("=== Testando from_environment ===")
config = XBotConfig.from_environment()

print(f"config.binance.api_key: {bool(config.binance.api_key)}")
print(f"config.binance.api_secret: {bool(config.binance.api_secret)}")
print(f"config.binance.testnet: {config.binance.testnet}")

print("\n=== Comparando com __init__ normal ===")
config2 = XBotConfig()
print(f"config2.binance.api_key: {bool(config2.binance.api_key)}")
print(f"config2.binance.api_secret: {bool(config2.binance.api_secret)}")
print(f"config2.binance.testnet: {config2.binance.testnet}")

print(f"\n=== Variáveis de ambiente ===")
print(f"BINANCE_API_KEY: {bool(os.getenv('BINANCE_API_KEY'))}")
print(f"BINANCE_SECRET_KEY: {bool(os.getenv('BINANCE_SECRET_KEY'))}")
print(f"BINANCE_TESTNET: {os.getenv('BINANCE_TESTNET')}")