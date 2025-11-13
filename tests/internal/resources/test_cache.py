import types

import pytest


class FakeSurface:
    def __init__(self):
        self.scaled_to = None


class FakeTransform:
    @staticmethod
    def scale(surface, size):
        surface.scaled_to = size
        return surface


class FakePygameError(Exception):
    pass


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    import pygame
    monkeypatch.setattr(pygame, "transform", FakeTransform, raising=True)
    monkeypatch.setattr(pygame, "error", FakePygameError, raising=True)

    # Stable resource_path for tests
    from internal.utils import functions
    monkeypatch.setattr(functions, "resource_path", lambda p: f"/fake/{p}", raising=True)


def test_get_image_caching(monkeypatch):
    import pygame
    from internal.resources.cache import ResourceCache

    # Load returns a simple surface
    monkeypatch.setattr(pygame.image, "load", lambda p: FakeSurface(), raising=True)

    cache = ResourceCache()
    cache.clear_cache()
    cache.cache_hits = 0
    cache.cache_misses = 0

    img1 = cache.get_image("imagens/fundo3.png", (100, 80))
    img2 = cache.get_image("imagens/fundo3.png", (100, 80))

    assert img1 is img2
    assert isinstance(img1, FakeSurface)
    assert img1.scaled_to == (100, 80)

    stats = cache.get_cache_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["images_cached"] == 1
    assert 0 < stats["hit_rate"] <= 100


def test_get_image_failure_returns_none(monkeypatch):
    import pygame
    from internal.resources.cache import ResourceCache

    def fail_load(path):
        raise FakePygameError("fail")

    monkeypatch.setattr(pygame.image, "load", fail_load, raising=True)

    cache = ResourceCache()
    cache.clear_cache()
    img = cache.get_image("imagens/does-not-exist.png")
    assert img is None