#!/usr/bin/env python3
"""
XBot v2 - Launcher Script
Script de inicialização que configura os paths corretamente
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório src ao Python path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

def main():
    """Função principal de inicialização"""
    print("🚀 XBot v2 - Trading Bot System")
    print("=" * 50)
    
    try:
        # Agora podemos importar os módulos corretamente
        from infrastructure.config import XBotConfig
        from main import main as xbot_main
        
        print("✅ Módulos carregados com sucesso")
        print("🔧 Inicializando XBot v2...")
        
        # Executar a função principal do XBot
        xbot_main()
        
    except Exception as e:
        print(f"❌ Erro ao inicializar XBot v2: {e}")
        print("\n💡 Dicas:")
        print("   1. Verifique se todas as dependências estão instaladas")
        print("   2. Configure o arquivo .env com suas credenciais")
        print("   3. Execute: pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)