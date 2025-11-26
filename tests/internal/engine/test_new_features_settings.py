import os
import pygame

from internal.engine.game import Game, GameState


def _make_game_dev():
    g = Game()
    g.music.play_menu_music = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None
    g.music.play_music = lambda *_a, **_k: None
    return g


def test_main_menu_dynamic_continue_and_new_game_confirm(tmp_path, monkeypatch):
    g = _make_game_dev()
    g.autosave_path = os.path.join(tmp_path, "autosave.json")
    g._ensure_saves_dir()
    g._save_autosave(3, 123, 3)
    g._rebuild_main_menu_options()
    assert "Continuar" in g.menu_options
    g.menu_selected = g.menu_options.index("Continuar")
    monkeypatch.setattr(g.music, "play_level_music", lambda *_a, **_k: None)
    g.handle_menu_selection()
    assert g.state == GameState.PLAYING
    g.state = GameState.MAIN_MENU
    g._save_autosave(4, 150, 3)
    g._rebuild_main_menu_options()
    g.menu_selected = g.menu_options.index("Novo Jogo")
    g.handle_menu_selection()
    assert g.state == GameState.CONFIRM_NEW_GAME
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""}))
    g.handle_events()
    assert g.state == GameState.SELECT_DIFFICULTY


def test_pause_menu_navigation_and_options_open(monkeypatch):
    g = _make_game_dev()
    g.state = GameState.PLAYING
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE, "unicode": ""}))
    g.handle_events()
    assert g.state == GameState.PAUSED
    g.pause_menu_options = ["Continuar", "Botões/Teclas", "Áudio", "Vídeo", "Sair"]
    g.pause_selected = 2
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""}))
    g.handle_events()
    assert g.state == GameState.OPTIONS_AUDIO
    g.state = GameState.PAUSED
    g.pause_selected = 3
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""}))
    g.handle_events()
    assert g.state == GameState.OPTIONS_VIDEO


def test_audio_reset_and_persistence(tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.state = GameState.OPTIONS_AUDIO
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "unicode": ""}))
    g.handle_events()
    assert g.music_volume > 0.7
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r, "unicode": ""}))
    g.handle_events()
    assert abs(g.music_volume - 0.7) < 1e-6
    g2 = _make_game_dev()
    g2.settings_path = g.settings_path
    g2._ensure_saves_dir()
    g2._load_settings()
    assert abs(g2.music_volume - 0.7) < 1e-6


def test_video_toggle_and_scale_reset(tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.state = GameState.OPTIONS_VIDEO
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""}))
    g.handle_events()
    assert isinstance(g.env_config.get("fullscreen", False), bool)
    g.env_config["window_scale"] = 1.0
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "unicode": ""}))
    g.handle_events()
    assert g.env_config.get("window_scale", 1.0) in g.window_scales
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r, "unicode": ""}))
    g.handle_events()
    assert g.env_config.get("window_scale", 0) == 1.0
    assert g.env_config.get("fullscreen", True) is False


def test_controls_reset_and_edit_keyboard_and_joystick(monkeypatch, tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.state = GameState.OPTIONS_CONTROLS
    g.controls_selected = 3
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r, "unicode": ""}))
    g.handle_events()
    assert pygame.K_SPACE in g.controls["shoot"]
    g.controls_selected = 3
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""}))
    g.handle_events()
    assert g.controls_editing is True
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_q, "unicode": ""}))
    g.handle_events()
    assert g.controls["shoot"] == [pygame.K_q]
    g.joystick_connected = True
    g.joystick_name = "FakePad"
    g.controls_editing = True
    g.controls_selected = 2
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 0}))
    g.handle_events()
    assert g.joystick_controls.get("jump") == 0


def test_joystick_profiles_persistence(tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.joystick_connected = True
    g.joystick_name = "MyController"
    g.joystick_controls["shoot"] = 5
    g._save_settings()
    g2 = _make_game_dev()
    g2.settings_path = g.settings_path
    g2._ensure_saves_dir()
    g2.joystick_connected = True
    g2.joystick_name = "MyController"
    g2._load_settings()
    assert g2.joystick_controls.get("shoot") == 5


def test_main_menu_options_settings_and_back(monkeypatch):
    g = _make_game_dev()
    g._rebuild_main_menu_options()
    assert "Configurações" in g.menu_options
    g.menu_selected = g.menu_options.index("Configurações")
    g.handle_menu_selection()
    assert g.state == GameState.OPTIONS_MENU
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE, "unicode": ""}))
    g.handle_events()
    assert g.state == GameState.MAIN_MENU