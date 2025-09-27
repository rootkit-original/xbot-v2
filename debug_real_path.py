# Simular o caminho real do arquivo config.py
from pathlib import Path

config_file_path = Path("src/infrastructure/config.py")
project_root = config_file_path.parent.parent.parent
env_path = project_root / '.env'

print(f"Config file: {config_file_path}")
print(f"Parent (infrastructure): {config_file_path.parent}")
print(f"Parent.parent (src): {config_file_path.parent.parent}")
print(f"Parent.parent.parent (project root): {project_root}")
print(f"Arquivo .env existe em {env_path}: {env_path.exists()}")

# Na verdade está correto, mas vamos testar o Path(__file__) real
print(f"\nCaminho real do arquivo config.py:")
real_config_path = Path("src/infrastructure/config.py").resolve()
print(f"Caminho absoluto: {real_config_path}")
print(f"Parent: {real_config_path.parent}")
print(f"Parent.parent: {real_config_path.parent.parent}") 
print(f"Parent.parent.parent: {real_config_path.parent.parent.parent}")