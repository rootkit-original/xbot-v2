import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env da raiz do projeto
project_root = Path(__file__).parent
env_path = project_root / '.env'

print(f"Procurando .env em: {env_path}")
print(f"Arquivo .env existe: {env_path.exists()}")

load_dotenv(env_path)

print(f"BINANCE_API_KEY: {bool(os.getenv('BINANCE_API_KEY'))}")
print(f"BINANCE_SECRET_KEY: {bool(os.getenv('BINANCE_SECRET_KEY'))}")
print(f"BINANCE_TESTNET: {os.getenv('BINANCE_TESTNET')}")

# Testar diretamente do arquivo
if env_path.exists():
    with open(env_path, 'r') as f:
        content = f.read()
    print("\nConteúdo do .env:")
    for i, line in enumerate(content.split('\n')[:10], 1):
        if line.strip() and not line.startswith('#'):
            if 'BINANCE' in line:
                key = line.split('=')[0]
                print(f"  Linha {i}: {key}=***")
            else:
                print(f"  Linha {i}: {line}")