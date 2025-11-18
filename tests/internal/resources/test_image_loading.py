import types

import internal.resources.image as image_mod
import internal.resources.cache as cache_mod
from internal.utils.constants import WIDTH, HEIGHT


class FakeSurface:
    def __init__(self, w=10, h=10):
        self._w = w
        self._h = h

    def get_width(self):
        return self._w

    def get_height(self):
        return self._h

    def get_rect(self):
        return types.SimpleNamespace(width=self._w, height=self._h)

    def get_size(self):
        return (self._w, self._h)


class FakeTransform:
    @staticmethod
    def scale(img, size):
        return FakeSurface(size[0], size[1])


def _install_fake_pygame(monkeypatch):
    # Provide minimal pygame API used by Image.load_images
    monkeypatch.setattr(
        image_mod,
        "pygame",
        types.SimpleNamespace(transform=FakeTransform, error=Exception),
        raising=False,
    )


def test_load_images_with_game_and_scaling(monkeypatch):
    _install_fake_pygame(monkeypatch)

    calls = []

    def fake_get_image(self, path, scale=None):
        calls.append((path, scale))
        # Shape sizes by path to trigger scaling branches
        if "logos/game.png" in path:
            base = FakeSurface(600, 400)
            if scale:
                return FakeSurface(scale[0], scale[1])
            return base
        if "imagens/logos/" in path:
            base = FakeSurface(500, 350)
            if scale:
                return FakeSurface(scale[0], scale[1])
            return base
        if "imagens/inimigos/fogo.png" in path:
            # Base fire image; scaled later via pygame.transform.scale
            return FakeSurface(60, 120)
        # Default: respect provided scale if any
        if scale:
            return FakeSurface(scale[0], scale[1])
        return FakeSurface(20, 10)

    monkeypatch.setattr(
        cache_mod.ResourceCache, "get_image", fake_get_image, raising=False
    )

    img = image_mod.Image()
    fake_game = types.SimpleNamespace(current_level=15)
    img.load_images(fake_game)

    # Background should use the updated level 11-16 background asset
    assert calls[0][0] == "imagens/bg/fase 2.png"
    assert calls[0][1] == (WIDTH, HEIGHT)
    assert isinstance(img.background_img, FakeSurface)

    # Logos list populated and scaled down to fit 400x300 box
    assert len(img.logos) == 3
    assert img.logos[0].get_width() == 400
    assert img.logos[0].get_height() == 280

    # Game main logo scaled to 300x200
    assert img.game_logo.get_width() == 300
    assert img.game_logo.get_height() == 200

    # Fire image keeps aspect ratio to target height 30
    assert img.fire_image.get_width() == 15
    assert img.fire_image.get_height() == 30


def test_load_images_without_game_sets_background_none(monkeypatch):
    _install_fake_pygame(monkeypatch)

    def fake_get_image(self, path, scale=None):
        if scale:
            return FakeSurface(scale[0], scale[1])
        return FakeSurface(22, 11)

    monkeypatch.setattr(
        cache_mod.ResourceCache, "get_image", fake_get_image, raising=False
    )

    img = image_mod.Image()
    img.load_images(None)

    assert img.background_img is None
    assert isinstance(img.menu_background_img, FakeSurface)


def test_load_images_error_fallback(monkeypatch):
    _install_fake_pygame(monkeypatch)

    # Make cache always raise pygame.error to trigger the outer fallback
    def raising_get_image(self, path, scale=None):
        raise image_mod.pygame.error("boom")

    monkeypatch.setattr(
        cache_mod.ResourceCache, "get_image", raising_get_image, raising=False
    )

    img = image_mod.Image()
    img.load_images(None)

    # Fallback sets critical assets to None
    assert img.background_img is None
    assert img.platform_texture is None
    assert img.bird_img1 is None
    assert img.bird_img2 is None
    assert img.bullet_img is None
    assert img.bullet_image is None
    assert img.explosion_img is None
    assert img.explosion_image is None
