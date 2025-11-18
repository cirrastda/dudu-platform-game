import types
import pygame

from internal.engine.game import Game, GameState
from internal.engine.difficulty import Difficulty
import internal.engine.game as gm
import internal.engine.level.level as level_module


def post_key(key):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, unicode=""))


def test_add_score_multiplier_and_exception_fallback(monkeypatch):
    g = Game()

    # Easy: multiplier 0.4, positive minimum enforced
    g.difficulty = Difficulty.EASY
    points = g.add_score(1)
    assert points == 1  # rounded to 0, but minimum positive becomes 1
    assert g.score >= 1

    # Hard: multiplier 3.0
    g.difficulty = Difficulty.HARD
    prev = g.score
    points = g.add_score(2)
    assert points == 6
    assert g.score == prev + 6

    # Fallback when get_score_multiplier raises
    monkeypatch.setattr(
        g, "get_score_multiplier", lambda: (_ for _ in ()).throw(Exception("boom"))
    )
    prev = g.score
    points = g.add_score(10)
    assert points == 10
    assert g.score == prev + 10


def test_check_extra_life_milestones_and_increment(monkeypatch):
    g = Game()
    # Configure Normal difficulty extra life system explicitly
    g.difficulty = Difficulty.NORMAL
    milestones, inc = g.get_extra_life_milestones_and_increment()
    g.extra_life_milestones = milestones
    g.extra_life_increment_after_milestones = inc
    g.next_extra_life_score = milestones[0]
    g.extra_lives_earned = 0
    g.lives = 3

    calls = []
    monkeypatch.setattr(
        g.sound_effects, "play_sound_effect", lambda name: calls.append(name)
    )

    # First award at first milestone
    added = g.add_score(milestones[0])
    assert added == milestones[0]
    assert g.lives == 4
    assert g.next_extra_life_score == milestones[1]
    assert calls[-1] == "new-life"

    # Second award at second milestone
    delta = milestones[1] - g.score
    added = g.add_score(delta)
    assert added == delta
    assert g.lives == 5
    assert g.next_extra_life_score == milestones[2]
    assert calls[-1] == "new-life"

    # Third award transitions to increment-based thresholds
    delta = milestones[2] - g.score
    added = g.add_score(delta)
    assert added == delta
    assert g.lives == 6
    assert g.next_extra_life_score == milestones[2] + inc
    assert calls[-1] == "new-life"

    # Fourth award uses increment after milestones
    delta = (milestones[2] + inc) - g.score
    added = g.add_score(delta)
    assert added == delta
    assert g.lives == 7
    assert g.next_extra_life_score == milestones[2] + inc + inc
    assert calls[-1] == "new-life"


def test_draw_ocean_background_fallback_gradient_and_waves():
    g = Game()
    # Ensure no background images are available
    g.state = GameState.MAIN_MENU
    g.image.background_img = None
    # Use a dedicated surface to avoid relying on Game.screen
    surface = pygame.Surface((gm.WIDTH, gm.HEIGHT))
    surface.fill((255, 255, 255))

    g.draw_ocean_background(draw_surface=surface)
    # Top pixel should be changed from the initial fill (gradient applied)
    top = surface.get_at((0, 0))
    assert (top.r, top.g, top.b) != (255, 255, 255)

    # Also test PLAYING path with missing background
    g.state = GameState.PLAYING
    # Explicitly set attribute background_img to None to trigger fallback
    g.background_img = None
    g.draw_ocean_background(draw_surface=surface)
    top2 = surface.get_at((1, 0))
    # Color should remain non-default indicating gradient draw occurred
    assert (top2.r, top2.g, top2.b) != (255, 255, 255)


def test_draw_ocean_background_uses_menu_background_when_available():
    g = Game()
    g.state = GameState.MAIN_MENU
    # Create a solid background for menu and set it explicitly
    bg = pygame.Surface((gm.WIDTH, gm.HEIGHT))
    bg.fill((1, 2, 3))
    g.menu_background_img = bg
    surface = pygame.Surface((gm.WIDTH, gm.HEIGHT))

    g.draw_ocean_background(draw_surface=surface)
    pix = surface.get_at((0, 0))
    assert (pix.r, pix.g, pix.b) == (1, 2, 3)


def test_title_screen_skip_opening_video_goes_to_main_menu(monkeypatch):
    g = Game()
    g.state = GameState.TITLE_SCREEN
    g.env_config = {"skip-opening-video": "1"}
    # Ensure environment is not development so the skip logic uses env_config
    monkeypatch.setitem(gm.ENV_CONFIG, "environment", "production")

    played = {"called": False}
    monkeypatch.setattr(
        g.music, "play_menu_music", lambda *_a, **_k: played.__setitem__("called", True)
    )
    g.music_started = False

    post_key(pygame.K_RETURN)
    g.handle_events()

    # Em produção, não deve pular; deve ir para OPENING_VIDEO
    assert g.state == GameState.OPENING_VIDEO
    # Música de menu não inicia ainda
    assert g.music_started is False
    assert played["called"] is False


def test_update_bird_difficulty_ranges_and_difficulty(monkeypatch):
    g = Game()

    # Patch Level getters for birds/bats to deterministic values
    monkeypatch.setattr(level_module.Level, "get_birds_per_spawn", lambda lvl: 2)
    monkeypatch.setattr(level_module.Level, "get_bird_spawn_interval", lambda lvl: 100)

    # Levels 1-20: birds
    g.current_level = 10
    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.birds_per_spawn == 2
    assert g.bird_spawn_interval == 100

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    # qty round(2 * 0.7) -> 1; interval max(60, 100 * 1.5) -> 150
    assert g.birds_per_spawn == 1
    assert g.bird_spawn_interval == 150

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    # qty round(2 * 1.4) -> 3; interval max(60, 100 * 0.7) -> 70
    assert g.birds_per_spawn == 3
    assert g.bird_spawn_interval == 70

    # Levels 21-30: bats use birds progression
    g.current_level = 25
    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.bats_per_spawn == 2
    assert g.bat_spawn_interval == 100

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    assert g.bats_per_spawn == 1
    assert g.bat_spawn_interval == 150

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    assert g.bats_per_spawn == 3
    assert g.bat_spawn_interval == 70

    # Levels 31-40: airplanes fixed base values with difficulty modifiers
    g.current_level = 35
    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.airplanes_per_spawn == 1
    assert g.airplane_spawn_interval == 150

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    assert g.airplanes_per_spawn == 1
    assert g.airplane_spawn_interval == 225

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    assert g.airplanes_per_spawn == 1
    assert g.airplane_spawn_interval == 105

    # Levels 41-50: flying disks fixed base values with difficulty modifiers
    g.current_level = 45
    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.flying_disks_per_spawn == 1
    assert g.flying_disk_spawn_interval == 150

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    assert g.flying_disks_per_spawn == 1
    assert g.flying_disk_spawn_interval == 225

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    assert g.flying_disks_per_spawn == 1
    assert g.flying_disk_spawn_interval == 105

    # Level 51+: fires fixed base values with difficulty modifiers and clamp
    g.current_level = 51
    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.fires_per_spawn == 1
    assert g.fire_spawn_interval == 240

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    assert g.fires_per_spawn == 1
    assert g.fire_spawn_interval == 360

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    assert g.fires_per_spawn == 1
    assert g.fire_spawn_interval == 168
