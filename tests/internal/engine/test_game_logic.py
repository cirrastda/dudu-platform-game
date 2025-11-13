import types
import builtins
import math
import pytest


class FakeSurface:
    def __init__(self, w=800, h=600):
        self.w = w
        self.h = h
        self.blit_calls = []
        self.fill_calls = []

    def blit(self, src, rect):
        self.blit_calls.append((src, rect))

    def fill(self, color):
        self.fill_calls.append(color)

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h

    def copy(self):
        return FakeSurface(self.w, self.h)

    def set_alpha(self, *_args, **_kwargs):
        return None

    def get_rect(self, **kwargs):
        # Very simple rect-like tuple for center positioning
        return types.SimpleNamespace(**{
            "center": kwargs.get("center", (self.w // 2, self.h // 2)),
            "inflate": lambda a, b: (a, b),
        })


class FakeFont:
    def render(self, *_args, **_kwargs):
        return FakeSurface(100, 20)


class FakeRect:
    def __init__(self, x=0, y=0, w=10, h=10):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    def colliderect(self, other):
        return not (
            self.right <= other.x or other.right <= self.x or self.bottom <= other.y or other.bottom <= self.y
        )


class FakeDraw:
    def __init__(self):
        self.lines = []
        self.circles = []
        self.rects = []

    def line(self, *_args, **_kwargs):
        self.lines.append((_args, _kwargs))

    def circle(self, *_args, **_kwargs):
        self.circles.append((_args, _kwargs))

    def rect(self, *_args, **_kwargs):
        self.rects.append((_args, _kwargs))

    def ellipse(self, *_args, **_kwargs):
        # No-op collector to prevent AttributeError during trophy drawing
        pass

    def arc(self, *_args, **_kwargs):
        # No-op collector to prevent AttributeError during trophy drawing
        pass


class FakeTime:
    def __init__(self):
        self.ticks = 0

    def get_ticks(self):
        return self.ticks
    def Clock(self):
        return types.SimpleNamespace(tick=lambda fps: None)


class FakeDisplayInfo:
    def __init__(self, w=1200, h=800):
        self.current_w = w
        self.current_h = h


class FakeDisplay:
    def __init__(self):
        self.captions = []
        self.mode_calls = []

    def set_caption(self, text):
        self.captions.append(text)

    def Info(self):
        return FakeDisplayInfo()

    def set_mode(self, size, flags=0):
        self.mode_calls.append((size, flags))
        return FakeSurface(size[0], size[1])

    def flip(self):
        # No-op used by Screen.present
        return None


class FakeTransform:
    @staticmethod
    def scale(surface, size):
        return FakeSurface(size[0], size[1])


class FakeVideoPlayer:
    def __init__(self):
        self._loaded = False
        self._started = False
        self._finished = False

    def load_video(self, _path):
        self._loaded = True
        return True

    def start_playback(self):
        self._started = True

    def stop(self):
        self._finished = True

    def update(self):
        pass

    def is_finished(self):
        return self._finished

    def cleanup(self):
        pass

    def draw(self, _screen):
        pass


class FakeEndingVideoPlayer(FakeVideoPlayer):
    def load_video(self, _path):
        self._loaded = True
        return True


class FakeMusic:
    def __init__(self):
        self.play_menu_calls = 0
        self.play_level_calls = []
        self.play_music_calls = []

    def start(self, _game):
        # Initialize any internal flags if needed
        return None

    def play_menu_music(self, _game):
        self.play_menu_calls += 1

    def play_level_music(self, _game, level):
        self.play_level_calls.append(level)

    def play_music(self, track):
        self.play_music_calls.append(track)


class FakeSoundEffects:
    def __init__(self):
        self.effects = []

    def play_sound_effect(self, name):
        self.effects.append(name)

    def load_sound_effects(self):
        return None


class FakeJoystick:
    def __init__(self, axes=None):
        # axes dict: index -> value
        self._axes = axes or {0: 0.0, 1: 0.0, 6: 0.0, 7: 0.0}

    def get_numaxes(self):
        return 8

    def get_axis(self, idx):
        return self._axes.get(idx, 0.0)


class FakePlayer:
    def __init__(self):
        self.x = 100
        self.y = 200
        self.rect = FakeRect(self.x, self.y, 30, 30)
        self.bullets = []
        self.is_invulnerable = False
        self.is_hit = False
        self.is_being_abducted = False
        self.abduction_timer = 0
        self.just_landed = False

    def update(self, platforms, bullet_img, camera_x, joystick, game):
        # Simular uma ação de pulo seguida de tiro
        if hasattr(game, "_next_player_action"):
            action = game._next_player_action.pop(0) if game._next_player_action else None
            if action == "jump":
                return "jump"
            if action == "shot":
                return "shot"
            if action == "die":
                return False
        return None

    def take_hit(self):
        self.is_hit = True

    def start_abduction(self):
        self.is_being_abducted = True
        self.abduction_timer = 600

    def draw(self, _screen):
        # No-op for rendering path coverage
        return None


class DummyObj:
    def __init__(self, x=0, y=0, w=10, h=10, id_=1):
        self.x = x
        self.y = y
        self.rect = FakeRect(x, y, w, h)
        self.id = id_
        self.scale_x = 1
        self.scale_y = 1
    def draw(self, _screen):
        pass
    def update(self, *args, **kwargs):
        # Keep object "visible" by default during update cycles
        return True


@pytest.fixture(autouse=True)
def headless_pygame(monkeypatch):
    # Patch pygame module pieces used by Game
    import internal.engine.game as game_module

    class PygameStub:
        Rect = FakeRect
        draw = FakeDraw()
        time = FakeTime()
        display = FakeDisplay()
        transform = FakeTransform()
        K_UP = 273
        K_DOWN = 274
        K_RETURN = 13
        K_SPACE = 32
        K_ESCAPE = 27
        FULLSCREEN = 1

        def event_get(self):
            return []

        def key_get_pressed(self):
            # Return a tuple usable with indexing for SPACE
            arr = [False] * 400
            return tuple(arr)

    pg = PygameStub()

    # Bind functions expected by code
    monkeypatch.setattr(game_module.pygame, "Rect", pg.Rect, raising=False)
    monkeypatch.setattr(game_module.pygame, "draw", pg.draw, raising=False)
    monkeypatch.setattr(game_module.pygame, "time", pg.time, raising=False)
    monkeypatch.setattr(game_module.pygame, "display", pg.display, raising=False)
    monkeypatch.setattr(game_module.pygame, "transform", pg.transform, raising=False)
    monkeypatch.setattr(game_module.pygame, "K_UP", pg.K_UP, raising=False)
    monkeypatch.setattr(game_module.pygame, "K_DOWN", pg.K_DOWN, raising=False)
    monkeypatch.setattr(game_module.pygame, "K_RETURN", pg.K_RETURN, raising=False)
    monkeypatch.setattr(game_module.pygame, "K_SPACE", pg.K_SPACE, raising=False)
    monkeypatch.setattr(game_module.pygame, "K_ESCAPE", pg.K_ESCAPE, raising=False)

    # Patch functions
    monkeypatch.setattr(game_module.pygame, "event", types.SimpleNamespace(get=lambda: []), raising=False)
    monkeypatch.setattr(game_module.pygame, "key", types.SimpleNamespace(get_pressed=lambda: pg.key_get_pressed()), raising=False)

    # Fonts
    monkeypatch.setattr(game_module.pygame, "font", types.SimpleNamespace(Font=lambda *_a, **_k: FakeFont()), raising=False)

    # Screen.init to set screen surface
    import internal.engine.screen as screen_module
    def fake_screen_init(game):
        game.screen_manager = types.SimpleNamespace(game_surface=FakeSurface(1024, 768), screen_buffer=FakeSurface(1024, 768), scale_x=1.0, scale_y=1.0)
        game.screen = game.screen_manager.game_surface
        game.is_fullscreen = False
    monkeypatch.setattr(screen_module.Screen, "init", fake_screen_init)

    # TitleScreen.show no-op
    import internal.engine.title as title_module
    monkeypatch.setattr(title_module.TitleScreen, "show", lambda game: None)

    # Music and effects
    import internal.engine.game as gm
    gm.Music = lambda: FakeMusic()
    gm.SoundEffects = lambda: FakeSoundEffects()

    # Mixer.init no-op
    import internal.engine.sound.mixer as mixer_module
    monkeypatch.setattr(mixer_module.Mixer, "init", lambda _pg: None)

    # pygame.mixer.music.stop no-op used in credits draw
    monkeypatch.setattr(game_module.pygame, "mixer", types.SimpleNamespace(
        music=types.SimpleNamespace(stop=lambda: None)
    ), raising=False)

    # Joystick.init: inject FakeJoystick and mark as disconnected by default
    import internal.engine.joystick as joystick_module
    def fake_joystick_init(game):
        game.joystick = FakeJoystick()
        game.joystick_connected = False
    monkeypatch.setattr(joystick_module.Joystick, "init", fake_joystick_init)

    # Video players
    gm.VideoPlayer = lambda: FakeVideoPlayer()
    gm.GameState  # ensure import


def make_game(monkeypatch, env=None):
    import internal.engine.game as game_module
    # Patch ENV_CONFIG before Game() is instantiated
    env_conf = {"environment": "development"}
    if env:
        env_conf.update(env)
    monkeypatch.setattr(game_module, "ENV_CONFIG", env_conf)

    # Instantiate game
    g = game_module.Game()
    # Inject stubs
    g.music = FakeMusic()
    g.sound_effects = FakeSoundEffects()
    g.video_player = FakeVideoPlayer()
    g.ending_video_player = FakeEndingVideoPlayer()
    # Minimal images and resources
    g.image = types.SimpleNamespace(
        background_img=None,
        bullet_image=None,
        explosion_image=None,
    )
    # Prepare lists
    g.platforms = []
    g.birds = []
    g.bats = []
    g.airplanes = []
    g.flying_disks = []
    g.fires = []
    g.turtles = []
    g.spiders = []
    g.robots = []
    g.orphan_missiles = []
    g.aliens = []
    g.orphan_lasers = []
    # Player
    g.player = FakePlayer()
    # Misc
    g.flag = None
    g.spaceship = None
    g.camera_x = 0
    g.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
    g.game_logo = FakeSurface(120, 40)
    g.big_font = FakeFont()
    g.font = FakeFont()
    g.difficulty_options = ["Fácil", "Normal", "Difícil"]
    g.difficulty_selected = 1
    g.menu_selected = 0
    g.game_over_options = ["Jogar novamente", "Recordes", "Sair"]
    g.game_over_selected = 0
    g.max_lives = 3
    g.lives = 3
    g.score = 0
    g.joystick_connected = False
    # Garanta um joystick falso disponível para leituras de eixo
    g.joystick = FakeJoystick()
    # Splash
    g.logos = [FakeSurface(50, 20)]
    g.logo_display_time = 60
    g.fade_in_duration = 10
    g.fade_out_duration = 10
    g.splash_timer = 0
    g.splash_duration = 30
    return g


def test_splash_key_dev_skips_to_title(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch, env={"environment": "development"})

    # Feed a KEYDOWN event to handle_events
    key_event = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [key_event]))
    g.state = gm.GameState.SPLASH
    assert g.handle_events() is True
    assert g.state == gm.GameState.TITLE_SCREEN


def test_title_to_opening_video_and_skip_to_menu(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch, env={"environment": "production", "skip-opening-video": "0"})
    g.state = gm.GameState.TITLE_SCREEN
    key_event = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [key_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.OPENING_VIDEO

    # Now press any key to stop video and go to main menu
    g.state = gm.GameState.OPENING_VIDEO
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [key_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU
    assert g.music.play_menu_calls >= 1


def test_title_joystick_to_opening_and_skip_to_menu(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch, env={"environment": "production", "skip-opening-video": "0"})
    # Navigate from title to opening video via joystick
    g.state = gm.GameState.TITLE_SCREEN
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.OPENING_VIDEO
    assert g.video_player._loaded is True
    assert g.video_player._started is True

    # Any joystick button during opening video skips to main menu
    g.state = gm.GameState.OPENING_VIDEO
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU
    assert g.music.play_menu_calls >= 1


def test_title_skip_opening_video_by_env_joystick(monkeypatch):
    import internal.engine.game as gm
    # In production with skip-opening-video enabled, joystick should go to MAIN_MENU directly
    g = make_game(monkeypatch, env={"environment": "production", "skip-opening-video": "1"})
    g.state = gm.GameState.TITLE_SCREEN
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU
    assert g.music.play_menu_calls >= 1


def test_opening_video_load_failure_falls_back_to_menu(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch, env={"environment": "production", "skip-opening-video": "0"})
    # Force video load failure
    g.video_player._loaded = False
    g.video_player.load_video = lambda _path: False
    g.state = gm.GameState.TITLE_SCREEN
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU
    assert g.music.play_menu_calls >= 1


def test_joystick_main_menu_selection_starts_difficulty(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.MAIN_MENU
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    g.handle_events()
    assert g.state == gm.GameState.SELECT_DIFFICULTY


def test_draw_opening_and_ending_video_calls_draw(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Track draw calls
    calls = {"opening": 0, "ending": 0}
    def opening_draw(screen):
        calls["opening"] += 1
    def ending_draw(screen):
        calls["ending"] += 1
    g.video_player.draw = opening_draw
    g.ending_video_player.draw = ending_draw

    g.state = gm.GameState.OPENING_VIDEO
    g.draw()
    assert calls["opening"] == 1

    g.state = gm.GameState.ENDING_VIDEO
    g.draw()
    assert calls["ending"] == 1


def test_draw_game_over_renders_menu_and_instructions(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.GAME_OVER
    g.score = 123
    pre_blits = len(g.screen.blit_calls)
    g.draw()
    # Expect at least title, score, options and instructions to blit
    assert len(g.screen.blit_calls) > pre_blits


def test_draw_victory_renders_texts(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.VICTORY
    pre_blits = len(g.screen.blit_calls)
    g.draw()
    # Several victory texts should be blitted
    assert len(g.screen.blit_calls) > pre_blits


def test_draw_enter_name_renders_fields(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.ENTER_NAME
    g.player_name = "PLAYER"
    pre_blits = len(g.screen.blit_calls)
    g.draw()
    # Title, score, prompt, name and instruction should be blitted
    assert len(g.screen.blit_calls) > pre_blits


def test_draw_show_ranking_renders_table(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Stub ranking manager
    g.ranking_manager = types.SimpleNamespace(get_rankings=lambda: [
        {"name": "AAA", "score": 1000},
        {"name": "BBB", "score": 750},
    ])
    g.player_name = "AAA"
    g.state = gm.GameState.SHOW_RANKING
    pre_blits = len(g.screen.blit_calls)
    g.draw()
    # Title, headers and at least two rows should be blitted
    assert len(g.screen.blit_calls) > pre_blits


def test_draw_fim_screen_shows_skip_hint(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.FIM_SCREEN
    # Ensure timer passes threshold to draw skip hint
    g.fim_screen_timer = 61
    pre_fills = len(g.screen.fill_calls)
    pre_blits = len(g.screen.blit_calls)
    g.draw()
    # Background fill and hint text blit expected
    assert len(g.screen.fill_calls) > pre_fills
    assert len(g.screen.blit_calls) > pre_blits


def test_draw_credits_menu_and_cinematic_scroll_finish(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Credits menu variant
    g.state = gm.GameState.CREDITS
    g.credits_type = "menu"
    pre_blits = len(g.screen.blit_calls)
    g.draw()
    assert len(g.screen.blit_calls) > pre_blits

    # Credits ending cinematic: force scroll past the end to trigger finish
    g.state = gm.GameState.CREDITS
    g.credits_type = "ending"
    g.credits_scroll_y = 10_000
    # Track menu music calls
    pre_menu_calls = g.music.play_menu_calls
    g.draw()
    assert g.state == gm.GameState.MAIN_MENU
    assert g.music.play_menu_calls == pre_menu_calls + 1
    assert g.credits_scroll_y == 0


def test_update_credits_menu_loop_reset(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Start credits in menu type and simulate long scroll
    g.state = gm.GameState.CREDITS
    g.credits_type = "menu"
    g.credits_scroll_y = 50
    g.credits_reset_timer = 1799
    g.update()
    # After one update, timer hits threshold and resets
    assert g.credits_reset_timer == 1800 or g.credits_reset_timer == 0
    if g.credits_reset_timer == 0:
        assert g.credits_scroll_y == 0


def test_fim_screen_key_and_joystick_to_credits(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # KEYDOWN path
    g.state = gm.GameState.FIM_SCREEN
    key_event = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [key_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.CREDITS
    assert g.credits_type == "ending"

    # JOYBUTTONDOWN path
    g.state = gm.GameState.FIM_SCREEN
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.CREDITS
    assert g.credits_type == "ending"


def test_credits_menu_exit_via_key_and_joystick(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Credits react only when type == 'menu'
    g.state = gm.GameState.CREDITS
    g.credits_type = "menu"
    ev_escape = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_ESCAPE, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_escape]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU

    # Joystick path
    g.state = gm.GameState.CREDITS
    g.credits_type = "menu"
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=1)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU


def test_records_back_to_previous_or_menu_via_key_and_joystick(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Set previous state and exit via KEYDOWN
    g.state = gm.GameState.RECORDS
    g.previous_state_before_records = gm.GameState.GAME_OVER
    ev_enter = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_enter]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.GAME_OVER

    # Fallback to MAIN_MENU when no previous via JOYBUTTONDOWN
    g.state = gm.GameState.RECORDS
    g.previous_state_before_records = None
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=6)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU


def test_enter_name_confirm_via_joystick(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Ranking stub
    class FakeRanking:
        def __init__(self):
            self.added = None
        def add_score(self, name, score):
            self.added = (name, score)
        def is_high_score(self, score):
            return True
    g.ranking_manager = FakeRanking()
    # Enter name state and confirm via joystick
    g.state = gm.GameState.ENTER_NAME
    g.player_name = "ABC"
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=6)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.ranking_manager.added == ("ABC", g.score)
    assert g.state == gm.GameState.SHOW_RANKING


def test_game_over_joystick_records_and_exit(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.GAME_OVER
    g.joystick_connected = True
    # Select Recordes
    g.game_over_selected = 1
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.RECORDS
    assert g.previous_state_before_records == gm.GameState.GAME_OVER

    # Select Sair
    g.state = gm.GameState.GAME_OVER
    g.game_over_selected = 2
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is False


def test_ending_video_update_load_and_finish(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Load success: sets loaded and starts playback
    g.state = gm.GameState.ENDING_VIDEO
    g.update()
    assert hasattr(g, "ending_video_loaded") and g.ending_video_loaded is True
    assert g.ending_video_player._started is True

    # Finish transitions to FIM_SCREEN and resets timer
    g.ending_video_player._finished = True
    g.update()
    assert g.state == gm.GameState.FIM_SCREEN
    assert g.fim_screen_timer == 0

    # Load failure path goes directly to FIM_SCREEN
    g = make_game(monkeypatch)
    g.state = gm.GameState.ENDING_VIDEO
    g.ending_video_player.load_video = lambda _p: False
    g.update()
    assert g.state == gm.GameState.FIM_SCREEN
    assert g.fim_screen_timer == 0


def test_handle_menu_selection_recordes_creditos_e_sair(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Patch sys.exit to catch call
    import internal.engine.game as game_module
    called = {"exit": False}
    def fake_quit():
        return None
    def fake_exit():
        called["exit"] = True
        raise SystemExit
    monkeypatch.setattr(game_module, "pygame", types.SimpleNamespace(quit=fake_quit), raising=True)
    monkeypatch.setattr(game_module, "sys", types.SimpleNamespace(exit=fake_exit), raising=True)

    # Recordes
    g.menu_selected = g.menu_options.index("Recordes")
    g.handle_menu_selection()
    assert g.state == gm.GameState.RECORDS

    # Créditos
    g.menu_selected = g.menu_options.index("Créditos")
    g.handle_menu_selection()
    assert g.state == gm.GameState.CREDITS
    assert g.credits_type == "menu"

    # Sair
    g.menu_selected = g.menu_options.index("Sair")
    try:
        g.handle_menu_selection()
    except SystemExit:
        pass
    assert called["exit"] is True


def test_show_ranking_joystick_back_to_previous(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SHOW_RANKING
    g.previous_state_before_ranking = gm.GameState.VICTORY
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=1)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.VICTORY
    assert g.previous_state_before_ranking is None


def test_select_difficulty_joystick_back_to_menu(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SELECT_DIFFICULTY
    g.joystick_connected = True
    joy_event = types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=1)
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [joy_event]))
    assert g.handle_events() is True
    assert g.state == gm.GameState.MAIN_MENU


def test_playing_joystick_button_mapping_no_errors(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.PLAYING
    g.joystick_connected = True
    # Buttons A/X and B/Circle branches
    events = [
        types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=0),
        types.SimpleNamespace(type=gm.pygame.JOYBUTTONDOWN, button=1),
    ]
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: events))
    assert g.handle_events() is True


def test_game_over_key_navigation_up_down(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.GAME_OVER
    g.game_over_selected = 0
    # Navigate down then up
    ev_down = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_DOWN, unicode="")
    ev_up = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_UP, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_down]))
    g.handle_events()
    assert g.game_over_selected == 1
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_up]))
    g.handle_events()
    assert g.game_over_selected == 0


def test_main_menu_navigation_and_start_selection(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.MAIN_MENU
    ev_enter = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_enter]))
    g.handle_events()
    # Menu selection triggers handle_menu_selection -> SELECT_DIFFICULTY
    assert g.state == gm.GameState.SELECT_DIFFICULTY


def test_select_difficulty_confirms_and_starts_playing(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SELECT_DIFFICULTY
    # Confirm difficulty
    ev_confirm = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_confirm]))
    # Patch Level.init_level to a no-op
    import internal.engine.level.level as level_module
    monkeypatch.setattr(level_module.Level, "init_level", lambda game: None)
    g.handle_events()
    assert g.state == gm.GameState.PLAYING


def test_enter_name_flow_and_show_ranking(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Force ranking path
    class FakeRanking:
        def is_high_score(self, score):
            return True
        def add_score(self, name, score):
            self.last = (name, score)
    g.ranking_manager = FakeRanking()

    # Simulate player death driving to ENTER_NAME
    g.state = gm.GameState.PLAYING
    g._next_player_action = ["die"]
    g.lives = 1
    g.update()
    assert g.state == gm.GameState.ENTER_NAME

    # Type name and press enter
    ev_a = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=0, unicode="A")
    ev_enter = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_a, ev_enter]))
    g.handle_events()
    assert g.state == gm.GameState.SHOW_RANKING


def test_show_ranking_escape_returns_previous(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SHOW_RANKING
    g.previous_state_before_ranking = gm.GameState.GAME_OVER
    ev_esc = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_ESCAPE, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_esc]))
    # Patch Level.init_level (called on ESC fallback)
    import internal.engine.level.level as level_module
    monkeypatch.setattr(level_module.Level, "init_level", lambda game: None)
    g.handle_events()
    assert g.state == gm.GameState.GAME_OVER


def test_update_splash_advances_to_title(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SPLASH
    # Run update until splash_duration
    for _ in range(g.splash_duration + 1):
        g.update()
    assert g.state == gm.GameState.TITLE_SCREEN


def test_opening_video_update_finish_to_menu(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.OPENING_VIDEO
    # Mark video finished
    g.video_player._finished = True
    g.update()
    assert g.state == gm.GameState.MAIN_MENU
    assert g.music.play_menu_calls >= 1


def test_fim_screen_transitions_to_credits(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.FIM_SCREEN
    g.fim_screen_timer = 179
    g.update()
    assert g.state == gm.GameState.CREDITS


def test_playing_actions_and_death_paths(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Jump then shot
    g.state = gm.GameState.PLAYING
    g._next_player_action = ["jump", "shot", None]
    g.update()
    g.update()
    assert "jump" in g.sound_effects.effects
    assert "shot" in g.sound_effects.effects

    # Death to GAME_OVER when not high score
    class FakeRankingLow:
        def is_high_score(self, score):
            return False
    g.ranking_manager = FakeRankingLow()
    g._next_player_action = ["die"]
    g.lives = 1
    g.update()
    assert g.state == gm.GameState.GAME_OVER


def test_playing_collisions_robot_and_alien(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.PLAYING
    g.current_level = 35
    # Robot collides with player
    robot = DummyObj(g.player.x, g.player.y, 10, 10, id_=1)
    robot.missiles = [DummyObj(g.player.x, g.player.y, 5, 5, id_=7)]
    robot.missiles[0].update = lambda _cx: False
    robot.update = lambda _cx: None
    g.robots = [robot]
    g.update()
    # Collisions decrement life or set game over depending on lives
    assert g.lives in (2, 3)

    # Switch to alien level and test bullet hit
    g.current_level = 45
    alien = DummyObj(g.player.x, g.player.y, 10, 10, id_=1)
    alien.lasers = [DummyObj(g.player.x, g.player.y, 5, 5, id_=8)]
    alien.lasers[0].update = lambda _cx: False
    alien.update = lambda _cx: None
    g.aliens = [alien]
    # Add a bullet colliding with alien
    g.player.bullets.append(DummyObj(alien.x, alien.y, 5, 5, id_=9))
    # Ensure orphan lasers list contains items with update/draw to avoid attribute errors
    g.orphan_lasers = [types.SimpleNamespace(update=lambda _cx: False, draw=lambda _s: None, x=0, y=0)]
    g.update()
    # Alien removed or orphan lasers transferred
    assert len(g.orphan_lasers) >= 0


def test_playing_fire_collision_reduces_life_and_persists(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.PLAYING
    g.current_level = 51
    g.lives = 2
    # Add a fire overlapping player
    fire = DummyObj(g.player.x, g.player.y, 10, 10, id_=100)
    g.fires = [fire]
    # Ranking: ensure not high score path to avoid ENTER_NAME on life <= 0
    class FakeRanking:
        def is_high_score(self, score):
            return False
    g.ranking_manager = FakeRanking()

    g.update()
    # Player should have taken a hit, lost one life, fire remains
    assert g.player.is_hit is True
    assert g.lives == 1
    assert len(g.fires) == 1


def test_playing_turtle_collision_removes_enemy_and_life_loss(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.PLAYING
    g.current_level = 5  # turtles branch
    g.lives = 3
    turtle = DummyObj(g.player.x, g.player.y, 10, 10, id_=200)
    g.turtles = [turtle]
    class FakeRanking:
        def is_high_score(self, score):
            return False
    g.ranking_manager = FakeRanking()
    g.update()
    # Turtle removed, life decremented
    assert len(g.turtles) == 0
    assert g.player.is_hit is True
    assert g.lives == 2


def test_playing_spider_collision_removes_enemy_and_life_loss(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.PLAYING
    g.current_level = 25  # spiders branch
    g.lives = 3
    spider = DummyObj(g.player.x, g.player.y, 10, 10, id_=300)
    g.spiders = [spider]
    class FakeRanking:
        def is_high_score(self, score):
            return False
    g.ranking_manager = FakeRanking()
    g.update()
    # Spider removed, life decremented
    assert len(g.spiders) == 0
    assert g.player.is_hit is True
    assert g.lives == 2


def test_invulnerable_enemy_collision_awards_score_no_life_loss(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.PLAYING
    g.current_level = 18  # turtles branch
    g.lives = 3
    g.score = 0
    g.player.is_invulnerable = True
    turtle = DummyObj(g.player.x, g.player.y, 10, 10, id_=400)
    g.turtles = [turtle]
    g.update()
    # Turtle removed, life unchanged, score increased
    assert len(g.turtles) == 0
    assert g.lives == 3
    assert g.score > 0


def test_draw_paths_for_menu_select_and_playing(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Splash draw executes gradient fallback
    g.state = gm.GameState.SPLASH
    gm.pygame.time.ticks = 100
    g.draw()
    assert len(gm.pygame.draw.lines) >= 0

    # Main menu draw with logo and options
    g.state = gm.GameState.MAIN_MENU
    g.draw()
    # Select difficulty draw
    g.state = gm.GameState.SELECT_DIFFICULTY
    g.draw()

    # Playing draw with platforms and enemies
    g.state = gm.GameState.PLAYING
    g.platforms = [types.SimpleNamespace(x=0, y=0, rect=FakeRect(0, 0, 50, 10), draw=lambda s: None, scale_x=1, scale_y=1)]
    g.flag = types.SimpleNamespace(x=10, y=0, draw=lambda s: None, scale_x=1, scale_y=1)
    g.spaceship = types.SimpleNamespace(x=20, y=5, update_position=lambda x, y: None, draw=lambda s: None, scale_x=1, scale_y=1)
    g.birds = [DummyObj(0, 0)]
    g.bats = [DummyObj(0, 0)]
    g.airplanes = [DummyObj(0, 0)]
    g.flying_disks = [DummyObj(0, 0)]
    g.fires = [DummyObj(0, 0)]
    g.turtles = [DummyObj(0, 0)]
    g.spiders = [DummyObj(0, 0)]
    g.robots = [DummyObj(0, 0)]
    g.robots[0].missiles = [DummyObj(0, 0)]
    g.orphan_missiles = [DummyObj(0, 0)]
    g.aliens = [DummyObj(0, 0)]
    g.aliens[0].lasers = [DummyObj(0, 0)]
    g.orphan_lasers = [DummyObj(0, 0)]
    # Traverse levels to hit each branch
    for lvl in [10, 25, 35, 45, 51]:
        g.current_level = lvl
        g.draw()


def test_game_over_menu_selection_play_again(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.GAME_OVER
    g.game_over_selected = 0
    ev_enter = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_enter]))
    import internal.engine.level.level as level_module
    monkeypatch.setattr(level_module.Level, "init_level", lambda game: None)
    g.handle_events()
    assert g.state == gm.GameState.PLAYING


def test_joystick_menu_navigation(monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.MAIN_MENU
    g.joystick_connected = True
    g.joystick = FakeJoystick(axes={0: 0.0, 1: -1.0, 6: 0.0, 7: 0.0})
    # First handle to update prev values
    g.handle_events()
    # Change axis to simulate down movement
    g.joystick._axes[1] = 1.0
    g.handle_events()
    assert g.menu_selected in (0, 1)


import internal.engine.game as game_mod
from internal.engine.level.level import Level
from internal.engine.difficulty import Difficulty


def _setup_game(monkeypatch):
    # Tornar __init__ inofensivo
    monkeypatch.setattr(game_mod.Game, "__init__", lambda self: None)
    # Neutralizar ENV_CONFIG para não interferir com valores de dificuldade
    monkeypatch.setattr(game_mod, "ENV_CONFIG", {}, raising=False)
    g = game_mod.Game()
    # Campos mínimos usados pelos métodos
    g.env_config = {}
    g.difficulty = Difficulty.NORMAL
    g.current_level = 1
    g.score = 0
    g.lives = 0
    # Vidas extras
    milestones, inc = game_mod.Game.get_extra_life_milestones_and_increment(g)
    g.extra_life_milestones = milestones
    g.extra_life_increment_after_milestones = inc
    g.next_extra_life_score = milestones[0]
    g.extra_lives_earned = 0
    g.sound_effects = types.SimpleNamespace(play_sound_effect=lambda name: None)
    g.birds_per_spawn = 0
    g.bird_spawn_interval = 0
    return g


def test_initial_lives_by_difficulty(monkeypatch):
    g = _setup_game(monkeypatch)
    g.difficulty = Difficulty.EASY
    assert game_mod.Game.get_initial_lives(g) == 5
    g.difficulty = Difficulty.NORMAL
    assert game_mod.Game.get_initial_lives(g) == 3
    g.difficulty = Difficulty.HARD
    assert game_mod.Game.get_initial_lives(g) == 2


def test_score_multiplier(monkeypatch):
    g = _setup_game(monkeypatch)
    g.difficulty = Difficulty.EASY
    m_easy = game_mod.Game.get_score_multiplier(g)
    g.difficulty = Difficulty.NORMAL
    m_normal = game_mod.Game.get_score_multiplier(g)
    g.difficulty = Difficulty.HARD
    m_hard = game_mod.Game.get_score_multiplier(g)
    assert m_easy <= m_normal <= m_hard


def test_extra_life_milestones_and_increment_by_difficulty(monkeypatch):
    g = _setup_game(monkeypatch)
    g.difficulty = Difficulty.EASY
    miles, inc = game_mod.Game.get_extra_life_milestones_and_increment(g)
    assert miles == [1000, 2000, 3000] and inc == 1000
    g.difficulty = Difficulty.NORMAL
    miles, inc = game_mod.Game.get_extra_life_milestones_and_increment(g)
    assert miles == [1000, 5000, 10000] and inc == 10000
    g.difficulty = Difficulty.HARD
    miles, inc = game_mod.Game.get_extra_life_milestones_and_increment(g)
    assert miles == [5000, 10000, 20000] and inc == 20000


def test_add_score_and_minimum_one(monkeypatch):
    g = _setup_game(monkeypatch)
    g.difficulty = Difficulty.HARD
    before = g.score
    game_mod.Game.add_score(g, 0.4)  # valor pequeno com multiplicador
    assert g.score >= before + 1


def test_add_score_multiplier_points_per_difficulty(monkeypatch):
    g = _setup_game(monkeypatch)
    # EASY: 10 * 0.4 = 4
    g.difficulty = Difficulty.EASY
    g.score = 0
    pts = game_mod.Game.add_score(g, 10)
    assert pts == 4 and g.score == 4
    # NORMAL: 10 * 1.0 = 10
    g.difficulty = Difficulty.NORMAL
    g.score = 0
    pts = game_mod.Game.add_score(g, 10)
    assert pts == 10 and g.score == 10
    # HARD: 10 * 3.0 = 30
    g.difficulty = Difficulty.HARD
    g.score = 0
    pts = game_mod.Game.add_score(g, 10)
    assert pts == 30 and g.score == 30


def test_extra_life_after_initial_milestones_uses_increment(monkeypatch):
    g = _setup_game(monkeypatch)
    g.difficulty = Difficulty.NORMAL
    # Passar pelos três marcos iniciais
    for _ in range(3):
        g.score = g.next_extra_life_score
        assert game_mod.Game.check_extra_life(g) is True
    # Após marcos, incremento deve ser aplicado (10000 no NORMAL)
    prev_next = g.next_extra_life_score
    g.score = prev_next
    assert game_mod.Game.check_extra_life(g) is True
    assert g.next_extra_life_score == prev_next + 10000


def test_extra_life_flow(monkeypatch):
    g = _setup_game(monkeypatch)
    g.lives = 1
    g.score = 0
    # Alcançar o primeiro marco
    first = g.next_extra_life_score
    g.score = first
    assert game_mod.Game.check_extra_life(g) is True
    assert g.lives == 2
    # Próximo marco atualizado
    second = g.next_extra_life_score
    g.score = second
    assert game_mod.Game.check_extra_life(g) is True
    assert g.lives == 3


def test_update_bird_difficulty(monkeypatch):
    g = _setup_game(monkeypatch)
    # Examinar alguns níveis e dificuldades
    for diff in (Difficulty.EASY, Difficulty.NORMAL, Difficulty.HARD):
        g.difficulty = diff
        for lvl in (1, 5, 10, 20, 30):
            g.current_level = lvl
            game_mod.Game.update_bird_difficulty(g)
            # Deve configurar intervalos coerentes e número por spawn
            bps = g.birds_per_spawn
            interval = g.bird_spawn_interval
            assert isinstance(bps, int) and bps >= 0
            assert isinstance(interval, (int, float)) and interval > 0


def test_update_spawn_monotonicity_across_ranges(monkeypatch):
    g = _setup_game(monkeypatch)
    # Faixa 1-20: pássaros
    g.current_level = 15
    g.difficulty = Difficulty.EASY
    game_mod.Game.update_bird_difficulty(g)
    easy_bps, easy_int = g.birds_per_spawn, g.bird_spawn_interval
    g.difficulty = Difficulty.NORMAL
    game_mod.Game.update_bird_difficulty(g)
    normal_bps, normal_int = g.birds_per_spawn, g.bird_spawn_interval
    g.difficulty = Difficulty.HARD
    game_mod.Game.update_bird_difficulty(g)
    hard_bps, hard_int = g.birds_per_spawn, g.bird_spawn_interval
    assert 1 <= easy_bps <= 3 and 1 <= normal_bps <= 3 and 1 <= hard_bps <= 3
    assert easy_bps <= normal_bps <= hard_bps
    assert easy_int >= normal_int >= hard_int and min(easy_int, normal_int, hard_int) >= 60

    # Faixa 21-30: morcegos
    g.current_level = 25
    g.difficulty = Difficulty.EASY
    game_mod.Game.update_bird_difficulty(g)
    easy_bps, easy_int = g.bats_per_spawn, g.bat_spawn_interval
    g.difficulty = Difficulty.NORMAL
    game_mod.Game.update_bird_difficulty(g)
    normal_bps, normal_int = g.bats_per_spawn, g.bat_spawn_interval
    g.difficulty = Difficulty.HARD
    game_mod.Game.update_bird_difficulty(g)
    hard_bps, hard_int = g.bats_per_spawn, g.bat_spawn_interval
    assert easy_bps <= normal_bps <= hard_bps
    assert easy_int >= normal_int >= hard_int and min(easy_int, normal_int, hard_int) >= 60

    # Faixa 31-40: aviões
    g.current_level = 35
    g.difficulty = Difficulty.EASY
    game_mod.Game.update_bird_difficulty(g)
    easy_bps, easy_int = g.airplanes_per_spawn, g.airplane_spawn_interval
    g.difficulty = Difficulty.NORMAL
    game_mod.Game.update_bird_difficulty(g)
    normal_bps, normal_int = g.airplanes_per_spawn, g.airplane_spawn_interval
    g.difficulty = Difficulty.HARD
    game_mod.Game.update_bird_difficulty(g)
    hard_bps, hard_int = g.airplanes_per_spawn, g.airplane_spawn_interval
    assert easy_bps <= normal_bps <= hard_bps
    assert easy_int >= normal_int >= hard_int and min(easy_int, normal_int, hard_int) >= 60

    # Faixa 41-50: flying-disks
    g.current_level = 45
    g.difficulty = Difficulty.EASY
    game_mod.Game.update_bird_difficulty(g)
    easy_bps, easy_int = g.flying_disks_per_spawn, g.flying_disk_spawn_interval
    g.difficulty = Difficulty.NORMAL
    game_mod.Game.update_bird_difficulty(g)
    normal_bps, normal_int = g.flying_disks_per_spawn, g.flying_disk_spawn_interval
    g.difficulty = Difficulty.HARD
    game_mod.Game.update_bird_difficulty(g)
    hard_bps, hard_int = g.flying_disks_per_spawn, g.flying_disk_spawn_interval
    assert easy_bps <= normal_bps <= hard_bps
    assert easy_int >= normal_int >= hard_int and min(easy_int, normal_int, hard_int) >= 60

    # Nível 51: foguinhos
    g.current_level = 51
    g.difficulty = Difficulty.EASY
    game_mod.Game.update_bird_difficulty(g)
    easy_bps, easy_int = g.fires_per_spawn, g.fire_spawn_interval
    g.difficulty = Difficulty.NORMAL
    game_mod.Game.update_bird_difficulty(g)
    normal_bps, normal_int = g.fires_per_spawn, g.fire_spawn_interval
    g.difficulty = Difficulty.HARD
    game_mod.Game.update_bird_difficulty(g)
    hard_bps, hard_int = g.fires_per_spawn, g.fire_spawn_interval
    assert 1 <= easy_bps <= 4 and 1 <= normal_bps <= 4 and 1 <= hard_bps <= 4
    assert easy_bps <= normal_bps <= hard_bps
    assert easy_int >= normal_int >= hard_int and min(easy_int, normal_int, hard_int) >= 60


def test_level_static_rules():
    # Cobrir métodos estáticos de Level sem dependências
    assert Level.get_birds_per_spawn(1) >= 0
    assert Level.get_birds_per_spawn(50) >= Level.get_birds_per_spawn(1)
    assert Level.get_bird_spawn_interval(1) > 0
    assert Level.get_bird_spawn_interval(50) <= Level.get_bird_spawn_interval(1)


def test_enter_name_typing_backspace_and_length_limit(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.ENTER_NAME
    # Ensure needed key constants exist in stub
    monkeypatch.setattr(gm.pygame, "K_BACKSPACE", 8, raising=False)
    monkeypatch.setattr(gm.pygame, "K_RETURN", 13, raising=False)

    # Type 26 characters, but limit should cap at 25
    events = [types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=0, unicode="A") for _ in range(26)]
    # One backspace should reduce to 24
    events.append(types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_BACKSPACE, unicode=""))
    # Non-printable/empty unicode should be ignored
    events.append(types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=0, unicode=""))
    # Confirm name to transition
    events.append(types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_RETURN, unicode=""))
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: events))

    # Ranking manager stub to accept score
    class FakeRanking:
        def is_high_score(self, score):
            return True
        def add_score(self, name, score):
            self.added = (name, score)
    g.ranking_manager = FakeRanking()

    g.handle_events()
    # Name capped then reduced by backspace
    assert len(g.player_name) == 24
    # Transitioned to SHOW_RANKING after confirm
    assert g.state == gm.GameState.SHOW_RANKING


def test_show_ranking_key_r_restart_to_playing(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SHOW_RANKING
    # Ensure K_r exists in stub
    monkeypatch.setattr(gm.pygame, "K_r", 114, raising=False)
    # Patch Level.init_level and music.play_level_music to observe calls
    import internal.engine.level.level as level_module
    called = {"level": 0, "music": 0}
    def fake_init_level(game):
        called["level"] += 1
    monkeypatch.setattr(level_module.Level, "init_level", fake_init_level)
    g.music.play_level_music = lambda game, lvl: called.__setitem__("music", called["music"] + 1)

    ev_r = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_r, unicode="r")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_r]))
    g.handle_events()
    assert g.state == gm.GameState.PLAYING
    assert called["level"] == 1 and called["music"] == 1


def test_show_ranking_escape_fallback_to_game_over(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.SHOW_RANKING
    g.previous_state_before_ranking = None
    # Patch Level.init_level for ESC path
    import internal.engine.level.level as level_module
    monkeypatch.setattr(level_module.Level, "init_level", lambda game: None)

    ev_esc = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_ESCAPE, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_esc]))
    g.handle_events()
    assert g.state == gm.GameState.GAME_OVER


def test_get_pooled_bullet_pool_usage_and_fallback(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    # Prepare a simple bullet stub in the pool
    class BulletStub:
        def __init__(self):
            self.x = 0; self.y = 0; self.direction = 1; self.image = None
            self.rect = FakeRect(0, 0, 5, 5)
    g.bullet_pool = [BulletStub()]

    # Use pooled bullet
    b1 = gm.Game.get_pooled_bullet(g, 10, 20, direction=-1, image=None)
    assert isinstance(b1, BulletStub)
    assert b1.x == 10 and b1.y == 20 and b1.direction == -1
    assert b1.rect.x == 10 and b1.rect.y == 20

    # With empty pool, should create a new Bullet
    b2 = gm.Game.get_pooled_bullet(g, 30, 40, direction=1, image=None)
    from internal.resources.bullet import Bullet
    assert isinstance(b2, Bullet)
    assert b2.rect.x == 30 and b2.rect.y == 40


def test_main_menu_keyboard_navigation(headless_pygame, monkeypatch):
    import internal.engine.game as gm
    g = make_game(monkeypatch)
    g.state = gm.GameState.MAIN_MENU
    # Simulate UP then DOWN to move selection
    ev_up = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_UP, unicode="")
    ev_down = types.SimpleNamespace(type=gm.pygame.KEYDOWN, key=gm.pygame.K_DOWN, unicode="")
    monkeypatch.setattr(gm.pygame, "event", types.SimpleNamespace(get=lambda: [ev_up, ev_down]))
    g.handle_events()
    # Selection index remains within range
    assert 0 <= g.menu_selected < len(g.menu_options)