import types

from internal.utils.constants import WIDTH
import internal.resources.enemies.bird as bird_mod
import internal.resources.enemies.bat as bat_mod
import internal.resources.enemies.airplane as airplane_mod
import internal.resources.enemies.flying_disk as disk_mod
import internal.resources.enemies.spider as spider_mod
import internal.resources.enemies.robot as robot_mod


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


class FakeTransform:
    @staticmethod
    def flip(img, xbool, ybool):
        return img


class FakeDraw:
    @staticmethod
    def ellipse(screen, color, rect):
        screen.draw_calls.append(("ellipse", color, rect.x, rect.y, rect.w, rect.h))

    @staticmethod
    def polygon(screen, color, points):
        screen.draw_calls.append(("polygon", color, points))

    @staticmethod
    def rect(screen, color, rect):
        screen.draw_calls.append(("rect", color, rect[0], rect[1], rect[2], rect[3]))

    @staticmethod
    def circle(screen, color, center, radius):
        screen.draw_calls.append(("circle", color, center, radius))

    @staticmethod
    def line(screen, color, p1, p2, w):
        screen.draw_calls.append(("line", color, p1, p2, w))


class FakeScreen:
    def __init__(self):
        self.blit_calls = []
        self.draw_calls = []

    def blit(self, sprite, pos):
        self.blit_calls.append((pos[0], pos[1]))


def _install_fake_pygame(monkeypatch, module):
    fake_pygame = types.SimpleNamespace(
        Rect=FakeRect,
        transform=FakeTransform,
        draw=FakeDraw,
        error=Exception,
    )
    monkeypatch.setattr(module, "pygame", fake_pygame, raising=False)


def test_bird_update_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, bird_mod)
    b = bird_mod.Bird(x=WIDTH - 10, y=50, bird_images=(FakeSurface(), FakeSurface()))
    screen = FakeScreen()

    # Update moves left and returns True while visible
    ok = b.update()
    assert ok is True
    assert b.x < WIDTH - 10

    # Draw uses provided images
    b.draw(screen)
    assert len(screen.blit_calls) == 1

    # Move offscreen to the left should return False
    b.x = -b.width - 1
    assert b.update() is False


def test_bat_update_direction_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, bat_mod)
    bat = bat_mod.Bat(x=WIDTH - 10, y=50, bat_images=[FakeSurface(), FakeSurface(), FakeSurface()])
    screen = FakeScreen()

    # Update moves left, remains visible
    assert bat.update(camera_x=0) is True
    # Flip direction and draw should still blit
    bat.direction = 1
    bat.draw(screen)
    assert len(screen.blit_calls) == 1

    # Move far right offscreen, update returns False
    bat.x = 2000
    assert bat.update(camera_x=0) is False


def test_airplane_update_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, airplane_mod)
    ap = airplane_mod.Airplane(x=WIDTH - 10, y=80, airplane_images=[FakeSurface(), FakeSurface()])
    screen = FakeScreen()
    assert ap.update(camera_x=0) is True
    ap.draw(screen)
    assert len(screen.blit_calls) == 1
    ap.x = -400
    assert ap.update(camera_x=0) is False


def test_flying_disk_update_sine_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, disk_mod)
    d = disk_mod.FlyingDisk(x=WIDTH - 10, y=100, disk_images=[FakeSurface(), FakeSurface()], amplitude=20, frequency=0.2)
    screen = FakeScreen()
    y0 = d.y
    assert d.update(camera_x=0) is True
    assert d.y != y0  # sine motion changes y
    d.draw(screen)
    assert len(screen.blit_calls) == 1
    d.x = 2000
    assert d.update(camera_x=0) is False


def test_spider_update_limits_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, spider_mod)
    s = spider_mod.Spider(x=120, y=90, top_limit=60, bottom_limit=150, spider_images=[FakeSurface(), FakeSurface()])
    screen = FakeScreen()
    # After 100 updates from y=90 with speed=1.5, it cycles to top_limit
    for _ in range(100):
        s.update()
    assert s.y == s.top_limit
    # Continue updates until bottom limit reached in the next cycle
    for _ in range(1000):
        s.update()
        if s.y == s.bottom_limit:
            break
    assert s.y == s.bottom_limit
    # Draw should blit image and draw web line
    s.draw(screen)
    assert any(call[0] == "line" for call in screen.draw_calls)
    assert len(screen.blit_calls) == 1


def test_robot_update_shooting_and_draw(monkeypatch):
    _install_fake_pygame(monkeypatch, robot_mod)
    screen = FakeScreen()

    r = robot_mod.Robot(x=100, y=100, left_limit=80, right_limit=140, robot_images={
        "left": [FakeSurface(), FakeSurface()],
        "right": [FakeSurface(), FakeSurface()],
        "shot_left": [FakeSurface()],
        "shot_right": [FakeSurface()],
    }, missile_images={"left": FakeSurface(), "right": FakeSurface()})

    # Replace start_shooting to avoid importing real Missile
    shots = []

    def fake_start_shooting(images=None):
        r.is_shooting = True
        r.shoot_animation_timer = 0
        shots.append("shot")

    monkeypatch.setattr(r, "start_shooting", fake_start_shooting)

    # Force shoot_timer to exceed interval
    r.shoot_timer = r.shoot_interval
    r.direction = -1
    r.update(camera_x=0)
    assert r.is_shooting is True
    assert shots == ["shot"]

    # During shooting, draw uses shot_left images
    r.draw(screen)
    assert len(screen.blit_calls) == 1

    # Finish shooting after duration
    r.shoot_animation_timer = r.shoot_animation_duration
    r.update(camera_x=0)
    assert r.is_shooting is False
    # Move and invert direction at bounds
    r.x = r.platform_left
    r.direction = -1
    r.update(camera_x=0)
    assert r.direction == 1