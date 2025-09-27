"""
Teste básico para verificar se o XBot v2 está funcionando
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Testa importações básicas"""
    try:
        print("🧪 Testando importações...")
        
        # Testa importações básicas
        import requests
        import pandas as pd
        import numpy as np
        import ccxt
        print("✅ Bibliotecas externas OK")
        
        # Testa estrutura do projeto
        from src.domain import entities
        from src.domain import interfaces
        print("✅ Domain layer OK")
        
        from src.infrastructure import config
        print("✅ Infrastructure layer OK")
        
        from src.application import use_cases
        print("✅ Application layer OK")
        
        print("\n🎉 Todos os testes passaram!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_basic_functionality():
    """Testa funcionalidades básicas"""
    print("\n🔧 Testando funcionalidades básicas...")
    
    try:
        # Testa configuração
        from src.infrastructure.config import XBotConfig
        config = XBotConfig()
        print("✅ Configurações carregadas")
        
        print("\n📊 Status do ambiente:")
        print(f"   - Python: {sys.version.split()[0]}")
        print(f"   - Working Directory: {os.getcwd()}")
        print(f"   - Project Root: {project_root}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar funcionalidades: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 XBot v2 - Teste de Instalação")
    print("=" * 60)
    
    success = True
    
    success = success and test_imports()
    success = success and test_basic_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCESSO: XBot v2 está pronto para uso!")
        print("📋 Próximos passos:")
        print("   1. Configure suas credenciais no arquivo .env")
        print("   2. Execute: python -m src.main")
        print("   3. Ou use as VS Code tasks (Ctrl+Shift+P)")
    else:
        print("❌ FALHA: Corrija os problemas acima")
        print("💡 Tente executar o setup.py novamente")
    
    print("=" * 60)
