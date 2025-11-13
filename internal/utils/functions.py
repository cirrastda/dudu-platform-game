import sys
import os


def resource_path(relative_path):
    """Obter caminho absoluto para recursos, funcionando em dev, onefile e onedir.

    - PyInstaller onefile: usa sys._MEIPASS (pasta temporária extraída)
    - PyInstaller onedir: usa o diretório do executável (sys.executable)
    - Desenvolvimento: usa a raiz do projeto baseada neste arquivo
    """
    try:
        # PyInstaller (onefile): pasta temporária
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        # Se estiver congelado (PyInstaller onedir), usar diretório do executável
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            # Modo desenvolvimento: raiz do projeto relativa a este arquivo
            base_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )

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
