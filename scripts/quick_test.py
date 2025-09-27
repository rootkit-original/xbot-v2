#!/usr/bin/env python3
"""
XBot v2 - Quick Setup and Test Runner
Ferramentas para configurar e testar o XBot v2
"""

import os
import sys
import subprocess
from pathlib import Path

def print_status(message, status="INFO"):
    """Mostra status formatado"""
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def check_environment():
    """Verifica se o ambiente está configurado"""
    print_status("Verificando ambiente de desenvolvimento...")
    
    # Verificar Python
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor} OK", "SUCCESS")
    else:
        print_status("Python 3.8+ necessário", "ERROR")
        return False
    
    # Verificar venv
    venv_path = Path("venv")
    if venv_path.exists():
        print_status("Ambiente virtual encontrado", "SUCCESS")
    else:
        print_status("Ambiente virtual não encontrado", "WARNING")
    
    # Verificar dependências principais
    try:
        import requests
        import pandas
        import numpy
        import ccxt
        print_status("Dependências principais instaladas", "SUCCESS")
    except ImportError as e:
        print_status(f"Dependências faltando: {e}", "ERROR")
        return False
    
    return True

def create_simple_test():
    """Cria um teste simples para verificar instalação"""
    test_content = '''"""
Teste básico para verificar se o XBot v2 está funcionando
"""

import sys
import os
from pathlib import Path

# Adiciona src ao path para importações
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

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
        from domain import entities
        from domain import interfaces
        print("✅ Domain layer OK")
        
        from infrastructure import config
        print("✅ Infrastructure layer OK")
        
        from application import use_cases
        print("✅ Application layer OK")
        
        print("\\n🎉 Todos os testes passaram!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_basic_functionality():
    """Testa funcionalidades básicas"""
    print("\\n🔧 Testando funcionalidades básicas...")
    
    try:
        # Testa configuração
        from infrastructure.config import Settings
        settings = Settings()
        print("✅ Configurações carregadas")
        
        print("\\n📊 Status do ambiente:")
        print(f"   - Python: {sys.version.split()[0]}")
        print(f"   - Working Directory: {os.getcwd()}")
        print(f"   - Source Path: {src_path}")
        
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
    
    print("\\n" + "=" * 60)
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
'''
    
    test_path = Path("test_installation.py")
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print_status("Teste de instalação criado: test_installation.py", "SUCCESS")

def fix_imports():
    """Corrige problemas de importação comuns"""
    print_status("Corrigindo estrutura de importações...")
    
    # Criar __init__.py se necessário
    init_files = [
        "src/__init__.py",
        "src/domain/__init__.py",
        "src/application/__init__.py",
        "src/infrastructure/__init__.py",
        "src/strategies/__init__.py"
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        if not init_path.exists():
            with open(init_path, "w", encoding="utf-8") as f:
                f.write('"""XBot v2 module"""\\n')
            print_status(f"Criado: {init_file}", "SUCCESS")
    
    print_status("Estrutura de importações corrigida", "SUCCESS")

def run_simple_test():
    """Executa teste simples"""
    print_status("Executando teste de instalação...")
    
    try:
        result = subprocess.run([sys.executable, "test_installation.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Erros:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except Exception as e:
        print_status(f"Erro ao executar teste: {e}", "ERROR")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 XBot v2 - Quick Setup & Test")
    print("=" * 60)
    
    if not check_environment():
        print_status("Ambiente não configurado corretamente", "ERROR")
        return
    
    fix_imports()
    create_simple_test()
    
    print("\\n" + "=" * 60)
    print("🧪 Executando testes...")
    print("=" * 60)
    
    success = run_simple_test()
    
    if success:
        print_status("\\nSetup e testes concluídos com sucesso!", "SUCCESS")
        print("\\n📋 Comandos úteis:")
        print("   • python test_installation.py  - Testar instalação")
        print("   • python setup.py             - Setup completo")
        print("   • Ctrl+Shift+P → 'Tasks: Run Task' - VS Code tasks")
    else:
        print_status("\\nAlguns problemas encontrados", "WARNING")
        print("💡 Verifique os erros acima e corrija conforme necessário")

if __name__ == "__main__":
    main()