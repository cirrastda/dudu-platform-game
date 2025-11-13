import types

import pytest


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    @property
    def top(self):
        return self.y
    @property
    def bottom(self):
        return self.y + self.height
    @property
    def left(self):
        return self.x
    @property
    def right(self):
        return self.x + self.width


class FakeDraw:
    rect_calls = []

    @staticmethod
    def rect(screen, color, rect_or_tuple):
        FakeDraw.rect_calls.append((screen, color, rect_or_tuple))


class FakeScreen:
    def __init__(self):
        self.blit_calls = []
    def blit(self, img, pos):
        self.blit_calls.append((img, pos))


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    import pygame
    monkeypatch.setattr(pygame, "Rect", FakeRect, raising=True)
    monkeypatch.setattr(pygame, "draw", FakeDraw, raising=True)


def test_boss_alien_update_draw_initial_run_and_jump_trigger(monkeypatch):
    from internal.resources.enemies.boss_alien import BossAlien

    # Minimal platform map with a single platform under the boss
    platforms = [(0, 300, 400, 20)]

    screen = FakeScreen()

    # Create boss with no images to hit fallback drawing
    b = BossAlien(100, 300 - 60, platforms, boss_images=None)

    # Initial state: running
    assert b.state in ("run", "running")

    # Update several ticks; ensure draw works and rect called
    FakeDraw.rect_calls.clear()
    for _ in range(5):
        b.update(player_x=b.x - 50, camera_x=0)
        b.draw(screen)
    assert len(FakeDraw.rect_calls) >= 1

    # Force a jump trigger via helper to avoid complex timing
    b.jump()
    prev_y = b.y
    b.update(player_x=b.x, camera_x=0)
    # y should change due to jump physics progression
    assert b.y != prev_y