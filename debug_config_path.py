import os
from pathlib import Path
from dotenv import load_dotenv

# O mesmo caminho usado no config.py
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

print(f"Arquivo atual: {__file__}")
print(f"Parent: {Path(__file__).parent}")
print(f"Parent.parent: {Path(__file__).parent.parent}")  
print(f"Project root (parent.parent.parent): {project_root}")
print(f"Procurando .env em: {env_path}")
print(f"Arquivo .env existe: {env_path.exists()}")

load_dotenv(env_path)

print(f"BINANCE_API_KEY: {bool(os.getenv('BINANCE_API_KEY'))}")
print(f"BINANCE_SECRET_KEY: {bool(os.getenv('BINANCE_SECRET_KEY'))}")