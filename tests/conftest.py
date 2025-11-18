import os
import pytest
import pygame


def pytest_configure(config):
    # Forçar ambiente de desenvolvimento e headless durante testes
    os.environ.setdefault("PLATFORM_GAME_ENV", "development")
    os.environ.setdefault("PLATFORM_GAME_FULLSCREEN", "0")
    # Usar driver dummy para não abrir/janela real
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture(autouse=True)
def headless_display():
    """Inicializa pygame com display mínimo para evitar alterações de resolução."""
    try:
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        # Janela mínima em modo dummy
        pygame.display.set_mode((1, 1))
    except Exception:
        # Em alguns ambientes, o driver dummy pode não suportar set_mode.
        # Ignorar silenciosamente para não falhar a suíte inteira.
        pass
    yield
    try:
        if pygame.display.get_init():
            pygame.display.quit()
    except Exception:
        pass


@pytest.fixture(autouse=True)
def disable_audio(monkeypatch):
    """Desabilita inicialização do mixer para evitar uso de hardware de áudio."""
    try:
        from internal.engine.sound.mixer import Mixer
        monkeypatch.setattr(Mixer, "init", lambda *_, **__: None)
    except Exception:
        # Se módulo não existir/for diferente em alguns testes, ignore.
        pass