import types

import pytest


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


class FakeJoystick:
    def __init__(self):
        self.axes = {0: 0.0, 1: 0.0}
        self.numaxes = 2
    def get_numaxes(self):
        return self.numaxes
    def get_axis(self, idx):
        return self.axes.get(idx, 0.0)


def _setup_game(monkeypatch, env=None):
    import internal.engine.game as gm

    # Patch ENV_CONFIG
    env_conf = {"environment": "development"}
    if env:
        env_conf.update(env)
    monkeypatch.setattr(gm, "ENV_CONFIG", env_conf)

    # Patch audio
    gm.Music = lambda: FakeMusic()
    gm.SoundEffects = lambda: FakeSoundEffects()

    # Mixer.init no-op
    import internal.engine.sound.mixer as mixer_module
    monkeypatch.setattr(mixer_module.Mixer, "init", lambda _pg: None)

    # Joystick.init inject fake and mark connected
    import internal.engine.joystick as joystick_module
    def fake_joystick_init(game):
        game.joystick = FakeJoystick()
        game.joystick_connected = True
    monkeypatch.setattr(joystick_module.Joystick, "init", fake_joystick_init)

    # Level.init_level no-op
    import internal.engine.level.level as level_mod
    monkeypatch.setattr(level_mod.Level, "init_level", lambda game: None)

    # pygame.key.get_pressed stub
    import internal.engine.game as game_module
    def fake_get_pressed():
        # Return 300 keys as False
        return tuple(False for _ in range(300))
    monkeypatch.setattr(game_module.pygame.key, "get_pressed", fake_get_pressed)

    # Instantiate game
    g = gm.Game()
    g.music = FakeMusic()
    g.sound_effects = FakeSoundEffects()
    # Minimal fields
    g.difficulty_options = ["Fácil", "Normal", "Difícil"]
    g.difficulty_selected = 1
    g.max_lives = 3
    g.lives = 3
    g.score = 0
    g.platforms_jumped = set()
    g.birds_dodged = set()
    g.collected_extra_life_levels = set()
    return g


def test_select_difficulty_joystick_initial_stage_invalid(monkeypatch):
    g = _setup_game(monkeypatch, env={"initial-stage": "abc"})
    g.state = __import__("internal.engine.game").engine.game.GameState.SELECT_DIFFICULTY

    import internal.engine.game as gm
    ev_confirm = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_confirm]))

    result = g.handle_events()
    assert result is True
    assert g.state == __import__("internal.engine.game").engine.game.GameState.PLAYING
    assert g.current_level == 1
    assert g.lives == g.max_lives


def test_select_difficulty_joystick_initial_stage_out_of_range(monkeypatch):
    g = _setup_game(monkeypatch, env={"initial-stage": "999"})
    g.state = __import__("internal.engine.game").engine.game.GameState.SELECT_DIFFICULTY

    import internal.engine.game as gm
    ev_confirm = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_confirm]))

    g.handle_events()
    assert g.state == __import__("internal.engine.game").engine.game.GameState.PLAYING
    assert g.current_level == 1


def test_game_over_selection_exit_returns_false(monkeypatch):
    g = _setup_game(monkeypatch)
    import internal.engine.game as gm
    g.state = gm.GameState.GAME_OVER
    g.game_over_selected = 2
    # Trigger selection with Enter key
    ev_enter = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_enter]))
    res = g.handle_events()
    assert res is False


def test_show_ranking_back_fallback(monkeypatch):
    g = _setup_game(monkeypatch)
    import internal.engine.game as gm
    g.state = gm.GameState.SHOW_RANKING
    g.previous_state_before_ranking = None
    ev_back = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=1)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_back]))
    g.handle_events()
    assert g.state == gm.GameState.MAIN_MENU


def test_joystick_button_jump_and_axes_deadzone(monkeypatch):
    g = _setup_game(monkeypatch)
    import internal.engine.game as gm
    g.state = gm.GameState.PLAYING
    # Set axes small within deadzone
    g.joystick.axes[0] = 0.05
    g.joystick.axes[1] = -0.09

    events = [
        types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0),  # jump mapping
    ]
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: events))

    # Call handle_events to traverse joystick branch and axes reads
    res = g.handle_events()
    assert res is True