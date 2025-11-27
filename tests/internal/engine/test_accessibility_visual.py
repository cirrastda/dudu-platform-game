import os
import types
import pygame

from internal.engine.game import Game, GameState
from internal.engine.screen import Screen


def _make_game_dev():
    g = Game()
    g.music.play_menu_music = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None
    g.music.play_music = lambda *_a, **_k: None
    return g


def test_accessibility_colorblind_cycle_and_persistence(tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.state = GameState.OPTIONS_ACCESSIBILITY
    g.access_selected = 0
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "unicode": ""}))
    g.handle_events()
    assert g.colorblind_mode in ("deuteranopia", "protanopia", "tritanopia")
    g2 = _make_game_dev()
    g2.settings_path = g.settings_path
    g2._ensure_saves_dir()
    g2._load_settings()
    assert g2.colorblind_mode == g.colorblind_mode


def test_accessibility_vibration_toggle_and_rumble_integration(monkeypatch):
    g = _make_game_dev()
    g.vibration_enabled = True
    called = []
    g.joystick_connected = True
    g.joystick = types.SimpleNamespace(rumble=lambda lo, hi, dur: called.append((lo, hi, dur)))
    g.sound_effects.play_sound_effect("player-hit")
    assert called and called[0][2] >= 100


def test_video_visual_mode_toggle_and_persist(tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.state = GameState.OPTIONS_VIDEO
    g.video_selected = 2
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""}))
    g.handle_events()
    assert g.visual_mode in ("8bit", "normal")
    g2 = _make_game_dev()
    g2.settings_path = g.settings_path
    g2._ensure_saves_dir()
    g2._load_settings()
    assert g2.visual_mode == g.visual_mode


def test_screen_present_with_filters_no_error(monkeypatch):
    g = _make_game_dev()
    g.visual_mode = "8bit"
    g.colorblind_mode = "deuteranopia"
    Screen.present(g)


def test_accessibility_vibration_persistence(tmp_path):
    g = _make_game_dev()
    g.settings_path = os.path.join(tmp_path, "settings.json")
    g._ensure_saves_dir()
    g.vibration_enabled = True
    g._save_settings()
    g2 = _make_game_dev()
    g2.settings_path = g.settings_path
    g2._ensure_saves_dir()
    g2._load_settings()
    assert g2.vibration_enabled is True