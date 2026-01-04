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
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    return os.path.join(base_path, relative_path)


# Função para carregar configurações do arquivo .env
def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {"environment": "production", "fullscreen": True, "window_scale": 1.25}

    try:
        # Em executável congelado (onefile/onedir), ignorar .env para não depender de arquivo externo
        # e garantir modo production por padrão.
        if not getattr(sys, "frozen", False):
            env_path = resource_path(".env")
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao carregar .env: {e}")

    # Overrides por variáveis de ambiente (úteis para testes/headless)
    try:
        env_override = os.environ.get("PLATFORM_GAME_ENV")
        if env_override:
            config["environment"] = env_override.strip()

        fullscreen_env = os.environ.get("PLATFORM_GAME_FULLSCREEN")
        if fullscreen_env is not None:
            val = fullscreen_env.strip().lower()
            config["fullscreen"] = val in {"1", "true", "yes", "on"}

        initial_stage_env = os.environ.get("PLATFORM_GAME_INITIAL_STAGE")
        if initial_stage_env:
            config["initial-stage"] = initial_stage_env.strip()

        difficulty_env = os.environ.get("PLATFORM_GAME_DIFFICULTY")
        if difficulty_env:
            config["difficulty"] = difficulty_env.strip()
    except Exception:
        # Não interromper caso variáveis estejam malformadas
        pass

    return config
