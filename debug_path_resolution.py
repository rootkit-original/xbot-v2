from pathlib import Path

config_path = Path("src/infrastructure/config.py").resolve()
print(f"Config real: {config_path}")
print(f"Parent: {config_path.parent}")  # infrastructure
print(f"Parent.parent: {config_path.parent.parent}")  # src
print(f"Parent.parent.parent: {config_path.parent.parent.parent}")  # projeto

env_path = config_path.parent.parent.parent / '.env'
print(f"Env path: {env_path}")
print(f"Env exists: {env_path.exists()}")

# Verificar se há diferença quando executo de dentro da pasta src
import os
os.chdir("src")
config_path_from_src = Path("infrastructure/config.py").resolve()
print(f"\nExecutando de src:")
print(f"Config path: {config_path_from_src}")
print(f"Parent.parent.parent: {config_path_from_src.parent.parent.parent}")
env_from_src = config_path_from_src.parent.parent.parent / '.env'
print(f"Env path: {env_from_src}")
print(f"Env exists: {env_from_src.exists()}")