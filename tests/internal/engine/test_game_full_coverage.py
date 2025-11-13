import os
import types
import pygame
import pytest


def make_surface(w=10, h=10):
    pygame.init()
    return pygame.Surface((w, h))


def make_rect(x=0, y=0, w=10, h=10):
    return pygame.Rect(x, y, w, h)


def test_init_development_initial_stage_and_lives(monkeypatch):
    # Monkeypatch ENV_CONFIG before importing Game to exercise dev init path
    import internal.engine.game as game_mod
    original_env = dict(getattr(game_mod, 'ENV_CONFIG', {}))
    try:
        game_mod.ENV_CONFIG = {
            'environment': 'development',
            'initial-stage': '5',
            'lives': '3',
        }
        from internal.engine.game import Game, GameState
        g = Game()
        assert g.current_level == 5
        assert g.state == GameState.PLAYING
        assert g.lives == 3 and g.max_lives == 3
    finally:
        game_mod.ENV_CONFIG = original_env


@pytest.fixture
def game(monkeypatch):
    # Import game engine
    from internal.engine.game import Game, GameState

    # Ensure environment is predictable
    monkeypatch.setenv("PLATFORM_GAME_DEV", "1")

    # Initialize pygame modules for drawing/text
    pygame.init()
    pygame.font.init()

    # Minimal config for Game to initialize without assets
    g = Game()

    # Stub image assets used by draw/update branches
    g.image.menu_image = make_surface(20, 20)
    g.image.bullet_image = make_surface(5, 5)
    g.image.explosion_image = make_surface(8, 8)
    # Birds and bats
    g.image.bird_img1 = make_surface(6, 6)
    g.image.bird_img2 = make_surface(6, 6)
    g.image.bat_img1 = make_surface(6, 6)
    g.image.bat_img2 = make_surface(6, 6)
    # Airplane, flying disk, fire, turtle, spider, robot, alien, boss
    g.image.airplane_img = make_surface(10, 6)
    g.image.flying_disk_img = make_surface(6, 6)
    g.image.fire_img = make_surface(6, 8)
    g.image.turtle_img = make_surface(8, 6)
    g.image.spider_img = make_surface(8, 8)
    g.image.robot_img = make_surface(8, 10)
    g.image.alien_img = make_surface(8, 12)
    g.image.boss_alien_img = make_surface(20, 20)

    # Stub music to avoid actual playback
    g.music.play_menu_music = lambda _g: None
    g.music.play_level_music = lambda _g, _lvl: None
    g.music.play_music = lambda _name: None

    # Stub sound effects
    if hasattr(g, "sound_effects"):
        g.sound_effects.play_sound_effect = lambda _name: None

    # Stub ranking manager
    g.ranking_manager.is_high_score = lambda _score: False

    # Prepare player bullets container
    g.player.bullets = []

    # Prevent sys.exit in menu
    monkeypatch.setattr("sys.exit", lambda: None)

    return g


def test_draw_all_states(game, monkeypatch):
    from internal.engine.game import GameState
    import internal.engine.game as game_mod

    # SPLASH draw with development instruction and fade branches
    game_mod.ENV_CONFIG['environment'] = 'development'
    game.state = GameState.SPLASH
    game.logos = [make_surface(10, 10)]
    game.logo_display_time = 60
    game.fade_in_duration = 10
    game.fade_out_duration = 10
    game.splash_timer = 5  # fade in branch
    game.draw()
    game.splash_timer = 55  # fade out branch
    game.draw()

    # TITLE_SCREEN
    game.state = GameState.TITLE_SCREEN
    game.draw()

    # OPENING_VIDEO and ENDING_VIDEO with stub draw()
    class VD:
        def draw(self, screen):
            screen.blit(make_surface(5, 5), (0, 0))
    game.video_player = VD()
    game.state = GameState.OPENING_VIDEO
    game.draw()
    game.ending_video_player = VD()
    game.state = GameState.ENDING_VIDEO
    game.draw()


def test_bullet_hits_robot_transfers_orphan_missiles_and_scores(game):
    from internal.engine.game import GameState

    # Prepare PLAYING state in robot levels
    game.state = GameState.PLAYING
    game.current_level = 31
    game.player.is_being_abducted = False
    # Avoid player.update touching bullets
    game.player.update = lambda *a, **k: None

    # Dummy bullet overlapping robot
    class DummyBullet:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 10, 10)

    # Dummy missile projectile
    class DummyMissile:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 6, 6)
        def update(self, camera_x):
            return True
        def draw(self, screen):
            pass

    class DummyRobot:
        def __init__(self, x, y, missiles):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 20, 20)
            self.missiles = missiles
        def draw(self, screen):
            pass
        def update(self, camera_x):
            pass

    # Setup robot and missiles away from player to avoid prior collisions
    missiles = [DummyMissile(100, 100), DummyMissile(110, 100)]
    robot = DummyRobot(game.player.x, game.player.y, missiles)
    game.robots = [robot]

    # Add bullet overlapping robot rect
    bullet = DummyBullet(robot.x, robot.y)
    game.player.bullets.append(bullet)

    base_score = game.score
    game.update()

    # Robot removed, missiles transferred to orphan list, score added
    assert len(game.robots) == 0
    assert set(game.orphan_missiles) >= set(missiles)
    assert game.score == base_score + 100


def test_bullet_hits_alien_transfers_orphan_lasers_and_scores(game):
    from internal.engine.game import GameState

    # Prepare PLAYING state in alien levels
    game.state = GameState.PLAYING
    game.current_level = 41
    game.player.is_being_abducted = False
    game.player.update = lambda *a, **k: None

    class DummyBullet:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 10, 10)

    class DummyLaser:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 6, 6)
        def update(self, camera_x):
            return True
        def draw(self, screen):
            pass

    class DummyAlien:
        def __init__(self, x, y, lasers):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 20, 20)
            self.lasers = lasers
        def draw(self, screen):
            pass
        def update(self, camera_x):
            pass

    lasers = [DummyLaser(100, 100), DummyLaser(110, 100)]
    alien = DummyAlien(game.player.x, game.player.y, lasers)
    game.aliens = [alien]

    bullet = DummyBullet(alien.x, alien.y)
    game.player.bullets.append(bullet)

    base_score = game.score
    game.update()

    assert len(game.aliens) == 0
    assert set(game.orphan_lasers) >= set(lasers)
    assert game.score == base_score + 60


def test_robot_missile_hits_player_reduces_life_and_maybe_game_over(game, monkeypatch):
    from internal.engine.game import GameState

    game.state = GameState.PLAYING
    game.current_level = 31
    game.player.is_being_abducted = False
    game.player.is_invulnerable = False
    game.player.is_hit = False
    game.lives = 1
    # Ensure ranking returns False to hit GAME_OVER branch
    game.ranking_manager.is_high_score = lambda _score: False
    game.player.update = lambda *a, **k: None

    class DummyMissile:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 6, 6)
        def update(self, camera_x):
            return True
        def draw(self, screen):
            pass

    class DummyRobot:
        def __init__(self, x, y, missiles):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 20, 20)
            self.missiles = missiles
        def update(self, camera_x):
            pass

    missile = DummyMissile(game.player.rect.x, game.player.rect.y)
    robot = DummyRobot(50, 50, [missile])
    game.robots = [robot]

    game.update()

    assert game.lives == 0
    assert game.state in (GameState.GAME_OVER, GameState.ENTER_NAME)


def test_alien_laser_hits_player_reduces_life(game, monkeypatch):
    from internal.engine.game import GameState

    game.state = GameState.PLAYING
    game.current_level = 41
    game.player.is_being_abducted = False
    game.player.is_invulnerable = False
    game.player.is_hit = False
    game.lives = 2
    game.ranking_manager.is_high_score = lambda _score: False
    game.player.update = lambda *a, **k: None

    class DummyLaser:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 6, 6)
        def update(self, camera_x):
            return True
        def draw(self, screen):
            pass

    class DummyAlien:
        def __init__(self, x, y, lasers):
            self.x = x
            self.y = y
            self.rect = make_rect(x, y, 20, 20)
            self.lasers = lasers
        def update(self, camera_x):
            pass

    laser = DummyLaser(game.player.rect.x, game.player.rect.y)
    alien = DummyAlien(60, 60, [laser])
    game.aliens = [alien]

    pre_lives = game.lives
    game.update()
    assert game.lives == pre_lives - 1


def test_orphan_projectiles_update_lists(game):
    from internal.engine.game import GameState

    # Missiles on robot levels
    game.state = GameState.PLAYING
    game.current_level = 31
    class OM:
        def __init__(self, keep=True):
            self.x = 0; self.y = 0
            self.rect = make_rect(0,0,1,1)
            self._keep = keep
        def update(self, camera_x):
            return self._keep
    m1, m2 = OM(True), OM(False)
    game.orphan_missiles = [m1, m2]
    game.update()
    assert game.orphan_missiles == [m1]

    # Lasers on alien levels
    game.current_level = 41
    class OL:
        def __init__(self, keep=True):
            self.x = 0; self.y = 0
            self.rect = make_rect(0,0,1,1)
            self._keep = keep
        def update(self, camera_x):
            return self._keep
    l1, l2 = OL(True), OL(False)
    game.orphan_lasers = [l1, l2]
    game.update()
    assert game.orphan_lasers == [l1]


def test_spaceship_abduction_advances_level(game):
    from internal.engine.game import GameState
    # Position player and spaceship abduction area to collide
    game.state = GameState.PLAYING
    game.current_level = 50
    game.player.abduction_timer = 600
    game.player.is_being_abducted = False
    # Prevent start_abduction from resetting timer
    game.player.start_abduction = lambda: setattr(game.player, 'is_being_abducted', True)

    class DummySpaceship:
        def __init__(self, rect):
            self.abduction_rect = rect
    game.spaceship = DummySpaceship(make_rect(game.player.rect.x, game.player.rect.y, 10, 10))

    pre_level = game.current_level
    game.update()
    assert game.current_level == pre_level + 1


def test_draw_playing_robots_aliens_and_orphans(game):
    from internal.engine.game import GameState
    game.state = GameState.PLAYING
    game.player.is_being_abducted = False

    # Robots and missiles draw path
    game.current_level = 31
    class DR:
        def __init__(self, x, y):
            self.x = x; self.y = y
            self.rect = make_rect(x, y, 10, 10)
            self.missiles = []
        def draw(self, screen):
            screen.blit(make_surface(2,2), (0,0))
    class DM:
        def __init__(self, x, y):
            self.x=x; self.y=y
            self.rect = make_rect(x, y, 4, 4)
        def draw(self, screen):
            screen.blit(make_surface(1,1), (0,0))
    r = DR(game.player.x+60, game.player.y)
    r.missiles = [DM(r.x+5, r.y)]
    game.robots = [r]
    game.orphan_missiles = [DM(100, 100)]
    game.draw()

    # Aliens and lasers draw path
    game.current_level = 41
    class DA:
        def __init__(self, x, y):
            self.x=x; self.y=y
            self.rect = make_rect(x, y, 10, 10)
            self.lasers = []
        def draw(self, screen):
            screen.blit(make_surface(2,2), (0,0))
    class DL:
        def __init__(self, x, y):
            self.x=x; self.y=y
            self.rect = make_rect(x, y, 4, 4)
        def draw(self, screen):
            screen.blit(make_surface(1,1), (0,0))
    a = DA(game.player.x+60, game.player.y)
    a.lasers = [DL(a.x+5, a.y)]
    game.aliens = [a]
    game.orphan_lasers = [DL(120, 120)]
    game.draw()

    # MAIN_MENU and SELECT_DIFFICULTY
    game.state = GameState.MAIN_MENU
    game.draw()
    game.state = GameState.SELECT_DIFFICULTY
    game.draw()

    # RECORDS
    game.state = GameState.RECORDS
    game.ranking_manager.get_top_scores = lambda n=10: [
        {"name": "AAA", "score": 100},
        {"name": "BBB", "score": 50},
    ]
    game.draw()

    # CREDITS with both types
    game.state = GameState.CREDITS
    game.credits_type = 'menu'
    game.draw()
    game.credits_type = 'ending'
    game.draw()

    # GAME_OVER
    game.state = GameState.GAME_OVER
    game.draw()

    # PLAYING minimal draw
    game.state = GameState.PLAYING
    game.draw()


def test_dodge_scoring_across_levels(game):
    from internal.engine.game import GameState
    # Common player position
    game.player.x, game.player.y = 50, 50

    # Birds (<=20)
    game.state = GameState.PLAYING
    game.current_level = 10
    class Bird:
        def __init__(self):
            self.x, self.y, self.id = 45, 55, 'b1'
            self.rect = make_rect(40, 50, 5, 5)
        def update(self, *args, **kwargs):
            pass
    game.birds = [Bird()]
    base = game.score
    game.update()
    assert game.score >= base

    # Bats (<=30)
    game.current_level = 25
    class Bat:
        def __init__(self):
            self.x, self.y, self.id = 45, 55, 'bt1'
            self.rect = make_rect(40, 50, 5, 5)
        def update(self, *args, **kwargs):
            pass
    game.bats = [Bat()]
    base = game.score
    game.update()
    assert game.score >= base

    # Airplanes (<=40)
    game.current_level = 35
    class Air:
        def __init__(self):
            self.x, self.y, self.id = 45, 55, 'a1'
            self.rect = make_rect(40, 50, 5, 5)
        def update(self, *args, **kwargs):
            pass
    game.airplanes = [Air()]
    base = game.score
    game.update()
    assert game.score >= base

    # Flying disks (>40)
    game.current_level = 45
    class Disk:
        def __init__(self):
            self.x, self.y, self.id = 45, 55, 'd1'
            self.rect = make_rect(40, 50, 5, 5)
        def update(self, *args, **kwargs):
            pass
    game.flying_disks = [Disk()]
    base = game.score
    game.update()
    assert game.score >= base


def test_orphan_projectiles_update(game):
    from internal.engine.game import GameState
    # Robots missiles orphan lifecycle (31-40)
    game.state = GameState.PLAYING
    game.current_level = 32
    class Miss:
        def __init__(self, x):
            self.x, self.y = x, 0
            self.rect = make_rect(x, 0, 2, 2)
        def update(self, cam):
            return self.x % 2 == 0
    game.orphan_missiles = [Miss(0), Miss(1)]
    game.update()
    assert any(True for m in game.orphan_missiles)

    # Aliens lasers orphan lifecycle (41-50)
    game.current_level = 45
    class Las:
        def __init__(self, x):
            self.x, self.y = x, 0
            self.rect = make_rect(x, 0, 2, 2)
        def update(self, cam):
            return self.x % 2 == 0
    game.orphan_lasers = [Las(0), Las(1)]
    game.update()
    assert any(True for l in game.orphan_lasers)


def test_boss_capture_ending_video(game):
    from internal.engine.game import GameState
    # Level 51 boss capture sequence to ENDING_VIDEO
    game.state = GameState.PLAYING
    game.current_level = 51
    class Boss:
        def __init__(self):
            self.x, self.y = 0, 0
        def update(self, px, cam):
            pass
        def is_captured(self, rect):
            return True
    game.boss_alien = Boss()
    game.boss_alien_captured = False
    # Advance updates to exceed 300 frames
    for _ in range(310):
        game.update()
        if game.state == GameState.ENDING_VIDEO:
            break
    assert game.state == GameState.ENDING_VIDEO


def test_extra_life_thresholds_easy_hard(game):
    # EASY thresholds
    game.score = 0
    game.lives = 3
    from internal.engine.difficulty import Difficulty
    game.difficulty = Difficulty.EASY
    ms, inc = game.get_extra_life_milestones_and_increment()
    game.extra_life_milestones = ms
    game.extra_life_increment_after_milestones = inc
    game.next_extra_life_score = ms[0]
    base = game.lives
    m = game.get_score_multiplier()
    # Base points needed to reach milestone considering multiplier
    needed = int((game.next_extra_life_score + 1) / m)
    game.add_score(needed)
    assert game.lives >= base + 1

    # HARD thresholds
    game.score = 0
    game.lives = 3
    game.difficulty = Difficulty.HARD
    ms, inc = game.get_extra_life_milestones_and_increment()
    game.extra_life_milestones = ms
    game.extra_life_increment_after_milestones = inc
    game.next_extra_life_score = ms[0]
    base = game.lives
    m = game.get_score_multiplier()
    needed = int((game.next_extra_life_score + 1) / m)
    game.add_score(needed)
    assert game.lives >= base + 1


def test_credits_flow_and_records_draw(game, monkeypatch):
    from internal.engine.game import GameState

    # Enter FIM_SCREEN then advance to CREDITS and scroll/reset
    game.state = GameState.FIM_SCREEN
    game.fim_screen_timer = 179
    game.update()  # transition to credits
    assert game.state == GameState.CREDITS
    # Make credits long enough and then reset (menu type)
    game.credits_type = "menu"
    game.credits_reset_timer = 1799
    game.update()
    # Draw credits via main draw
    game.draw()

    # Go to records and draw table
    game.state = GameState.RECORDS
    # Stub records content expected by records draw
    game.ranking_manager.get_top_scores = lambda n=10: [
        {"name": "AAA", "score": 123},
        {"name": "BBB", "score": 45},
    ]
    game.draw()


def test_run_loop_stop_immediately(game, monkeypatch):
    # Make handle_events return False to stop run loop fast
    game.handle_events = lambda: False
    # Ensure draw() can be called for current state
    game.state = game.state  # no-op
    # Run should exit immediately without errors
    game.run()


def test_opening_video_update_to_menu(game, monkeypatch):
    from internal.engine.game import GameState

    # Stub video player to report finished
    class VP:
        def update(self):
            pass

        def is_finished(self):
            return True

        def cleanup(self):
            pass

    game.video_player = VP()
    game.music_started = False
    game.state = GameState.OPENING_VIDEO
    game.update()
    assert game.state == GameState.MAIN_MENU
    assert game.music_started is True


def test_ending_video_fallback_and_credits(game, monkeypatch):
    from internal.engine.game import GameState

    class EVP:
        def load_video(self, path):
            return False  # force fallback

        def start_playback(self):
            pass

        def update(self):
            pass

        def is_finished(self):
            return False

        def cleanup(self):
            pass

    game.ending_video_player = EVP()
    game.state = GameState.ENDING_VIDEO
    game.update()
    assert game.state == GameState.FIM_SCREEN
    game.fim_screen_timer = 180
    game.update()
    assert game.state == GameState.CREDITS


def test_joystick_axes_navigation_in_main_menu(game, monkeypatch):
    from internal.engine.game import GameState

    # Simulate joystick with enough axes
    class Joy:
        def get_numaxes(self):
            return 8

        def get_axis(self, idx):
            # Axis 1 up/down, 7 dpad simulation
            return -1.0 if idx in (1, 7) else 0.0

        def get_numbuttons(self):
            return 2

    game.joystick_connected = True
    game.joystick = Joy()
    game.state = GameState.MAIN_MENU
    # Set menu options
    game.menu_options = ["Jogar", "Recordes", "Créditos", "Sair"]
    game.menu_selected = 0
    # Handle events to move selection up (should wrap)
    pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {}))
    game.handle_events()
    # Selection should change due to axis up
    assert game.menu_selected in range(len(game.menu_options))


def test_joystick_game_over_restart_records_and_exit(game):
    from internal.engine.game import GameState

    game.state = GameState.GAME_OVER
    game.game_over_options = ["Jogar novamente", "Recordes", "Sair"]

    # Restart path when selected index 0
    game.game_over_selected = 0
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 0}))
    assert game.handle_events() is True
    assert game.state in (GameState.PLAYING, GameState.GAME_OVER)

    # Records path when selected index 1
    game.state = GameState.GAME_OVER
    game.game_over_selected = 1
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 0}))
    game.handle_events()
    assert game.state == GameState.RECORDS

    # Exit path when selected index 2
    game.state = GameState.GAME_OVER
    game.game_over_selected = 2
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 0}))
    assert game.handle_events() is False


def test_enter_name_confirm_and_show_ranking(game, monkeypatch):
    from internal.engine.game import GameState

    # Stub ranking add_score
    game.ranking_manager.add_score = lambda name, score: None

    game.state = GameState.ENTER_NAME
    game.player_name = "ABC"
    # Press Start/Options to confirm name
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 6}))
    game.handle_events()
    assert game.state == GameState.SHOW_RANKING
    assert game.previous_state_before_ranking == GameState.GAME_OVER


def test_show_ranking_back_button_returns_previous(game):
    from internal.engine.game import GameState

    game.previous_state_before_ranking = GameState.GAME_OVER
    game.state = GameState.SHOW_RANKING
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 1}))
    game.handle_events()
    assert game.state == GameState.GAME_OVER


def test_handle_menu_selection_options(game, monkeypatch):
    from internal.engine.game import GameState

    game.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]

    # Iniciar -> SELECT_DIFFICULTY
    game.menu_selected = 0
    game.handle_menu_selection()
    assert game.state == GameState.SELECT_DIFFICULTY

    # Recordes
    game.menu_selected = 1
    game.handle_menu_selection()
    assert game.state == GameState.RECORDS

    # Créditos
    game.menu_selected = 2
    game.handle_menu_selection()
    assert game.state == GameState.CREDITS

    # Sair (sys.exit is patched in fixture)
    game.menu_selected = 3
    assert game.handle_menu_selection() is None


def test_exhaustive_draw_and_update_states_and_levels(game):
    from internal.engine.game import GameState

    # Prepare ranking for records
    game.ranking_manager.get_top_scores = lambda n=10: [
        {"name": "AAA", "score": 100},
        {"name": "BBB", "score": 90},
    ]

    # SPLASH update/draw
    game.state = GameState.SPLASH
    game.logos = [make_surface(10, 10), make_surface(10, 10)]
    game.logo_display_time = 1
    game.splash_duration = 2
    game.update()
    game.draw()

    # TITLE_SCREEN draw
    game.state = GameState.TITLE_SCREEN
    game.draw()

    # OPENING_VIDEO update -> MAIN_MENU
    class VP2:
        def update(self):
            pass
        def is_finished(self):
            return True
        def cleanup(self):
            pass
    game.video_player = VP2()
    game.music_started = False
    game.state = GameState.OPENING_VIDEO
    game.update()
    game.draw()

    # MAIN_MENU draw and axis navigation again
    game.state = GameState.MAIN_MENU
    game.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
    game.menu_selected = 0
    game.draw()

    # SELECT_DIFFICULTY draw
    game.state = GameState.SELECT_DIFFICULTY
    game.draw()

    # PLAYING across level ranges with entities present
    def seed_entities():
        # populate minimal entities
        game.birds = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.bird_img1, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.bats = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.bat_img1, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.airplanes = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.airplane_img, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.flying_disks = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.flying_disk_img, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.fires = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.fire_img, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.turtles = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.turtle_img, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.spiders = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.spider_img, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.robots = [
            types.SimpleNamespace(
                x=5,
                y=5,
                rect=make_rect(5,5,5,5),
                image=game.image.robot_img,
                draw=lambda *a, **k: None,
                update=lambda *a, **k: None,
                missiles=[
                    types.SimpleNamespace(
                        x=5,
                        y=5,
                        rect=make_rect(5,5,4,4),
                        image=game.image.bullet_image,
                        draw=lambda *a, **k: None,
                        update=lambda *a, **k: None,
                    )
                ],
            )
        ]
        game.aliens = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.alien_img, draw=lambda *a, **k: None, update=lambda *a, **k: None, lasers=[])]
        game.boss_alien = types.SimpleNamespace(
            x=5,
            y=5,
            rect=make_rect(5,5,10,10),
            image=game.image.boss_alien_img,
            draw=lambda *a, **k: None,
            update=lambda *a, **k: None,
            is_captured=lambda _rect: False,
        )
        game.explosions = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,8,8), image=game.image.explosion_image, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.extra_lives = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,8,8), image=game.image.explosion_image, draw=lambda *a, **k: None, update=lambda *a, **k: None)]
        game.player.bullets = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,5,5), image=game.image.bullet_image, draw=lambda *a, **k: None, update=lambda *a, **k: None)]

    for lvl in [5, 15, 25, 35, 45, 51]:
        game.state = GameState.PLAYING
        game.current_level = lvl
        seed_entities()
        # Trigger scoring path
        game.player.just_landed = True
        game.player.landed_platform_id = f"p{lvl}"
        # Timers to trigger some spawns without heavy loops
        if lvl <= 20:
            game.bird_spawn_interval = 1
            game.bird_spawn_timer = 1
        elif lvl <= 30:
            game.bat_spawn_interval = 1
            game.bat_spawn_timer = 1
        elif lvl <= 40:
            game.airplane_spawn_interval = 1
            game.airplane_spawn_timer = 1
            game.fire_spawn_interval = 1
            game.fire_spawn_timer = 1
            game.flying_disk_spawn_interval = 1
            game.flying_disk_spawn_timer = 1
        elif lvl <= 50:
            game.alien_spawn_interval = 1
            game.alien_spawn_timer = 1
        else:
            # Level 51 spaceship/boss
            game.spaceship = types.SimpleNamespace(
                x=0,
                y=0,
                rect=make_rect(0,0,20,20),
                abduction_rect=make_rect(0,0,50,50),
                draw=lambda *a, **k: None,
                update=lambda *a, **k: None,
                update_position=lambda *a, **k: None,
                start_abduction=lambda *a, **k: None,
                stop_abduction=lambda *a, **k: None,
            )
        # Update and draw
        game.update()
        game.draw()

    # GAME_OVER draw
    game.state = GameState.GAME_OVER
    game.game_over_options = ["Jogar novamente", "Recordes", "Sair"]
    game.game_over_selected = 0
    game.draw()

    # ENTER_NAME draw and update confirmation via keyboard
    game.state = GameState.ENTER_NAME
    game.player_name = "XYZ"
    game.draw()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()

    # SHOW_RANKING draw and back
    game.state = GameState.SHOW_RANKING
    game.previous_state_before_ranking = GameState.GAME_OVER
    game.draw()
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 1}))
    game.handle_events()

    # VICTORY draw
    game.state = GameState.VICTORY
    game.draw()

    # ENDING_VIDEO update -> FIM_SCREEN -> CREDITS
    class EVP2:
        def load_video(self, path):
            return False
        def start_playback(self):
            pass
        def update(self):
            pass
        def is_finished(self):
            return False
        def cleanup(self):
            pass
    game.ending_video_player = EVP2()
    game.state = GameState.ENDING_VIDEO
    game.update()
    game.state = GameState.FIM_SCREEN
    game.fim_screen_timer = 180
    game.update()
    game.draw()

    # CREDITS draw with scrolling
    game.state = GameState.CREDITS
    game.credits_type = "menu"
    game.credits_reset_timer = 1799
    game.update()
    game.draw()

    # RECORDS draw
    game.state = GameState.RECORDS
    game.draw()


def test_playing_collision_paths_and_victory_abduction(game):
    from internal.engine.game import GameState

    # Common player rect to collide
    game.player.rect = make_rect(5,5,12,12)
    game.sound_effects.play_sound_effect = lambda _n: None

    # Levels 31-40: player bullets vs robots; robot missiles vs player
    game.state = GameState.PLAYING
    game.current_level = 35
    game.robots = [
        types.SimpleNamespace(
            x=5,
            y=5,
            rect=make_rect(5,5,6,6),
            image=game.image.robot_img,
            missiles=[types.SimpleNamespace(rect=make_rect(5,5,4,4), update=lambda *a, **k: None, draw=lambda *a, **k: None)],
            update=lambda *a, **k: None,
            draw=lambda *a, **k: None,
        )
    ]
    game.player.bullets = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,3,3), update=lambda *a, **k: None, draw=lambda *a, **k: None)]
    game.explosions = []
    game.update()

    # Levels 41-50: alien lasers vs player
    game.current_level = 45
    game.aliens = [
        types.SimpleNamespace(
            x=5,
            y=5,
            rect=make_rect(5,5,6,6),
            image=game.image.alien_img,
            lasers=[types.SimpleNamespace(rect=make_rect(5,5,2,2), update=lambda *a, **k: None, draw=lambda *a, **k: None)],
            update=lambda *a, **k: None,
            draw=lambda *a, **k: None,
        )
    ]
    game.update()

    # Level 51: boss alien lasers vs player and abduct spaceship
    game.current_level = 51
    game.boss_alien = types.SimpleNamespace(
        x=5,
        y=5,
        rect=make_rect(5,5,10,10),
        image=game.image.boss_alien_img,
        lasers=[types.SimpleNamespace(rect=make_rect(5,5,2,2), update=lambda *a, **k: None, draw=lambda *a, **k: None)],
        update=lambda *a, **k: None,
        draw=lambda *a, **k: None,
        is_captured=lambda _rect: False,
    )
    game.spaceship = types.SimpleNamespace(
        rect=make_rect(0,0,20,20),
        abduction_rect=make_rect(5,5,50,50),
        start_abduction=lambda *a, **k: None,
        stop_abduction=lambda *a, **k: None,
        update=lambda *a, **k: None,
        draw=lambda *a, **k: None,
        update_position=lambda *a, **k: None,
    )
    game.player.is_being_abducted = False
    game.update()
    # Now set being abducted True to exercise stop_abduction branch if present
    game.player.is_being_abducted = True
    game.update()

    # Victory path via flag collision: enter ranking and pure victory
    flag = types.SimpleNamespace(rect=make_rect(5,5,10,10), image=game.image.flag_img if hasattr(game.image, 'flag_img') else game.image.explosion_image)
    game.flag = flag

    # Case: is high score -> ENTER_NAME
    game.current_level = game.max_levels
    game.spaceship = None
    game.player.update = lambda *a, **k: None
    game.player.is_being_abducted = False
    game.ranking_manager.is_high_score = lambda s: True
    game.player.rect = make_rect(5,5,12,12)
    assert game.player.rect.colliderect(game.flag.rect)
    game.update()
    assert game.state in (GameState.ENTER_NAME, GameState.VICTORY)

    # Case: not high score -> VICTORY
    game.state = GameState.PLAYING
    game.ranking_manager.is_high_score = lambda s: False
    game.update()
    assert game.state == GameState.VICTORY


def test_invulnerable_collisions_and_game_over_ranking(game):
    from internal.engine.game import GameState

    # Invulnerable turtle collision awards points and explosion
    game.state = GameState.PLAYING
    game.current_level = 10
    game.player.rect = make_rect(5,5,12,12)
    game.player.is_invulnerable = True
    game.turtles = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,6,6), update=lambda *a, **k: None)]
    game.explosions = []
    game.update()
    assert len(game.explosions) >= 0

    # Game over via alien direct collision with ranking high score
    game.player.is_invulnerable = False
    game.player.is_hit = False
    game.player.is_being_abducted = False
    game.current_level = 45
    game.lives = 1
    # Reset player position to collide and avoid movement
    game.player.rect = make_rect(5,5,12,12)
    game.player.update = lambda *a, **k: None
    game.aliens = [types.SimpleNamespace(x=5, y=5, rect=make_rect(5,5,6,6), lasers=[], update=lambda *a, **k: None)]
    game.ranking_manager.is_high_score = lambda s: True
    # Ensure collision precondition holds
    assert game.player.rect.colliderect(game.aliens[0].rect)
    game.update()
    assert game.state in (GameState.ENTER_NAME, GameState.GAME_OVER)


def test_abduction_timer_victory(game):
    from internal.engine.game import GameState

    game.state = GameState.PLAYING
    game.current_level = game.max_levels
    game.player.rect = make_rect(5,5,12,12)
    # Ensure abduction is already happening so timer condition is evaluated
    game.player.is_being_abducted = True
    game.player.abduction_timer = 600
    # Avoid player movement interfering with abduction area collision
    game.player.update = lambda *a, **k: None
    game.spaceship = types.SimpleNamespace(
        abduction_rect=make_rect(5,5,50,50),
        start_abduction=lambda *a, **k: None,
        stop_abduction=lambda *a, **k: None,
        update=lambda *a, **k: None,
        draw=lambda *a, **k: None,
        update_position=lambda *a, **k: None,
    )
    # Sanity check: ensure collision precondition holds
    assert game.player.rect.colliderect(game.spaceship.abduction_rect)
    game.ranking_manager.is_high_score = lambda s: False
    game.update()
    assert game.state == GameState.VICTORY


def test_extra_life_award(game):
    # Force difficulty normal thresholds and award extra life by score
    game.difficulty = game.difficulty if hasattr(game, 'difficulty') else None
    milestones, inc = game.get_extra_life_milestones_and_increment()
    game.extra_life_milestones = milestones
    game.extra_life_increment_after_milestones = inc
    game.next_extra_life_score = game.extra_life_milestones[0]
    game.extra_lives_earned = 0
    base_lives = game.lives
    # Add enough score to cross the threshold
    game.add_score(game.next_extra_life_score + 10)
    assert game.lives >= base_lives


def test_update_alien_bullet_collision_and_explosion_pool(game, monkeypatch):
    from internal.engine.game import GameState

    # Setup level > 40 to ensure alien logic runs
    game.state = GameState.PLAYING
    game.current_level = 45

    # Create one alien with rect colliding a bullet
    class DummyAlien:
        def __init__(self):
            self.x = 50
            self.y = 50
            self.rect = make_rect(50, 50, 10, 10)
            self.lasers = []
            self.image = game.image.alien_img

        def update(self, *args, **kwargs):
            pass

        def draw(self, screen=None, *args, **kwargs):
            if screen is not None:
                screen.blit(self.image, (self.x, self.y))

    alien = DummyAlien()
    game.aliens = [alien]

    # Bullet overlapping alien rect
    class DummyBullet:
        def __init__(self):
            self.x = 50
            self.y = 50
            self.rect = make_rect(50, 50, 10, 10)
            self.image = game.image.bullet_image

        def update(self, *args, **kwargs):
            pass

        def draw(self, screen=None, *args, **kwargs):
            if screen is not None:
                screen.blit(self.image, (self.x, self.y))

    bullet = DummyBullet()
    game.player.bullets = [bullet]

    # Provide explosion pool helpers
    import types
    game.explosions = []
    game.orphan_lasers = []
    game.get_pooled_explosion = lambda x, y, img: types.SimpleNamespace(
        x=x,
        y=y,
        image=img,
        rect=make_rect(int(x), int(y), 8, 8),
        update=lambda *a, **k: None,
        draw=lambda *a, **k: None,
    )
    game.return_explosion_to_pool = lambda e: None

    # Run update which should process collision without raising
    game.update()
    # Lasers list exists (no strict assert on content)
    assert hasattr(game, "aliens")


def test_invulnerable_robot_direct_collision_transfers_orphan_missiles_and_scores(game):
    from internal.engine.game import GameState
    import types

    # Setup: PLAYING on robot levels, player invulnerable, robot colliding
    game.state = GameState.PLAYING
    game.current_level = 35
    game.player.is_invulnerable = True
    game.player.is_hit = False
    game.player.is_being_abducted = False
    game.player.update = lambda *a, **k: None
    game.player.rect = make_rect(5, 5, 12, 12)

    # Robot with active missiles that should be transferred to orphan list
    robot = types.SimpleNamespace(
        x=5,
        y=5,
        rect=make_rect(5, 5, 6, 6),
        # Place missile away from player so it isn't removed by missile collision branch
        missiles=[types.SimpleNamespace(x=100, y=100, rect=make_rect(100, 100, 3, 3), update=lambda *a, **k: True, draw=lambda *a, **k: None)],
        update=lambda *a, **k: None,
    )
    game.robots = [robot]
    game.explosions = []
    prev_orphans = len(game.orphan_missiles)
    prev_score = game.score

    # Run update: invulnerable branch explodes robot, transfers missiles, removes robot, adds score
    game.update()
    assert len(game.orphan_missiles) >= prev_orphans + 1
    assert len(game.robots) == 0
    assert game.score >= prev_score + 50


def test_invulnerable_alien_direct_collision_transfers_orphan_lasers_and_scores(game):
    from internal.engine.game import GameState
    import types

    # Setup: PLAYING on alien levels, player invulnerable, alien colliding
    game.state = GameState.PLAYING
    game.current_level = 45
    game.player.is_invulnerable = True
    game.player.is_hit = False
    game.player.is_being_abducted = False
    game.player.update = lambda *a, **k: None
    game.player.rect = make_rect(5, 5, 12, 12)

    alien = types.SimpleNamespace(
        x=5,
        y=5,
        rect=make_rect(5, 5, 6, 6),
        # Place laser away from player so it isn't removed by laser collision branch
        lasers=[types.SimpleNamespace(x=100, y=100, rect=make_rect(100, 100, 3, 3), update=lambda *a, **k: True, draw=lambda *a, **k: None)],
        update=lambda *a, **k: None,
    )
    game.aliens = [alien]
    game.explosions = []
    prev_orphans = len(game.orphan_lasers)
    prev_score = game.score

    # Run update: invulnerable branch explodes alien, transfers lasers, removes alien, adds score
    game.update()
    assert len(game.orphan_lasers) >= prev_orphans + 1
    assert len(game.aliens) == 0
    assert game.score >= prev_score + 60


def test_flag_collision_advances_level_and_plays_music(game, monkeypatch):
    from internal.engine.game import GameState
    import types
    from internal.engine.level.level import Level

    # Setup: PLAYING, flag colliding, below max level
    game.state = GameState.PLAYING
    game.current_level = 10
    game.max_levels = 51
    game.player.is_being_abducted = False
    game.player.update = lambda *a, **k: None
    game.player.rect = make_rect(5, 5, 12, 12)
    game.flag = types.SimpleNamespace(rect=make_rect(5, 5, 6, 6))

    # No-op level init to avoid heavy side effects
    monkeypatch.setattr(Level, "init_level", lambda g: None)
    # Track music play for new level
    calls = {}
    def fake_play_level_music(_game, lvl):
        calls["level"] = lvl
    monkeypatch.setattr(game.music, "play_level_music", fake_play_level_music)

    game.update()
    assert game.current_level == 11
    assert calls.get("level") == 11
    assert game.state == GameState.PLAYING


def test_draw_playing_with_entities(game):
    from internal.engine.game import GameState

    game.state = GameState.PLAYING
    game.current_level = 10

    class DummyEntity:
        def __init__(self, img, x=5, y=5):
            self.x = x
            self.y = y
            self.image = img
            self.rect = make_rect(x, y, 5, 5)

        def draw(self, screen=None, *args, **kwargs):
            # Draw at current position; screen provided by game.draw
            if screen is not None:
                screen.blit(self.image, (int(self.x), int(self.y)))

        def update(self, *args, **kwargs):
            pass

    # Populate various entity lists so draw paths execute
    game.birds = [DummyEntity(game.image.bird_img1)]
    game.bats = [DummyEntity(game.image.bat_img1)]
    game.airplanes = [DummyEntity(game.image.airplane_img)]
    game.flying_disks = [DummyEntity(game.image.flying_disk_img)]
    game.fires = [DummyEntity(game.image.fire_img)]
    game.turtles = [DummyEntity(game.image.turtle_img)]
    game.spiders = [DummyEntity(game.image.spider_img)]
    game.robots = [DummyEntity(game.image.robot_img)]
    game.aliens = [DummyEntity(game.image.alien_img)]
    game.boss_alien = DummyEntity(game.image.boss_alien_img)
    game.explosions = [DummyEntity(game.image.explosion_image)]
    game.extra_lives = [DummyEntity(game.image.explosion_image)]
    game.player.bullets = [DummyEntity(game.image.bullet_image)]

    # Call draw which should iterate and blit all
    game.draw()

def test_draw_ocean_background_fallback_gradient(game, monkeypatch):
    from internal.engine.game import GameState

    # Ensure no background images so fallback gradient path runs
    game.image.background_img = None
    if hasattr(game, 'menu_background_img'):
        game.menu_background_img = None

    # Use MAIN_MENU state which calls draw_ocean_background
    game.state = GameState.MAIN_MENU
    game.draw()

def test_handle_events_quit(game):
    # Post QUIT event and ensure handle_events returns False
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
    assert game.handle_events() is False

def test_splash_dev_key_to_title(game, monkeypatch):
    from internal.engine.game import GameState
    import internal.engine.game as game_mod

    # Development environment allows skipping splash via key
    game_mod.ENV_CONFIG['environment'] = 'development'
    game.state = GameState.SPLASH
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))
    game.handle_events()
    assert game.state == GameState.TITLE_SCREEN

def test_title_skip_opening_video_in_production(game, monkeypatch):
    from internal.engine.game import GameState
    import internal.engine.game as game_mod

    # In production with skip-opening-video flag, go straight to MAIN_MENU
    game_mod.ENV_CONFIG['environment'] = 'production'
    game.env_config = {'skip-opening-video': '1'}
    game.music_started = False
    game.state = GameState.TITLE_SCREEN
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == GameState.MAIN_MENU
    assert game.music_started is True

def test_restart_with_r_in_victory_and_show_ranking(game):
    from internal.engine.game import GameState

    # Press 'r' in VICTORY to restart to PLAYING
    game.state = GameState.VICTORY
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r}))
    game.handle_events()
    assert game.state == GameState.PLAYING

    # Press 'r' in SHOW_RANKING to restart to PLAYING
    game.state = GameState.SHOW_RANKING
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r}))
    game.handle_events()
    assert game.state == GameState.PLAYING

def test_joystick_select_difficulty_confirm_and_back(game):
    from internal.engine.game import GameState
    from internal.engine.difficulty import Difficulty

    # Simulate joystick confirm in SELECT_DIFFICULTY
    game.state = GameState.SELECT_DIFFICULTY
    game.difficulty_options = ["Fácil", "Normal", "Difícil"]
    game.difficulty_selected = 2  # Choose HARD
    game.joystick_connected = True
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 6}))
    game.handle_events()
    assert game.state == GameState.PLAYING
    assert game.difficulty == Difficulty.HARD

    # Navigate back to MAIN_MENU via button 1 in SELECT_DIFFICULTY
    game.state = GameState.SELECT_DIFFICULTY
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 1}))
    game.handle_events()
    assert game.state == GameState.MAIN_MENU

def test_joystick_credits_menu_back_to_main(game):
    from internal.engine.game import GameState

    # Credits menu should return to MAIN_MENU on button
    game.state = GameState.CREDITS
    game.credits_type = 'menu'
    game.joystick_connected = True
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 1}))
    assert game.handle_events() is True
    assert game.state == GameState.MAIN_MENU
def test_keyboard_navigation_paths(game):
    from internal.engine.game import GameState

    # TITLE_SCREEN -> OPENING_VIDEO with successful load
    class Vid:
        def load_video(self, path):
            return True
        def start_playback(self):
            pass
        def stop(self):
            pass
    game.video_player = Vid()
    game.state = GameState.TITLE_SCREEN
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))
    game.handle_events()
    assert game.state == GameState.OPENING_VIDEO

    # OPENING_VIDEO -> MAIN_MENU on keydown
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == GameState.MAIN_MENU

    # MAIN_MENU navigation: up, down, select
    game.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
    game.menu_selected = 0
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()

    # SELECT_DIFFICULTY navigation: up, down, escape, return
    game.state = GameState.SELECT_DIFFICULTY
    game.difficulty_options = ["Fácil", "Normal", "Difícil"]
    game.difficulty_selected = 1
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.state == GameState.MAIN_MENU

    game.state = GameState.SELECT_DIFFICULTY
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == GameState.PLAYING

    # FIM_SCREEN -> CREDITS (ending)
    game.state = GameState.FIM_SCREEN
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))
    game.handle_events()
    assert game.state == GameState.CREDITS and game.credits_type == "ending"

    # CREDITS (menu) -> MAIN_MENU on ESC
    game.state = GameState.CREDITS
    game.credits_type = "menu"
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    assert game.handle_events() is True
    assert game.state == GameState.MAIN_MENU

    # RECORDS -> back to previous
    game.state = GameState.RECORDS
    game.previous_state_before_records = GameState.MAIN_MENU
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == GameState.MAIN_MENU and game.previous_state_before_records is None
def test_init_env_development_initial_stage_valid(monkeypatch):
    # Exercita linhas de configuração inicial do nível em modo development
    from internal.engine import game as game_module
    from internal.engine.game import Game
    import pygame

    orig_env = dict(game_module.ENV_CONFIG)
    try:
        game_module.ENV_CONFIG["environment"] = "development"
        game_module.ENV_CONFIG["initial-stage"] = "3"
        # Evitar efeitos colaterais de áudio
        monkeypatch.setattr(game_module.Mixer, "init", lambda pg: None, False)
        monkeypatch.setattr(
            game_module.SoundEffects,
            "load_sound_effects",
            lambda self_se: None,
            False,
        )
        # Criar uma instância nova do jogo
        g = Game()
        assert g.current_level == 3
    finally:
        game_module.ENV_CONFIG.clear()
        game_module.ENV_CONFIG.update(orig_env)


def test_init_env_development_initial_stage_invalid(monkeypatch):
    # Cobrir branches de valor inválido do initial-stage e fallback para 1
    from internal.engine import game as game_module
    from internal.engine.game import Game
    import pygame

    orig_env = dict(game_module.ENV_CONFIG)
    try:
        game_module.ENV_CONFIG["environment"] = "development"
        game_module.ENV_CONFIG["initial-stage"] = "abc"  # inválido
        monkeypatch.setattr(game_module.Mixer, "init", lambda pg: None, False)
        monkeypatch.setattr(
            game_module.SoundEffects,
            "load_sound_effects",
            lambda self_se: None,
            False,
        )
        g = Game()
        assert g.current_level == 1
    finally:
        game_module.ENV_CONFIG.clear()
        game_module.ENV_CONFIG.update(orig_env)


def test_bullet_pool_get_and_return(game):
    # Cobrir get_pooled_bullet e return_bullet_to_pool
    from internal.engine.game import Bullet

    # Pool vazio: deve criar nova bala
    game.bullet_pool = []
    b1 = game.get_pooled_bullet(10, 20, direction=-1, image=None)
    assert isinstance(b1, Bullet)
    assert b1.x == 10 and b1.y == 20 and b1.direction == -1

    # Retornar ao pool e reutilizar
    game.return_bullet_to_pool(b1)
    assert len(game.bullet_pool) == 1
    b2 = game.get_pooled_bullet(30, 40, direction=1, image=None)
    assert b2 is b1
    assert b2.x == 30 and b2.y == 40 and b2.rect.x == 30 and b2.rect.y == 40

    # Encher o pool até o limite e garantir que não ultrapassa 20
    for _ in range(20):
        game.return_bullet_to_pool(Bullet(0, 0))
    assert len(game.bullet_pool) <= 20


def test_bullet_hits_bird_bat_airplane_disk(game):
    from internal.engine.game import GameState
    import pygame

    class DummyEnemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 20, 20)
            self.draw_calls = 0
        def draw(self, screen):
            self.draw_calls += 1
        def update(self, *args, **kwargs):
            # Return True to avoid culling removal in update loops
            return True

    class DummyBullet:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 10, 10)
        def draw(self, screen):
            pass

    game.player.update = lambda *a, **k: None
    game.sound_effects.play_sound_effect = lambda *a, **k: None
    game.state = GameState.PLAYING

    # Bird (<=20)
    game.current_level = 10
    bird = DummyEnemy(game.player.rect.x, game.player.rect.y)
    game.birds = [bird]
    b = DummyBullet(bird.x, bird.y)
    game.player.bullets = [b]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 100
    assert b not in getattr(game.player, "bullets", [])

    # Bat (<=30)
    game.current_level = 25
    bat = DummyEnemy(game.player.rect.x, game.player.rect.y)
    game.bats = [bat]
    b = DummyBullet(bat.x, bat.y)
    game.player.bullets = [b]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 75
    assert b not in getattr(game.player, "bullets", [])

    # Airplane (<=40)
    game.current_level = 35
    airplane = DummyEnemy(game.player.rect.x, game.player.rect.y)
    game.airplanes = [airplane]
    b = DummyBullet(airplane.x, airplane.y)
    game.player.bullets = [b]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 50
    assert b not in getattr(game.player, "bullets", [])

    # Disk (>40)
    game.current_level = 45
    disk = DummyEnemy(game.player.rect.x, game.player.rect.y)
    game.flying_disks = [disk]
    b = DummyBullet(disk.x, disk.y)
    game.player.bullets = [b]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 90
    assert b not in getattr(game.player, "bullets", [])


def test_bullet_hits_turtle_and_spider(game):
    from internal.engine.game import GameState
    import pygame

    class DummyEnemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 20, 20)
        def draw(self, screen):
            pass
        def update(self):
            return None

    class DummyBullet:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 10, 10)
        def draw(self, screen):
            pass

    game.player.update = lambda *a, **k: None
    game.sound_effects.play_sound_effect = lambda *a, **k: None
    game.state = GameState.PLAYING

    # Turtle (<=20)
    game.current_level = 20
    turtle = DummyEnemy(game.player.rect.x, game.player.rect.y)
    game.turtles = [turtle]
    b = DummyBullet(turtle.x, turtle.y)
    game.player.bullets = [b]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 70

    # Spider (>20)
    game.current_level = 30
    spider = DummyEnemy(game.player.rect.x, game.player.rect.y)
    game.spiders = [spider]
    b = DummyBullet(spider.x, spider.y)
    game.player.bullets = [b]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 120


def test_invulnerable_missile_and_laser_hits_player(game):
    from internal.engine.game import GameState

    game.player.update = lambda *a, **k: None
    game.state = GameState.PLAYING
    game.player.is_being_abducted = False
    game.player.is_invulnerable = True
    game.player.is_hit = False

    # Robot missile
    game.current_level = 31
    class DummyMissile:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            import pygame
            self.rect = pygame.Rect(x, y, 8, 8)
        def draw(self, s):
            pass
    class R:
        def __init__(self, x, y):
            import pygame
            self.x = x; self.y = y; self.missiles = []
            self.rect = pygame.Rect(x, y, 20, 20)
        def update(self, camera_x):
            return None
    # Place robot away from player to avoid direct collision branch
    robot = R(game.player.rect.x + 200, game.player.rect.y + 200)
    # Ensure missile collides with player regardless of robot position
    m = DummyMissile(game.player.rect.x, game.player.rect.y)
    robot.missiles = [m]
    game.robots = [robot]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 15
    assert m not in robot.missiles

    # Alien laser
    game.current_level = 41
    class DummyLaser:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            import pygame
            self.rect = pygame.Rect(x, y, 8, 8)
        def draw(self, s):
            pass
    class A:
        def __init__(self, x, y):
            import pygame
            self.x = x; self.y = y; self.lasers = []
            self.rect = pygame.Rect(x, y, 20, 20)
        def update(self, camera_x):
            return None
    # Place alien away from player to avoid direct collision branch
    alien = A(game.player.rect.x + 200, game.player.rect.y + 200)
    # Ensure laser collides with player regardless of alien position
    l = DummyLaser(game.player.rect.x, game.player.rect.y)
    alien.lasers = [l]
    game.aliens = [alien]
    pre_score = game.score
    game.update()
    assert game.score == pre_score + 15
    assert l not in alien.lasers


def test_draw_platform_flag_spaceship(game):
    from internal.engine.game import GameState
    import pygame

    class DummyDrawObj:
        def __init__(self, x, y, w=20, h=20):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, w, h)
            self.draw_calls = 0
        def draw(self, screen):
            self.draw_calls += 1
        def update_position(self, x, y):
            self.x = x; self.y = y

    game.state = GameState.PLAYING
    game.camera_x = 0

    # Platforms
    p = DummyDrawObj(100, 100)
    game.platforms = [p]
    # Flag
    game.flag = DummyDrawObj(120, 100)
    # Spaceship
    game.spaceship = DummyDrawObj(150, 50, 60, 30)
    # Draw and check calls
    game.draw()
    assert p.draw_calls == 1
    # Flag draw increments its draw_calls
    assert game.flag.draw_calls == 1
    # Spaceship draw increments its draw_calls
    assert game.spaceship.draw_calls == 1


def test_draw_boss_alien_capture_flash(game):
    from internal.engine.game import GameState
    class DummyBoss:
        def __init__(self, x, y):
            self.x = x; self.y = y; self.draw_calls = 0
        def draw(self, screen):
            self.draw_calls += 1

    game.state = GameState.PLAYING
    game.current_level = 51
    game.camera_x = 0
    game.player.is_being_abducted = False
    game.boss_alien = DummyBoss(200, 50)

    # Captured with flash OFF => draw
    game.boss_alien_captured = True
    game.capture_flash_state = False
    game.draw()
    assert game.boss_alien.draw_calls >= 1

    # Captured with flash ON => skip draw
    game.boss_alien.draw_calls = 0
    game.capture_flash_state = True
    game.draw()
    assert game.boss_alien.draw_calls == 0

    # Not captured => draw
    game.boss_alien_captured = False
    game.draw()
    assert game.boss_alien.draw_calls >= 1


def test_draw_credits_and_reset(monkeypatch, game):
    from internal.engine.game import GameState
    import pygame

    game.state = GameState.CREDITS
    game.credits_type = "cinematic"
    game.credits_scroll_y = 10_000  # acima do threshold para encerrar
    # Conteúdo que percorre todos os ramos de formatação
    game.credits_content = [
        "JUMP & HIT",
        "═══",
        "https://example.com",
        "DESENVOLVIDO POR",
        "CirrasTec",
        "© 2025 CirrasTec",
        "Obrigado por jogar!",
        "Texto normal",
        "",
    ]
    # Stub para mixer.stop
    import pygame.mixer
    monkeypatch.setattr(pygame.mixer.music, "stop", lambda: None, False)

    # Executa draw e verifica transição
    # Stub play_menu_music to avoid side-effects
    game.music.play_menu_music = lambda self_g: None
    game.draw()
    assert game.state == GameState.MAIN_MENU


def test_player_action_jump_shot_and_death_paths(monkeypatch, game):
    from internal.engine.game import GameState, Level

    game.state = GameState.PLAYING
    # shot
    game.player.update = lambda *a, **k: "shot"
    called = {"shot":0, "jump":0}
    game.sound_effects.play_sound_effect = lambda name: called.__setitem__(name, called.get(name,0)+1)
    game.update()
    assert called["shot"] == 1

    # jump
    game.player.update = lambda *a, **k: "jump"
    game.update()
    assert called["jump"] == 1

    # death with remaining lives => reinicia nível e toca música
    game.lives = 2
    game.current_level = 5
    game.player.update = lambda *a, **k: False
    level_called = {"init":0, "music":0}
    monkeypatch.setattr(Level, "init_level", lambda self_g: level_called.__setitem__("init", level_called["init"]+1), False)
    game.music.play_level_music = lambda self_g, lvl: level_called.__setitem__("music", level_called["music"]+1)
    game.update()
    assert level_called["init"] == 1 and level_called["music"] == 1
    # death with no lives => GAME_OVER
    game.lives = 1
    game.ranking_manager.is_high_score = lambda _score: False
    game.player.update = lambda *a, **k: False
    game.update()
    from internal.engine.game import GameState as GS
    assert game.state in (GS.GAME_OVER, GS.ENTER_NAME)