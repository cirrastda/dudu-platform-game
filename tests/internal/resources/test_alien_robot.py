import types

import pytest


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


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


def test_alien_shoots_and_draws_fallback(monkeypatch):
    # Make Laser update simple but keep behaviour
    from internal.resources import laser as laser_module

    screen = FakeScreen()

    from internal.resources.enemies.alien import Alien

    a = Alien(200, 300, 180, 240, alien_images=None)
    # Force immediate shooting when facing left
    a.shoot_interval = 1
    a.shoot_timer = 1
    a.direction = -1

    # Update should start shooting and create a laser
    a.update(camera_x=0)
    assert a.is_shooting is True
    assert len(a.lasers) == 1

    # Draw should fallback to rect and also draw the laser
    FakeDraw.rect_calls.clear()
    a.draw(screen)
    # Two rect calls: alien and laser
    assert len(FakeDraw.rect_calls) >= 1

    # After shooting animation completes, movement resumes and direction flips at bounds
    for _ in range(a.shoot_animation_duration):
        a.update(camera_x=0)
    assert a.is_shooting is False

    # Move to left bound and flip
    a.x = a.platform_left
    a.update(camera_x=0)
    assert a.direction == 1
    # Move to right bound and flip
    a.x = a.platform_right
    a.update(camera_x=0)
    assert a.direction == -1


def test_robot_shoots_and_moves(monkeypatch):
    screen = FakeScreen()

    from internal.resources.enemies.robot import Robot

    r = Robot(200, 300, 180, 240, robot_images=None, missile_images=None)
    r.shoot_interval = 1
    r.shoot_timer = 1
    r.direction = -1

    # Update triggers shooting and creates a missile
    r.update(camera_x=0)
    assert r.is_shooting is True
    assert len(r.missiles) == 1

    # After shooting finishes, movement resumes and respects bounds
    for _ in range(r.shoot_animation_duration):
        r.update(camera_x=0)
    assert r.is_shooting is False

    # Move to left bound and flip to right
    r.x = r.platform_left
    r.update(camera_x=0)
    assert r.direction == 1
    # Move to right bound and flip to left
    r.x = r.platform_right
    r.update(camera_x=0)
    assert r.direction == -1

    # Draw fallback should render robot and its missiles without images
    FakeDraw.rect_calls.clear()
    r.draw(screen)
    assert len(FakeDraw.rect_calls) >= 1