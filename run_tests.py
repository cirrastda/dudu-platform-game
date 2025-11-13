#!/usr/bin/env python3
import sys
import subprocess


def main():
    try:
        import pytest  # noqa: F401
    except ImportError:
        print("❌ pytest não está instalado. Instale com: pip install -r requirements.txt")
        return 1

    cmd = [sys.executable, "-m", "pytest", "-q"]
    print("▶️  Executando todos os testes com pytest...")
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())