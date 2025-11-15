import types

import pytest


def _setup_game(monkeypatch):
    import internal.engine.game as gm

    # Patch ENV_CONFIG to production to avoid dev shortcuts
    monkeypatch.setattr(gm, "ENV_CONFIG", {"environment": "production"})

    # Stub audio systems
    class FakeMusic:
        def play_menu_music(self, game):
            pass
        def play_level_music(self, game, level):
            pass
        def play_music(self, name):
            pass
        def start(self, game):
            pass
    class FakeSoundEffects:
        def load_sound_effects(self):
            pass
        def play_sound_effect(self, name):
            pass

    gm.Music = lambda: FakeMusic()
    gm.SoundEffects = lambda: FakeSoundEffects()

    # Mixer.init no-op
    import internal.engine.sound.mixer as mixer_module
    monkeypatch.setattr(mixer_module.Mixer, "init", lambda _pg: None)

    # Level.init_level no-op
    import internal.engine.level.level as level_mod
    monkeypatch.setattr(level_mod.Level, "init_level", lambda game: None)

    # pygame.key.get_pressed stub
    def fake_get_pressed():
        return tuple(False for _ in range(300))
    monkeypatch.setattr(gm.pygame.key, "get_pressed", fake_get_pressed)

    # Instantiate game
    g = gm.Game()
    g.music = FakeMusic()
    g.sound_effects = FakeSoundEffects()
    return g


def test_konami_code_keyboard_grants_99_lives(monkeypatch):
    import internal.engine.game as gm
    g = _setup_game(monkeypatch)
    # Ensure we're in a state that ignores key side-effects
    g.state = gm.GameState.OPENING_VIDEO

    # Build keyboard Konami sequence events
    seq = [
        gm.pygame.K_UP,
        gm.pygame.K_UP,
        gm.pygame.K_DOWN,
        gm.pygame.K_DOWN,
        gm.pygame.K_LEFT,
        gm.pygame.K_RIGHT,
        gm.pygame.K_LEFT,
        gm.pygame.K_RIGHT,
        gm.pygame.K_b,
        gm.pygame.K_a,
    ]
    events = []
    for key in seq:
        uni = "b" if key == gm.pygame.K_b else ("a" if key == gm.pygame.K_a else "")
        events.append(types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=key, unicode=uni))

    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: events))

    # Process all events in one pass
    res = g.handle_events()
    assert res is True
    assert getattr(g, "cheat_99_lives_enabled", False) is True
    assert g.get_initial_lives() == 99
    assert g.max_lives == 99
    assert g.lives == 99


class FakeJoystick:
    def __init__(self):
        self.axes = {0: 0.0, 1: 0.0}
        self.numaxes = 2
    def get_numaxes(self):
        return self.numaxes
    def get_axis(self, idx):
        return self.axes.get(idx, 0.0)


def test_konami_code_joystick_grants_99_lives(monkeypatch):
    import internal.engine.game as gm
    g = _setup_game(monkeypatch)

    # Inject fake joystick and mark connected
    g.joystick = FakeJoystick()
    g.joystick_connected = True

    # Avoid menu side-effects; OPENING_VIDEO ignores button input
    g.state = gm.GameState.OPENING_VIDEO

    # No events; we'll drive axes directly
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: []))

    # UP, UP
    g.joystick.axes[1] = -1.0
    g.handle_events()
    g.joystick.axes[1] = 0.0
    g.handle_events()
    g.joystick.axes[1] = -1.0
    g.handle_events()
    g.joystick.axes[1] = 0.0
    g.handle_events()

    # DOWN, DOWN
    g.joystick.axes[1] = 1.0
    g.handle_events()
    g.joystick.axes[1] = 0.0
    g.handle_events()
    g.joystick.axes[1] = 1.0
    g.handle_events()
    g.joystick.axes[1] = 0.0
    g.handle_events()

    # LEFT, RIGHT, LEFT, RIGHT
    g.joystick.axes[0] = -1.0
    g.handle_events()
    g.joystick.axes[0] = 0.0
    g.handle_events()
    g.joystick.axes[0] = 1.0
    g.handle_events()
    g.joystick.axes[0] = 0.0
    g.handle_events()
    g.joystick.axes[0] = -1.0
    g.handle_events()
    g.joystick.axes[0] = 0.0
    g.handle_events()
    g.joystick.axes[0] = 1.0
    g.handle_events()
    g.joystick.axes[0] = 0.0
    g.handle_events()

    # Finally B, A as joystick buttons
    ev_b = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=1)
    ev_a = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_b, ev_a]))
    g.handle_events()

    assert getattr(g, "cheat_99_lives_enabled", False) is True
    assert g.get_initial_lives() == 99
    assert g.max_lives == 99
    assert g.lives == 99