import types

import pytest


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class FakeSurface:
    def __init__(self):
        self.scaled_to = None


class FakeTransform:
    @staticmethod
    def scale(surface, size):
        surface.scaled_to = size
        return surface


class FakeDraw:
    rect_calls = []
    circle_calls = []

    @staticmethod
    def rect(screen, color, rect):
        FakeDraw.rect_calls.append((screen, color, rect))

    @staticmethod
    def circle(screen, color, center, radius):
        FakeDraw.circle_calls.append((screen, color, center, radius))


class FakeScreen:
    def __init__(self):
        self.blit_calls = []

    def blit(self, img, pos):
        self.blit_calls.append((img, pos))


class FakePygameError(Exception):
    pass


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    import pygame

    # Patch pygame primitives used by Spaceship
    monkeypatch.setattr(pygame, "Rect", FakeRect, raising=True)
    monkeypatch.setattr(pygame, "draw", FakeDraw, raising=True)
    monkeypatch.setattr(pygame, "transform", FakeTransform, raising=True)
    monkeypatch.setattr(pygame, "error", FakePygameError, raising=True)

    # Provide a deterministic resource_path
    from internal.utils import functions

    monkeypatch.setattr(functions, "resource_path", lambda p: f"/fake/{p}", raising=True)


def test_update_position_updates_rects(monkeypatch):
    # Ensure image.load does not fail for construction
    import pygame

    monkeypatch.setattr(pygame.image, "load", lambda p: FakeSurface(), raising=True)

    from internal.resources.spaceship import Spaceship

    s = Spaceship(10, 20)
    # Sanity preconditions
    assert s.rect.x == 10 and s.rect.y == 20
    assert s.abduction_rect.x == 10 and s.abduction_rect.y == 20

    s.update_position(100, 120)
    assert s.x == 100 and s.y == 120
    assert s.rect.x == 100 and s.rect.y == 120
    assert s.abduction_rect.x == 100 and s.abduction_rect.y == 120


def test_draw_with_image_blits(monkeypatch):
    import pygame

    def fake_load(path):
        return FakeSurface()

    monkeypatch.setattr(pygame.image, "load", fake_load, raising=True)

    from internal.resources.spaceship import Spaceship

    s = Spaceship(30, 40)
    screen = FakeScreen()
    s.draw(screen)

    # Should use blit when image is available
    assert len(screen.blit_calls) == 1
    img, pos = screen.blit_calls[0]
    assert isinstance(img, FakeSurface)
    assert pos == (30, 40)


def test_draw_without_image_fallback(monkeypatch):
    import pygame

    def fail_load(path):
        raise FakePygameError("fail")

    monkeypatch.setattr(pygame.image, "load", fail_load, raising=True)

    from internal.resources.spaceship import Spaceship

    FakeDraw.rect_calls.clear()
    FakeDraw.circle_calls.clear()

    s = Spaceship(5, 6)
    screen = FakeScreen()
    s.draw(screen)

    # Fallback should draw a rect and a circle
    assert len(FakeDraw.rect_calls) == 1
    assert len(FakeDraw.circle_calls) == 1