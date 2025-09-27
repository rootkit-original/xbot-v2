import os
from pathlib import Path
from dotenv import load_dotenv

print("=== Teste de carregamento .env ===")

# Carrega .env da raiz do projeto (como no config.py)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

print(f"Arquivo: {__file__}")
print(f"Project root calculado: {project_root}")
print(f"Caminho .env: {env_path}")
print(f"Arquivo .env existe: {env_path.exists()}")

if env_path.exists():
    print(f"Carregando .env de: {env_path}")
    result = load_dotenv(env_path)
    print(f"load_dotenv resultado: {result}")
    
    print(f"BINANCE_API_KEY após load_dotenv: {bool(os.getenv('BINANCE_API_KEY'))}")
    print(f"BINANCE_SECRET_KEY após load_dotenv: {bool(os.getenv('BINANCE_SECRET_KEY'))}")
    
    # Verificar o conteúdo do arquivo
    with open(env_path, 'r') as f:
        lines = f.read().split('\n')
    
    print(f"\nPrimeiras linhas do .env:")
    for i, line in enumerate(lines[:10], 1):
        if line.strip() and not line.startswith('#'):
            key = line.split('=')[0] if '=' in line else line
            print(f"  Linha {i}: {key}")
else:
    print("❌ Arquivo .env não encontrado!")

print("\n=== Testando do diretório atual ===")
current_env = Path('.env')
print(f"Arquivo .env no dir atual: {current_env.exists()}")
if current_env.exists():
    result2 = load_dotenv(current_env)
    print(f"load_dotenv resultado (atual): {result2}")
    print(f"BINANCE_API_KEY após load_dotenv atual: {bool(os.getenv('BINANCE_API_KEY'))}")
    print(f"BINANCE_SECRET_KEY após load_dotenv atual: {bool(os.getenv('BINANCE_SECRET_KEY'))}")