import types

import internal.engine.title as title_mod


class RenderSurface:
    def __init__(self, w=100, h=50):
        self._w = w
        self._h = h

    def get_rect(self, **kwargs):
        # Return simple rect-like with center propagated
        center = kwargs.get("center", (0, 0))
        return types.SimpleNamespace(center=center)


class FakeSurface(RenderSurface):
    pass


class FakeFont:
    def render(self, text, antialias, color):
        return RenderSurface()


class FakeScreen:
    def __init__(self):
        self.blit_calls = []
        self.fill_calls = []

    def blit(self, sprite, pos):
        self.blit_calls.append((sprite, pos))

    def fill(self, color):
        self.fill_calls.append(color)


class FakeClock:
    def tick(self, fps):
        return 16


class FakeGame:
    def __init__(self):
        self.screen = FakeScreen()
        self.clock = FakeClock()
        self.running = True
        self.pressed_keys = set()
        self.joystick_connected = False
        self.font = FakeFont()
        self.big_font = FakeFont()

    def get_events(self):
        # No quit or keydown events; single frame
        self.running = False
        return []


def test_title_screen_show_blits_background(monkeypatch):
    # Fake pygame image load through ResourceCache
    fake_cache = types.SimpleNamespace(get_image=lambda path, scale=None: FakeSurface())
    monkeypatch.setattr(title_mod, "ResourceCache", lambda: fake_cache)

    # Fake pygame modules used inside TitleScreen
    fake_pygame = types.SimpleNamespace(
        image=types.SimpleNamespace(load=lambda p: FakeSurface()),
        event=types.SimpleNamespace(get=lambda: []),
        QUIT=0,
        KEYDOWN=1,
        K_RETURN=13,
    )
    monkeypatch.setattr(title_mod, "pygame", fake_pygame)

    # Provide pygame.time.get_ticks
    fake_pygame.time = types.SimpleNamespace(get_ticks=lambda: 1000)
    game = FakeGame()
    title_mod.TitleScreen.show(game)
    # Should have attempted to blit at least one background/title
    assert len(game.screen.blit_calls) >= 1


def test_title_screen_show_fallback_on_error(monkeypatch):
    # ResourceCache raises to force fallback path
    def raise_error(*args, **kwargs):
        raise Exception("load error")

    fake_cache = types.SimpleNamespace(get_image=lambda path, scale=None: raise_error())
    monkeypatch.setattr(title_mod, "ResourceCache", lambda: fake_cache)

    fake_pygame = types.SimpleNamespace(
        image=types.SimpleNamespace(load=lambda p: FakeSurface()),
        event=types.SimpleNamespace(get=lambda: []),
        QUIT=0,
        KEYDOWN=1,
        K_RETURN=13,
        time=types.SimpleNamespace(get_ticks=lambda: 1000),
    )
    monkeypatch.setattr(title_mod, "pygame", fake_pygame)

    game = FakeGame()
    title_mod.TitleScreen.show(game)
    # Fallback draw should still result in a blit-like record
    assert len(game.screen.blit_calls) >= 1