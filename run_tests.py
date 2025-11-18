#!/usr/bin/env python3
import sys
import subprocess


def main():
    try:
        import pytest  # noqa: F401
    except ImportError:
        print("❌ pytest não está instalado. Instale com: pip install -r requirements.txt")
        return 1

    # Configurar ambiente headless e desenvolvimento para evitar travamentos
    env = dict(**os.environ)
    env.setdefault("PLATFORM_GAME_ENV", "development")
    env.setdefault("PLATFORM_GAME_FULLSCREEN", "0")
    env.setdefault("SDL_VIDEODRIVER", "dummy")

    cmd = [sys.executable, "-m", "pytest", "-q"]
    print("▶️  Executando todos os testes com pytest...")
    result = subprocess.run(cmd, env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())