import pygame

from internal.resources.flag import Flag
from internal.resources.extra_life import ExtraLife


def test_flag_rect_and_fallback_image(monkeypatch):
    # Forçar falha no carregamento da imagem para acionar fallback
    def raise_error(_):
        raise pygame.error("no image")

    monkeypatch.setattr(pygame.image, "load", raise_error)

    flag = Flag(100, 200)

    # Dimensões padrão
    assert flag.width == 20
    assert flag.height == 100
    assert flag.flag_width == 60
    assert flag.flag_height == 40

    # Retângulo cobre mastro + bandeira
    assert flag.rect.topleft == (100, 200)
    assert flag.rect.width == flag.width + flag.flag_width
    assert flag.rect.height == flag.height

    # Fallback: sem imagem quando pygame.image.load falha com pygame.error
    assert getattr(flag, "flag_image", None) is None


def test_flag_image_loaded_and_scaled(monkeypatch):
    # Simular imagem carregada
    loaded_surface = pygame.Surface((10, 10))
    monkeypatch.setattr(pygame.image, "load", lambda path: loaded_surface)

    # Interceptar scale para verificar dimensões de saída
    called = {}

    def fake_scale(surface, size):
        called["size"] = size
        return pygame.Surface(size)

    monkeypatch.setattr(pygame.transform, "scale", fake_scale)

    flag = Flag(0, 0)
    total_width = flag.width + flag.flag_width

    assert flag.flag_image.get_size() == (total_width, flag.height)
    assert called["size"] == (total_width, flag.height)


def test_extra_life_with_provided_image_sets_rect():
    img = pygame.Surface((24, 24), pygame.SRCALPHA)
    item = ExtraLife(50, 60, image=img)

    assert item.image is img
    assert item.rect.topleft == (50, 60)
    assert item.rect.size == (24, 24)


def test_extra_life_without_image_uses_circle_fallback(monkeypatch):
    # Forçar exceção para cair no fallback de círculo
    def raise_any(_):
        raise Exception("file not found")

    monkeypatch.setattr(pygame.image, "load", raise_any)

    item = ExtraLife(10, 20, image=None, size=(30, 20))

    assert isinstance(item.image, pygame.Surface)
    assert item.image.get_size() == (30, 20)
    assert item.rect.topleft == (10, 20)
    assert item.rect.size == (30, 20)