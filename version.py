#!/usr/bin/env python3
"""
Configuração de versão do Jump and Hit
"""

# Informações da versão
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_PATCH = 3
VERSION_STAGE = "alpha"  # alpha, beta, rc, stable
VERSION_BUILD = 1

# Versão completa
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
VERSION_FULL = f"{VERSION}-{VERSION_STAGE}.{VERSION_BUILD}"

# Informações do jogo
GAME_NAME = "Jump and Hit"
GAME_TITLE = "Jump and Hit"
GAME_DESCRIPTION = "Um jogo de plataforma 2D desenvolvido em Python com Pygame"
AUTHOR = "CirrasTec"
COPYRIGHT = "© 2025"

# Configurações de build
BUILD_PLATFORMS = ["windows", "linux", "macos"]
SUPPORTED_ARCHITECTURES = ["x64", "arm64"]

# Requisitos mínimos do sistema
MIN_PYTHON_VERSION = "3.8"
REQUIRED_PYGAME_VERSION = "2.5.2"


def get_version_info():
    """Retorna informações completas da versão"""
    return {
        "version": VERSION,
        "version_full": VERSION_FULL,
        "major": VERSION_MAJOR,
        "minor": VERSION_MINOR,
        "patch": VERSION_PATCH,
        "stage": VERSION_STAGE,
        "build": VERSION_BUILD,
        "game_name": GAME_NAME,
        "game_title": GAME_TITLE,
        "description": GAME_DESCRIPTION,
        "author": AUTHOR,
        "copyright": COPYRIGHT,
    }


def get_version_string():
    """Retorna string da versão para exibição"""
    return VERSION_FULL


def is_alpha():
    """Verifica se é versão alpha"""
    return VERSION_STAGE == "alpha"


def is_beta():
    """Verifica se é versão beta"""
    return VERSION_STAGE == "beta"


def is_stable():
    """Verifica se é versão estável"""
    return VERSION_STAGE == "stable"


if __name__ == "__main__":
    print(f"Versão: {get_version_string()}")
    print(f"Jogo: {GAME_TITLE}")
    print(f"Descrição: {GAME_DESCRIPTION}")
    print(f"Autor: {AUTHOR}")
    print(f"Copyright: {COPYRIGHT}")
