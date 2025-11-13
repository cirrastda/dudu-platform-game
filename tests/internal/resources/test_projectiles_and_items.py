import types

import internal.resources.bullet as bullet_mod
import internal.resources.missile as missile_mod
import internal.resources.enemies.fire as fire_mod
import internal.resources.enemies.turtle as turtle_mod
import internal.resources.explosion as explosion_mod
import internal.resources.extra_life as extra_life_mod
import internal.resources.flag as flag_mod


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def colliderect(self, other):
        return not (
            self.x + self.w <= other.x or self.x >= other.x + other.w or self.y + self.h <= other.y or self.y >= other.y + other.h
        )


class FakeSurface:
    def __init__(self, w=10, h=10):
        self._w = w
        self._h = h
        self.alpha = None

    def set_alpha(self, a):
        self.alpha = a


class FakeTransform:
    @staticmethod
    def scale(img, size):
        return img


class FakeDraw:
    @staticmethod
    def rect(screen, color, rect):
        screen.draw_calls.append(("rect", color, rect if isinstance(rect, tuple) else (rect.x, rect.y, rect.w, rect.h)))

    @staticmethod
    def circle(screen, color, center, radius):
        screen.draw_calls.append(("circle", color, center, radius))

    @staticmethod
    def polygon(screen, color, points):
        screen.draw_calls.append(("polygon", color, points))

    @staticmethod
    def ellipse(screen, color, rect):
        screen.draw_calls.append(("ellipse", color, (rect.x, rect.y, rect.w, rect.h)))


class FakeScreen:
    def __init__(self):
        self.blit_calls = []
        self.draw_calls = []

    def blit(self, sprite, pos):
        self.blit_calls.append((sprite, pos))


def _install_fake_pygame(monkeypatch, module):
    fake_pygame = types.SimpleNamespace(
        Rect=FakeRect,
        transform=FakeTransform,
        draw=FakeDraw,
        error=Exception,
        SRCALPHA=1,
        Surface=lambda size, flags=None: FakeSurface(size[0], size[1]),
        image=types.SimpleNamespace(load=lambda p: FakeSurface()),
    )
    monkeypatch.setattr(module, "pygame", fake_pygame, raising=False)


def test_bullet_update_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, bullet_mod)
    screen = FakeScreen()

    # With image
    b1 = bullet_mod.Bullet(10, 20, direction=1, image=FakeSurface())
    assert b1.update() is True
    assert b1.x > 10
    b1.draw(screen)
    assert len(screen.blit_calls) == 1

    # Fallback draw
    b2 = bullet_mod.Bullet(5, 6, direction=-1, image=None)
    b2.update()
    b2.draw(screen)
    assert any(call[0] == "rect" for call in screen.draw_calls)


def test_missile_update_bounds_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, missile_mod)
    screen = FakeScreen()
    images = {"left": FakeSurface(), "right": FakeSurface()}
    m = missile_mod.Missile(100, 40, direction=1, missile_images=images)
    assert m.update(camera_x=0) is True
    m.draw(screen)
    assert len(screen.blit_calls) == 1
    # Move far out of view
    m.x = 2000
    assert m.update(camera_x=0) is False

    # Fallback draw without images
    m2 = missile_mod.Missile(50, 50, direction=-1, missile_images=None)
    m2.draw(screen)
    assert any(c[0] == "rect" for c in screen.draw_calls)


def test_fire_update_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, fire_mod)
    screen = FakeScreen()
    # With image
    f1 = fire_mod.Fire(60, 70, fire_image=FakeSurface())
    assert f1.update(camera_x=0) is True
    f1.draw(screen)
    assert len(screen.blit_calls) == 1
    # Move left past camera margin
    f1.x = -300
    assert f1.update(camera_x=0) is False

    # Fallback draw without image
    f2 = fire_mod.Fire(10, 10, fire_image=None)
    f2.draw(screen)
    assert any(c[0] == "circle" for c in screen.draw_calls)


def test_turtle_update_bounds_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, turtle_mod)
    screen = FakeScreen()
    images = {"left": [FakeSurface(), FakeSurface()], "right": [FakeSurface()]}
    t = turtle_mod.Turtle(100, 80, left_limit=90, right_limit=110, turtle_images=images)
    # Move left to bound and flip to right
    for _ in range(100):
        t.update()
    assert t.direction in (-1, 1)
    t.draw(screen)
    assert len(screen.blit_calls) == 1
    # Fallback draw with no images
    t2 = turtle_mod.Turtle(0, 0, left_limit=0, right_limit=10, turtle_images=None)
    t2.draw(screen)
    assert any(c[0] == "ellipse" or c[0] == "circle" for c in screen.draw_calls)


def test_explosion_update_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, explosion_mod)
    screen = FakeScreen()
    e = explosion_mod.Explosion(30, 40, image=FakeSurface())
    assert e.update() is True
    e.draw(screen)
    assert len(screen.blit_calls) == 1
    # Exhaust timer and ensure update returns False
    for _ in range(40):
        e.update()
    assert e.timer <= 0
    assert e.update() is False
    # Fallback draw on new explosion without image
    e2 = explosion_mod.Explosion(10, 10, image=None)
    e2.draw(screen)
    # It may or may not blink this frame; ensure circles recorded sometime
    for _ in range(6):
        e2.timer = 5
        e2.draw(screen)
        e2.timer -= 1
    assert any(c[0] == "circle" for c in screen.draw_calls)


def test_extra_life_update_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, extra_life_mod)
    screen = FakeScreen()
    # Use provided image to avoid disk
    el = extra_life_mod.ExtraLife(15, 25, image=FakeSurface(), size=(24, 24))
    # Blink update toggles alpha values across a full cycle
    alphas = []
    for _ in range(el.blink_period + 5):
        el.update()
        el.draw(screen)
        alphas.append(el.current_alpha)
    assert any(a == 255 for a in alphas) and any(a == 90 for a in alphas)


def test_flag_draw_with_image_and_fallback(monkeypatch):
    # First, load image path successfully
    _install_fake_pygame(monkeypatch, flag_mod)
    fake_image_module = types.SimpleNamespace(load=lambda p: FakeSurface())
    fake_pygame = flag_mod.pygame
    fake_pygame.image = fake_image_module
    screen = FakeScreen()
    flg = flag_mod.Flag(5, 6)
    flg.draw(screen)
    assert len(screen.blit_calls) == 1

    # Now force load error to exercise fallback path
    def raise_error(*args, **kwargs):
        raise fake_pygame.error("load fail")
    fake_pygame.image.load = raise_error
    flg2 = flag_mod.Flag(10, 10)
    flg2.flag_image = None  # ensure fallback
    flg2.draw(screen)
    assert any(c[0] in ("rect", "polygon") for c in screen.draw_calls)