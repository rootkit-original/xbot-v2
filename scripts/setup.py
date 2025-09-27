#!/usr/bin/env python3
"""
XBot v2 - Quick Start Setup Script

Este script facilita a configuração inicial do XBot v2.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Imprime banner do XBot v2"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        XBot v2                               ║
    ║              Sistema Completo de Trading Bot                 ║
    ║                                                              ║
    ║  🚀 Detecção de Padrões Avançada                            ║
    ║  🛡️  Análise de Risco Sofisticada                           ║
    ║  📊 Compliance e Auditoria                                   ║
    ║  📱 Notificações Telegram                                    ║
    ║  🏗️  Clean Architecture                                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"Versão atual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        'data',
        'logs',
        'backups',
        'market_data',
        'audit_logs'
    ]
    
    print("\n📁 Criando diretórios...")
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")

def setup_virtual_environment():
    """Configura ambiente virtual"""
    print("\n🐍 Configurando ambiente virtual...")
    
    if not Path("venv").exists():
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("   ✅ Ambiente virtual criado")
    else:
        print("   ✅ Ambiente virtual já existe")
    
    # Instruções para ativação
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        activate_script = "source venv/bin/activate"
    
    print(f"   📌 Para ativar: {activate_script}")

def install_dependencies():
    """Instala dependências"""
    print("\n📦 Instalando dependências...")
    
    try:
        # Verifica se está em ambiente virtual
        pip_executable = "venv/Scripts/pip" if os.name == 'nt' else "venv/bin/pip"
        
        if not Path(pip_executable).exists():
            pip_executable = "pip"
        
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("   ✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao instalar dependências: {e}")
        print("   📌 Tente instalar manualmente: pip install -r requirements.txt")

def setup_config_file():
    """Configura arquivo de configuração"""
    print("\n⚙️  Configurando arquivo de ambiente...")
    
    env_file = Path(".env")
    example_file = Path(".env.example")
    
    if not env_file.exists() and example_file.exists():
        # Copia arquivo de exemplo
        with open(example_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Arquivo .env criado a partir do exemplo")
        print("   ⚠️  IMPORTANTE: Configure suas credenciais no arquivo .env")
    else:
        print("   ✅ Arquivo .env já existe")

def test_installation():
    """Testa a instalação"""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testa import principal
        sys.path.insert(0, '.')
        from src.main import XBotApplication
        print("   ✅ Imports principais funcionando")
        
        # Testa configuração
        from src.infrastructure.config import XBotConfig
        config = XBotConfig()
        print("   ✅ Sistema de configuração funcionando")
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False
    
    return True

def show_next_steps():
    """Mostra próximos passos"""
    steps = """
📋 PRÓXIMOS PASSOS:

1. 📝 Configure suas credenciais:
   - Edite o arquivo .env
   - Configure BINANCE_API_KEY e BINANCE_SECRET_KEY
   - (Opcional) Configure Telegram para notificações

2. 🎯 Teste no Testnet primeiro:
   - Mantenha BINANCE_TESTNET=true
   - Obtenha credenciais de teste em: https://testnet.binance.vision/

3. 🚀 Execute sua primeira simulação:
   python src/main.py create-bot "MeuPrimeiroBot" --capital 1000
   python src/main.py list-bots
   python src/main.py start-bot <bot-id> --dry-run

4. 📊 Monitore via dashboard:
   python src/main.py dashboard

5. 📖 Consulte a documentação:
   - Leia o README.md para detalhes completos
   - Veja exemplos de uso na documentação

⚠️  LEMBRE-SE:
- Sempre teste estratégias no testnet primeiro
- Nunca arrisque mais do que pode perder  
- Monitore seus bots constantemente
- Mantenha backups das configurações

🎉 Instalação concluída com sucesso!
"""
    print(steps)

def main():
    """Função principal"""
    print_banner()
    
    try:
        check_python_version()
        create_directories()
        setup_virtual_environment()
        install_dependencies()
        setup_config_file()
        
        if test_installation():
            print("\n✅ Instalação completada com sucesso!")
            show_next_steps()
        else:
            print("\n❌ Instalação completada com erros.")
            print("Verifique os logs acima e tente resolver os problemas.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Instalação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante instalação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()