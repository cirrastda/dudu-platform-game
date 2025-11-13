import types

import pytest


def test_difficulty_enum_has_members():
    from internal.engine.difficulty import Difficulty
    # Tiny enum coverage – reflect actual members present
    assert hasattr(Difficulty, "EASY")
    assert hasattr(Difficulty, "HARD")


class FakeSurface:
    def __init__(self, w=800, h=600):
        self.w = w
        self.h = h


class FakePygameError(Exception):
    pass


class FakeInfo:
    def __init__(self, w=1024, h=768):
        self.current_w = w
        self.current_h = h


class FakeDisplay:
    def __init__(self):
        self.set_mode_calls = []
    def set_mode(self, size, flags=0):
        self.set_mode_calls.append((size, flags))
        return FakeSurface(size[0], size[1])
    def Info(self):
        return FakeInfo()


class FakePygame:
    FULLSCREEN = 1
    def __init__(self):
        self.display = FakeDisplay()
        self.Surface = FakeSurface


def test_screen_window_mode_path(monkeypatch):
    from internal.engine import screen as screen_module

    # Patch pygame module inside screen to our fake
    monkeypatch.setattr(screen_module, "pygame", FakePygame(), raising=True)

    # Fake game object reporting development mode and fullscreen disabled
    class FakeGame:
        def __init__(self):
            self.env_config = {"environment": "development"}
        def is_development(self):
            return True

    game = FakeGame()
    # Force is_fullscreen to return False
    monkeypatch.setattr(screen_module.Screen, "is_fullscreen", lambda g: False, raising=True)

    screen_module.Screen.init(game)
    # Window mode path: set_mode with flags 0
    calls = screen_module.pygame.display.set_mode_calls
    assert calls[-1] == ((screen_module.WIDTH, screen_module.HEIGHT), 0)
    assert isinstance(game.screen, FakeSurface)


def test_screen_fullscreen_path(monkeypatch):
    from internal.engine import screen as screen_module

    monkeypatch.setattr(screen_module, "pygame", FakePygame(), raising=True)

    class FakeGame:
        def __init__(self):
            self.env_config = {"environment": "development"}
        def is_development(self):
            return True

    game = FakeGame()
    # Force fullscreen choice
    monkeypatch.setattr(screen_module.Screen, "is_fullscreen", lambda g: True, raising=True)

    screen_module.Screen.init(game)
    calls = screen_module.pygame.display.set_mode_calls
    info = screen_module.pygame.display.Info()
    assert calls[-1] == ((info.current_w, info.current_h), screen_module.pygame.FULLSCREEN)
    # game.screen should be a game_surface instance
    assert isinstance(game.screen, FakeSurface)


def test_title_show_handles_missing_background(monkeypatch):
    from internal.engine import title as title_module

    # Fake screen with fill/blit collector
    class FakeScreen:
        def __init__(self):
            self.fills = []
            self.blits = []
        def fill(self, color):
            self.fills.append(color)
        def blit(self, img, pos):
            self.blits.append((img, pos))

    class FakeRenderObj:
        def get_rect(self, center):
            return types.SimpleNamespace(center=center)

    class FakeFont:
        def render(self, text, aa, color):
            return FakeRenderObj()

    # Patch ResourceCache to raise error and force fallback path
    class FakeCache:
        def get_image(self, path, scale):
            raise FakePygameError("load fail")

    # Patch pygame time
    class FakePyg:
        class time:
            @staticmethod
            def get_ticks():
                return 0

    monkeypatch.setattr(title_module, "ResourceCache", lambda: FakeCache(), raising=True)
    monkeypatch.setattr(title_module, "pygame", FakePyg, raising=True)

    # Minimal fake game
    game = types.SimpleNamespace(
        screen=FakeScreen(),
        big_font=FakeFont(),
        font=FakeFont(),
        joystick_connected=False,
    )

    # Show should not crash; fallback path draws text
    title_module.TitleScreen.show(game)
    assert len(game.screen.blits) >= 1