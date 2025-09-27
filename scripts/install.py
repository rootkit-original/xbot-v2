#!/usr/bin/env python3
"""
XBot v2 - Professional Installation & Setup Script
Sistema moderno de configuração e instalação do ambiente de desenvolvimento
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Optional
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class XBotInstaller:
    """Classe principal para instalação e configuração do XBot v2"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_path = self.project_root / "venv"
        self.requirements_file = self.project_root / "requirements.txt"
        
    def print_header(self) -> None:
        """Mostra header profissional do setup"""
        print("=" * 70)
        print("🚀 XBot v2 - Professional Trading Bot System")
        print("=" * 70)
        print("📋 Automated Development Environment Setup")
        print("🏗️  Clean Architecture | 🧪 Full Test Coverage | 📊 Professional Grade")
        print("=" * 70)
        print()

    def check_system_requirements(self) -> bool:
        """Verifica requisitos do sistema"""
        logger.info("Checking system requirements...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            logger.error(f"Python 3.8+ required. Current: {version.major}.{version.minor}")
            return False
        
        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        
        # Check platform
        system = platform.system()
        logger.info(f"✅ Platform: {system} - {platform.release()}")
        
        return True

    def create_virtual_environment(self) -> bool:
        """Cria ambiente virtual otimizado"""
        logger.info("Setting up virtual environment...")
        
        if self.venv_path.exists():
            logger.info("✅ Virtual environment already exists")
            return True
        
        try:
            subprocess.run([
                sys.executable, "-m", "venv", str(self.venv_path),
                "--upgrade-deps"
            ], check=True, capture_output=True)
            
            logger.info("✅ Virtual environment created successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return False

    def get_python_executable(self) -> Path:
        """Retorna caminho do executável Python no venv"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        return self.venv_path / "bin" / "python"

    def install_dependencies(self) -> bool:
        """Instala todas as dependências com otimizações"""
        logger.info("Installing dependencies...")
        
        python_exe = self.get_python_executable()
        if not python_exe.exists():
            logger.error("Python executable not found in virtual environment")
            return False

        try:
            # Upgrade pip first
            logger.info("📦 Upgrading pip...")
            subprocess.run([
                str(python_exe), "-m", "pip", "install", 
                "--upgrade", "pip", "setuptools", "wheel"
            ], check=True, capture_output=True)

            # Install requirements
            if self.requirements_file.exists():
                logger.info("📦 Installing project dependencies...")
                subprocess.run([
                    str(python_exe), "-m", "pip", "install",
                    "-r", str(self.requirements_file)
                ], check=True, capture_output=True)
            
            # Install development dependencies
            dev_deps = [
                "pytest>=7.4.0",
                "pytest-cov>=4.1.0",
                "pytest-asyncio>=0.21.0",
                "pytest-mock>=3.11.0",
                "coverage[toml]>=7.3.0",
                "flake8>=6.0.0",
                "black>=23.0.0",
                "mypy>=1.5.0",
                "pre-commit>=3.4.0"
            ]
            
            logger.info("📦 Installing development dependencies...")
            subprocess.run([
                str(python_exe), "-m", "pip", "install"
            ] + dev_deps, check=True, capture_output=True)
            
            logger.info("✅ All dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False

    def create_project_structure(self) -> None:
        """Cria estrutura completa de diretórios"""
        logger.info("Creating project structure...")
        
        directories = [
            "logs",
            "data",
            "backups",
            "config",
            "tests/unit",
            "tests/integration",
            "tests/fixtures",
            "examples/basic",
            "examples/advanced",
            "examples/configurations",
            "scripts",
            ".coverage_reports"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ Project structure created")

    def setup_configuration_files(self) -> None:
        """Configura arquivos de configuração profissionais"""
        logger.info("Setting up configuration files...")
        
        # pytest.ini
        pytest_config = """[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html:.coverage_reports/html
    --cov-report=xml:.coverage_reports/coverage.xml
    --cov-report=term-missing
    --cov-fail-under=100
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
"""
        
        with open(self.project_root / "pytest.ini", "w") as f:
            f.write(pytest_config)
        
        # .coveragerc
        coverage_config = """[run]
source = src
omit = 
    */tests/*
    */venv/*
    */scripts/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[html]
directory = .coverage_reports/html
"""
        
        with open(self.project_root / ".coveragerc", "w") as f:
            f.write(coverage_config)
            
        logger.info("✅ Configuration files created")

    def run_validation_tests(self) -> bool:
        """Executa testes de validação da instalação"""
        logger.info("Running validation tests...")
        
        python_exe = self.get_python_executable()
        
        try:
            # Test basic imports
            test_script = """
import sys
sys.path.insert(0, 'src')
try:
    import domain.entities
    import infrastructure.config
    import application.use_cases
    print('✅ All modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"""
            
            result = subprocess.run([
                str(python_exe), "-c", test_script
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Validation tests passed")
                return True
            else:
                logger.error(f"Validation tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running validation tests: {e}")
            return False

    def print_next_steps(self) -> None:
        """Mostra próximos passos profissionais"""
        print("\n" + "=" * 70)
        print("🎉 XBot v2 - Installation Complete!")
        print("=" * 70)
        print()
        print("📋 Next Steps:")
        print("   1. Configure your API credentials in .env file")
        print("   2. Run tests: python -m pytest")
        print("   3. Check coverage: python -m pytest --cov")
        print("   4. Start development with VS Code tasks")
        print()
        print("🔧 Available Scripts:")
        print("   scripts/test_installation.py  - Validate installation")
        print("   scripts/run_development.py    - Development mode")
        print("   python -m src.main            - Run XBot v2")
        print()
        print("📊 Quality Assurance:")
        print("   python -m flake8 src tests    - Code linting")
        print("   python -m black src tests     - Code formatting")
        print("   python -m mypy src            - Type checking")
        print()
        print("🧪 Testing Framework:")
        print("   python -m pytest tests/unit         - Unit tests")
        print("   python -m pytest tests/integration  - Integration tests")
        print("   python -m pytest --cov-report=html  - HTML coverage report")
        print()

    def install(self) -> int:
        """Executa instalação completa"""
        self.print_header()
        
        if not self.check_system_requirements():
            return 1
            
        if not self.create_virtual_environment():
            return 1
            
        if not self.install_dependencies():
            return 1
            
        self.create_project_structure()
        self.setup_configuration_files()
        
        if not self.run_validation_tests():
            logger.warning("Some validation tests failed, but installation completed")
            
        self.print_next_steps()
        return 0


def main():
    """Função principal"""
    installer = XBotInstaller()
    return installer.install()


if __name__ == "__main__":
    sys.exit(main())