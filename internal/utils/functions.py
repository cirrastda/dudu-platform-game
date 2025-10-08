import sys
import os


def resource_path(relative_path):
    """Obter caminho absoluto para recursos, funciona para dev e PyInstaller"""
    try:
        # PyInstaller cria uma pasta temporária e armazena
        # o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Modo desenvolvimento - usar diretório atual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Função para carregar configurações do arquivo .env
def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {"environment": "production"}  # Valor padrão

    try:
        env_path = resource_path(".env")
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        # Se o arquivo .env não existir, usar valores padrão
        pass
    except Exception as e:
        print(f"Erro ao carregar .env: {e}")

    return config
