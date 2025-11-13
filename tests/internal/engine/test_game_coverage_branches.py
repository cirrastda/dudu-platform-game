import types
import pygame
import pytest
from internal.engine.state import GameState


def _make_game():
    # Helper to create a Game with minimal side effects
    from internal.engine.game import Game, WIDTH, HEIGHT
    g = Game()
    # Disable music hooks to avoid external dependency during tests
    g.play_menu_music = lambda: None
    g.play_level_music = lambda: None
    g.stop_music = lambda: None
    g.sound_effects = types.SimpleNamespace(play_sound_effect=lambda *_a, **_k: None)
    # Ensure explosions can be created
    assert hasattr(g, "explosion_image")
    # Provide a dummy screen
    g.screen = pygame.Surface((WIDTH, HEIGHT))
    # Ensure gameplay logic runs by default
    g.state = GameState.PLAYING
    return g


def _rect_at_center():
    return pygame.Rect(0, 0, 10, 10).move(340, 240)


def test_update_collects_extra_life_increments_lives_and_marks_level(monkeypatch):
    g = _make_game()
    g.current_level = 12
    # Ensure player starts with a known number of lives
    # Lives in dev mode may be high; just capture baseline
    baseline_lives = g.lives
    # Mark level as not yet collected
    g.collected_extra_life_levels.discard(g.current_level)
    # Place an extra life overlapping player
    item = types.SimpleNamespace(update=lambda: None, rect=_rect_at_center())
    g.player.rect = _rect_at_center()
    # Keep player static so rect doesn't change during update
    g.player.update = lambda *args, **kwargs: None
    g.extra_lives = [item]

    # Avoid sound side effects by stubbing the specific game sound
    g.extra_life_sound = types.SimpleNamespace(play=lambda: None)

    g.update()

    assert g.lives == baseline_lives + 1
    assert g.current_level in g.collected_extra_life_levels


def test_update_alien_laser_invulnerable_explodes_and_scores(monkeypatch):
    g = _make_game()
    # Level range for aliens (lasers): 41-50
    g.current_level = 45
    g.score = 0
    # Player invulnerable and overlapping a laser
    g.player.is_invulnerable = True
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    laser = types.SimpleNamespace(rect=_rect_at_center(), x=340, y=240)
    alien = types.SimpleNamespace(x=340, y=240, lasers=[laser], rect=pygame.Rect(1000, 1000, 10, 10), update=lambda camera_x: None)
    g.aliens = [alien]

    # Explosion sound muted
    g.explosion_sound = types.SimpleNamespace(play=lambda: None)

    g.update()

    # Score should increase when invulnerable and hit by alien laser
    assert g.score > 0


def test_update_robot_collision_invulnerable_transfers_missiles_and_scores(monkeypatch):
    g = _make_game()
    g.current_level = 35
    g.score = 0
    g.player.is_invulnerable = True
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    missile = types.SimpleNamespace(rect=_rect_at_center(), x=340, y=240)
    robot = types.SimpleNamespace(x=340, y=240, missiles=[missile], rect=_rect_at_center(), update=lambda camera_x: None)
    g.robots = [robot]

    g.explosion_sound = types.SimpleNamespace(play=lambda: None)

    g.update()
    # Score should increase when invulnerable collides with robot/missile
    assert g.score > 0


def test_update_flag_collision_advances_level(monkeypatch):
    from internal.engine.level.level import Level

    g = _make_game()
    g.current_level = 5
    g.state = GameState.PLAYING
    # Put flag on player
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    flag = types.SimpleNamespace(rect=_rect_at_center())
    g.flag = flag

    # Avoid level initialization side effects (signature: init_level(game))
    monkeypatch.setattr(Level, "init_level", lambda g: None)
    # Avoid music side effects used by game.update
    g.music.play_level_music = lambda *_a, **_k: None

    g.update()
    assert g.current_level == 6


def test_update_spaceship_abduction_timer_advances_level(monkeypatch):
    from internal.engine.level.level import Level

    g = _make_game()
    g.current_level = 19
    g.state = GameState.PLAYING
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    # Simulate spaceship overlapping and abduction timer passed
    abduction_rect = _rect_at_center()
    spaceship = types.SimpleNamespace(rect=_rect_at_center(), abduction_rect=abduction_rect)
    g.spaceship = spaceship
    g.player.abduction_timer = 600

    monkeypatch.setattr(Level, "init_level", lambda g: None)
    # Ensure abduction is already in progress so timer isn't reset
    g.player.is_being_abducted = True
    g.music.play_level_music = lambda *_a, **_k: None

    g.update()
    assert g.current_level == 20


def test_draw_credits_scroll_end_returns_to_main_menu(monkeypatch):
    from internal.engine.game import WIDTH, HEIGHT
    g = _make_game()
    g.state = GameState.CREDITS
    g.credits_type = "ending"
    # Simulate long scroll beyond content height; push far past threshold
    g.credits_content = ["line" for _ in range(50)]
    g.credits_scroll_y = HEIGHT + 10000

    called = {"stop": 0, "menu": 0}

    def _stop():
        called["stop"] += 1

    def _play_menu():
        called["menu"] += 1

    monkeypatch.setattr(pygame.mixer.music, "stop", _stop, raising=False)
    # Patch music subsystem used in draw()
    g.music.play_menu_music = lambda *_a, **_k: _play_menu()

    g.draw()

    assert g.state == GameState.MAIN_MENU
    assert called["stop"] == 1
    assert called["menu"] == 1


def test_update_fire_collision_hits_player_on_level_51(monkeypatch):
    g = _make_game()
    g.current_level = 51
    g.state = GameState.PLAYING
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    g.player.is_hit = False

    took_hit = {"called": 0}

    def _take_hit():
        took_hit["called"] += 1
        g.player.is_hit = True

    g.player.take_hit = _take_hit
    # Fire needs rect, x, update(camera_x) and draw(screen)
    fire = types.SimpleNamespace(rect=_rect_at_center(), x=340, update=lambda camera_x: True, draw=lambda s: None)
    g.fires = [fire]

    g.update()
    assert took_hit["called"] == 1
    assert g.player.is_hit


def test_update_bird_collision_invulnerable_explodes_enemy_and_scores(monkeypatch):
    g = _make_game()
    g.current_level = 20
    g.state = GameState.PLAYING
    g.score = 0
    g.player.is_invulnerable = True
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    # Bird dummy needs update() method
    bird = types.SimpleNamespace(rect=_rect_at_center(), x=340, y=240, update=lambda: True)
    g.birds = [bird]

    g.explosion_sound = types.SimpleNamespace(play=lambda: None)

    g.update()
    assert g.score > 0


def test_update_bird_collision_normal_causes_damage_and_game_over_flow(monkeypatch):
    g = _make_game()
    g.current_level = 20
    g.state = GameState.PLAYING
    g.player.is_invulnerable = False
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    g.birds = [types.SimpleNamespace(rect=_rect_at_center(), x=340, y=240, update=lambda: True)]

    # Avoid music and ranking prompts
    g.stop_music = lambda: None
    g.music.play_menu_music = lambda *_a, **_k: None
    g.ranking_manager.is_high_score = lambda score: False

    # Force lives to 1 so a single hit triggers game over flow
    g.lives = 1

    g.update()
    # Player should be hit and state transitions handled toward game over flow
    assert g.player.is_hit
    assert g.state in (
        GameState.GAME_OVER,
        GameState.ENTER_NAME,
        GameState.SHOW_RANKING,
        GameState.MAIN_MENU,
    )
def test_update_alien_direct_collision_invulnerable_explodes_and_scores():
    g = _make_game()
    g.current_level = 45
    g.score = 0
    g.player.is_invulnerable = True
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    alien = types.SimpleNamespace(x=340, y=240, lasers=[], rect=_rect_at_center(), update=lambda camera_x: None)
    g.aliens = [alien]

    g.update()

    assert g.score >= 60
    assert g.aliens == []


def test_update_bullet_hits_alien_transfers_lasers_and_scores():
    g = _make_game()
    g.current_level = 45
    g.score = 0
    g.player.rect = _rect_at_center()
    g.player.update = lambda *args, **kwargs: None
    # Bullet overlapping alien
    bullet = types.SimpleNamespace(rect=_rect_at_center(), x=340, y=240, draw=lambda screen: None)
    g.player.bullets = [bullet]
    # Alien with one active laser to be orphaned
    laser = types.SimpleNamespace(rect=pygame.Rect(0,0,1,1), x=340, y=240, update=lambda camera_x: True, draw=lambda s: None)
    alien = types.SimpleNamespace(x=340, y=240, lasers=[laser], rect=_rect_at_center(), update=lambda camera_x: None)
    g.aliens = [alien]
    # Stub sfx to avoid audio
    g.sound_effects.play_sound_effect = lambda *_a, **_k: None

    g.update()

    assert g.score >= 60
    assert laser in g.orphan_lasers
    assert g.player.bullets == []
    assert g.aliens == []
import os
@pytest.fixture(autouse=True)
def init_pygame_display():
    if not pygame.get_init():
        pygame.init()
    if not pygame.display.get_init():
        pygame.display.init()
    pygame.display.set_mode((1, 1))
    yield


@pytest.fixture(autouse=True)
def disable_mixer(monkeypatch):
    from internal.engine.sound.mixer import Mixer
    monkeypatch.setattr(Mixer, "init", lambda *args, **kwargs: None)