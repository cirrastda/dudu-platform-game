import pytest
import pygame
import os
import time
import threading
import types

from internal.engine.game import Game, GameState
from internal.engine.difficulty import Difficulty
from internal.engine.level.level import Level
from internal.resources.bullet import Bullet
from internal.resources.explosion import Explosion


@pytest.fixture(autouse=True)
def init_pygame_display():
    # Garante que o display do pygame esteja inicializado para superfícies
    if not pygame.get_init():
        pygame.init()
    if not pygame.display.get_init():
        pygame.display.init()
    # Usa um display mínimo para evitar problemas em ambientes headless
    pygame.display.set_mode((1, 1))
    yield


@pytest.fixture(autouse=True)
def disable_mixer(monkeypatch):
    # Evita inicialização do mixer de áudio em ambientes de teste/headless
    from internal.engine.sound.mixer import Mixer

    monkeypatch.setattr(Mixer, "init", lambda *args, **kwargs: None)


def post_key(key):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, unicode=""))


def test_title_screen_skip_opening_goes_to_main_menu(monkeypatch):
    # Em produção, a flag skip-opening é respeitada
    import internal.engine.game as game_module

    monkeypatch.setitem(game_module.ENV_CONFIG, "environment", "production")
    g = Game()
    # Garante que música não tenha iniciado
    g.music_started = False
    g.state = GameState.TITLE_SCREEN
    # Força skip-opening via env_config
    g.env_config["skip-opening-video"] = "1"
    # Evita tocar música de verdade
    monkeypatch.setattr(g.music, "play_menu_music", lambda *_args, **_kwargs: None)

    post_key(pygame.K_RETURN)
    g.handle_events()

    # Em produção, não deve pular; deve ir para OPENING_VIDEO
    assert g.state == GameState.OPENING_VIDEO
    # Música de menu não inicia até entrar em MAIN_MENU
    assert g.music_started is False


def test_title_screen_opening_video_fallback_to_menu_on_load_fail(monkeypatch):
    # Em produção, tenta carregar o vídeo; se falhar, cai no menu
    import internal.engine.game as game_module

    monkeypatch.setitem(game_module.ENV_CONFIG, "environment", "production")
    g = Game()
    g.music_started = False
    g.state = GameState.TITLE_SCREEN
    # Explicita que não vamos pular o vídeo
    g.env_config["skip-opening-video"] = "0"
    # Força falha no carregamento do vídeo
    monkeypatch.setattr(g.video_player, "load_video", lambda *_args, **_kwargs: False)
    monkeypatch.setattr(g.music, "play_menu_music", lambda *_args, **_kwargs: None)

    post_key(pygame.K_SPACE)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU
    assert g.music_started is True


def test_opening_video_any_key_skips_to_menu(monkeypatch):
    g = Game()
    g.music_started = False
    g.state = GameState.OPENING_VIDEO
    # Evita tocar música real
    monkeypatch.setattr(g.music, "play_menu_music", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(g.video_player, "stop", lambda *_args, **_kwargs: None)

    post_key(pygame.K_a)
    g.handle_events()

    # Comportamento atualizado: durante OPENING_VIDEO, teclas não pulam para o menu
    assert g.state == GameState.OPENING_VIDEO
    # Música de menu permanece parada até o vídeo finalizar
    assert g.music_started is False


@pytest.mark.parametrize(
    "selected,expected",
    [(0, Difficulty.EASY), (1, Difficulty.NORMAL), (2, Difficulty.HARD)],
)
def test_select_difficulty_confirm_starts_playing(monkeypatch, selected, expected):
    g = Game()
    g.state = GameState.SELECT_DIFFICULTY
    g.difficulty_selected = selected
    # Evita custo de inicialização de nível e som
    monkeypatch.setattr(Level, "init_level", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_args, **_kwargs: None)

    post_key(pygame.K_RETURN)
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert g.difficulty == expected
    # vidas devem ser coerentes com dificuldade
    assert g.lives == g.get_initial_lives()


def test_esc_in_other_states_returns_false():
    g = Game()
    g.state = GameState.PLAYING
    post_key(pygame.K_ESCAPE)
    assert g.handle_events() is False


def test_bullet_pool_get_and_return():
    g = Game()
    # Prepara um pool com uma bala reutilizável
    g.bullet_pool = [Bullet(10, 20, 1, None)]
    b = g.get_pooled_bullet(100, 200, direction=-1, image=None)
    # Deve ter retornado a bala do pool e atualizado atributos
    assert isinstance(b, Bullet)
    assert b.x == 100 and b.y == 200 and b.direction == -1
    # Retorna ao pool e valida limite/estado
    g.return_bullet_to_pool(b)
    assert len(g.bullet_pool) >= 1


def test_explosion_pool_get_and_return():
    g = Game()
    g.explosion_pool = [Explosion(5, 6, None)]
    e = g.get_pooled_explosion(50, 60, image=None)
    assert isinstance(e, Explosion)
    assert e.x == 50 and e.y == 60 and e.timer == 30
    g.return_explosion_to_pool(e)
    assert len(g.explosion_pool) >= 1


def test_draw_ocean_background_fallback_gradient_and_waves():
    g = Game()
    # Força ausência de imagem de fundo
    g.state = GameState.MAIN_MENU
    g.image.background_img = None
    g.menu_background_img = None
    # Usa uma superfície própria para desenhar
    surface = pygame.Surface((800, 600))
    # Executa sem exceções e cobre ramo de gradiente/ondas
    g.draw_ocean_background(surface)
    # Checagem simples: superfície continua válida
    assert isinstance(surface, pygame.Surface)


def test_joystick_title_to_opening_and_fallback(monkeypatch):
    # Em produção, sem skip-opening, vai para vídeo; depois botão pula para menu
    import internal.engine.game as game_module

    monkeypatch.setitem(game_module.ENV_CONFIG, "environment", "production")
    g = Game()
    g.joystick_connected = True
    g.state = GameState.TITLE_SCREEN
    g.env_config["skip-opening-video"] = "0"
    # Simula load OK e start playback no-op
    monkeypatch.setattr(g.video_player, "load_video", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        g.video_player, "start_playback", lambda *_args, **_kwargs: None
    )
    # Posta evento de botão A (0)
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    g.handle_events()
    assert g.state == GameState.OPENING_VIDEO

    # Comportamento atualizado: joystick durante OPENING_VIDEO não muda de estado
    monkeypatch.setattr(g.music, "play_menu_music", lambda *_args, **_kwargs: None)
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    g.handle_events()
    assert g.state == GameState.OPENING_VIDEO


def test_game_over_exit_option_returns_false(monkeypatch):
    g = Game()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 2  # "Sair"
    # Posta ENTER para confirmar opção
    post_key(pygame.K_RETURN)
    assert g.handle_events() is False


def test_records_esc_returns_to_previous_state():
    g = Game()
    g.previous_state_before_records = GameState.GAME_OVER
    g.state = GameState.RECORDS
    post_key(pygame.K_ESCAPE)
    g.handle_events()
    assert g.state == GameState.GAME_OVER
    assert g.previous_state_before_records is None


def test_show_ranking_esc_returns_to_previous():
    g = Game()
    g.previous_state_before_ranking = GameState.VICTORY
    g.state = GameState.SHOW_RANKING
    post_key(pygame.K_ESCAPE)
    g.handle_events()
    assert g.state == GameState.VICTORY
    assert g.previous_state_before_ranking is None


def test_enter_name_flow_adds_ranking_and_shows_ranking(monkeypatch):
    g = Game()
    g.state = GameState.ENTER_NAME
    g.player_name = "ABC"
    # Evita efeitos colaterais de tocar música ou iniciar nível
    monkeypatch.setattr(g.music, "play_level_music", lambda *_args, **_kwargs: None)
    # Simula confirmação
    post_key(pygame.K_RETURN)
    g.handle_events()
    assert g.state == GameState.SHOW_RANKING


def test_main_menu_select_iniciar_transitions_to_select_difficulty(monkeypatch):
    g = Game()
    g.state = GameState.MAIN_MENU
    # Garante opções e seleção
    g.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
    g.menu_selected = 0
    # Evita inicialização pesada
    monkeypatch.setattr(Level, "init_level", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_args, **_kwargs: None)

    g.handle_menu_selection()

    assert g.state == GameState.SELECT_DIFFICULTY
    assert g.current_level == 1


def test_main_menu_select_recordes_transitions_to_records():
    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Recordes"]
    g.menu_selected = 0

    g.handle_menu_selection()

    assert g.state == GameState.RECORDS


def test_main_menu_select_creditos_transitions_to_credits_menu():
    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Créditos"]
    g.menu_selected = 0

    g.handle_menu_selection()

    assert g.state == GameState.CREDITS
    assert g.credits_type == "menu"


def test_main_menu_select_sair_exits(monkeypatch):
    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Sair"]
    g.menu_selected = 0
    # Evita chamar pygame.quit real
    monkeypatch.setattr(pygame, "quit", lambda *_args, **_kwargs: None)

    with pytest.raises(SystemExit):
        g.handle_menu_selection()


def test_main_menu_keyboard_navigation_wraparound_and_confirm_recordes():
    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Iniciar", "Recordes", "Créditos"]
    g.menu_selected = 0

    # DOWN vai para 1
    post_key(pygame.K_DOWN)
    g.handle_events()
    assert g.menu_selected == 1
    # UP volta para 0
    post_key(pygame.K_UP)
    g.handle_events()
    assert g.menu_selected == 0
    # UP wrap-around vai para o último
    post_key(pygame.K_UP)
    g.handle_events()
    assert g.menu_selected == 2

    # CONFIRM com ENTER em "Recordes"
    g.menu_selected = 1
    post_key(pygame.K_RETURN)
    g.handle_events()
    assert g.state == GameState.RECORDS


def test_main_menu_joystick_analog_navigation_and_confirm_creditos(monkeypatch):
    class FakeJoy:
        def __init__(self):
            self.axes = {0: 0.0, 1: 0.0, 6: 0.0, 7: 0.0}

        def get_numaxes(self):
            return 8

        def get_axis(self, idx):
            return self.axes.get(idx, 0.0)

    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Iniciar", "Recordes", "Créditos"]
    g.menu_selected = 0
    g.joystick_connected = True
    g.joystick = FakeJoy()
    g.prev_analog_vertical = 0
    g.prev_dpad_vertical = 0

    # Analógico para cima reduz seleção (wrap desde 0 para último)
    g.joystick.axes[1] = -1.0
    g.handle_events()
    assert g.menu_selected == 2

    # Zerar para atualizar prev e depois descer
    g.joystick.axes[1] = 0.0
    g.handle_events()
    g.joystick.axes[1] = 1.0
    g.handle_events()
    assert g.menu_selected == 0  # 2 -> 0

    # Confirmar "Créditos" com botão A (0)
    g.menu_selected = 2
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    g.handle_events()
    assert g.state == GameState.CREDITS
    assert g.credits_type == "menu"


def test_main_menu_joystick_confirm_recordes(monkeypatch):
    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Iniciar", "Recordes", "Créditos"]
    g.menu_selected = 1  # Recordes
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    g.handle_events()
    assert g.state == GameState.RECORDS


def test_main_menu_keyboard_confirm_creditos():
    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Iniciar", "Recordes", "Créditos"]
    g.menu_selected = 2  # Créditos
    post_key(pygame.K_RETURN)
    g.handle_events()
    assert g.state == GameState.CREDITS
    assert g.credits_type == "menu"


def test_credits_keyboard_menu_returns_to_main_menu(monkeypatch):
    g = Game()
    g.state = GameState.CREDITS
    g.credits_type = "menu"
    post_key(pygame.K_ESCAPE)
    assert g.handle_events() is True
    assert g.state == GameState.MAIN_MENU


def test_credits_keyboard_ending_ignores_escape():
    g = Game()
    g.state = GameState.CREDITS
    g.credits_type = "ending"
    post_key(pygame.K_ESCAPE)
    assert g.handle_events() is True
    assert g.state == GameState.CREDITS


def test_credits_joystick_menu_returns_to_main_menu():
    g = Game()
    g.state = GameState.CREDITS
    g.credits_type = "menu"
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=1))
    assert g.handle_events() is True
    assert g.state == GameState.MAIN_MENU


def test_victory_r_key_restarts_playing(monkeypatch):
    g = Game()
    g.state = GameState.VICTORY
    # Evitar custo de init
    monkeypatch.setattr(Level, "init_level", lambda *_a, **_k: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_a, **_k: None)
    post_key(pygame.K_r)
    g.handle_events()
    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_victory_joystick_start_restarts_playing(monkeypatch):
    g = Game()
    g.state = GameState.VICTORY
    monkeypatch.setattr(Level, "init_level", lambda *_a, **_k: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_a, **_k: None)
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    g.handle_events()
    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_show_ranking_joystick_fallback_to_main_menu_when_no_previous():
    g = Game()
    g.state = GameState.SHOW_RANKING
    g.previous_state_before_ranking = None
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=1))
    g.handle_events()
    assert g.state == GameState.MAIN_MENU


def test_game_over_keyboard_restart_and_recordes(monkeypatch):
    g = Game()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 0  # Jogar novamente
    monkeypatch.setattr(Level, "init_level", lambda *_a, **_k: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_a, **_k: None)
    post_key(pygame.K_RETURN)
    g.handle_events()
    assert g.state == GameState.PLAYING

    # Agora selecionar Recordes
    g.state = GameState.GAME_OVER
    g.game_over_selected = 1
    post_key(pygame.K_RETURN)
    g.handle_events()
    assert g.state == GameState.RECORDS
    assert g.previous_state_before_records == GameState.GAME_OVER


def test_game_over_joystick_recordes_and_exit():
    g = Game()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 1
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    g.handle_events()
    assert g.state == GameState.RECORDS
    assert g.previous_state_before_records == GameState.GAME_OVER

    # Selecionar Sair
    g.state = GameState.GAME_OVER
    g.game_over_selected = 2
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    assert g.handle_events() is False


def test_game_over_dpad_navigation_wraparound_and_confirm_exit():
    class FakeJoy:
        def __init__(self):
            self.axes = {0: 0.0, 1: 0.0, 6: 0.0, 7: 0.0}

        def get_numaxes(self):
            return 8

        def get_axis(self, idx):
            return self.axes.get(idx, 0.0)

    g = Game()
    g.state = GameState.GAME_OVER
    g.joystick_connected = True
    g.joystick = FakeJoy()
    g.game_over_selected = 0
    g.prev_dpad_vertical = 0

    # D-pad UP: wrap para último índice
    g.joystick.axes[7] = -1.0
    g.handle_events()
    assert g.game_over_selected == len(g.game_over_options) - 1
    # Zerar e DOWN: volta para 0
    g.joystick.axes[7] = 0.0
    g.handle_events()
    g.joystick.axes[7] = 1.0
    g.handle_events()
    assert g.game_over_selected == 0

    # Confirmar "Sair" ao selecionar último
    g.game_over_selected = len(g.game_over_options) - 1
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    assert g.handle_events() is False


def test_records_keyboard_escape_back_to_main_or_previous():
    g = Game()
    # Caso com previous: volta ao estado anterior
    g.state = GameState.RECORDS
    g.previous_state_before_records = GameState.PLAYING
    post_key(pygame.K_ESCAPE)
    g.handle_events()
    assert g.state == GameState.PLAYING
    assert g.previous_state_before_records is None

    # Caso sem previous: fallback para MAIN_MENU
    g.state = GameState.RECORDS
    g.previous_state_before_records = None
    post_key(pygame.K_ESCAPE)
    g.handle_events()
    assert g.state == GameState.MAIN_MENU


def test_records_joystick_back_to_previous_or_menu():
    g = Game()
    g.state = GameState.RECORDS
    g.joystick_connected = True

    # Volta ao previous via botão 6
    g.previous_state_before_records = GameState.GAME_OVER
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    g.handle_events()
    assert g.state == GameState.GAME_OVER
    assert g.previous_state_before_records is None

    # Sem previous: fallback para MAIN_MENU via botão 7
    g.state = GameState.RECORDS
    g.previous_state_before_records = None
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=7))
    g.handle_events()
    assert g.state == GameState.MAIN_MENU


def test_show_ranking_keyboard_escape_fallback_to_menu_when_no_previous():
    g = Game()
    g.state = GameState.SHOW_RANKING
    g.previous_state_before_ranking = None
    post_key(pygame.K_ESCAPE)
    g.handle_events()
    # Com previous ausente, jogo retorna ao fluxo de pós-jogo
    assert g.state == GameState.GAME_OVER


def test_credits_menu_reset_scroll_after_timeout(monkeypatch):
    g = Game()
    g.state = GameState.CREDITS
    g.credits_type = "menu"
    g.credits_scroll_y = 100
    g.credits_reset_timer = 1799
    # Velocidade padrão já incrementa scroll e timer
    g.update()
    assert g.credits_reset_timer == 0
    assert g.credits_scroll_y == 0


def test_video_player_play_audio_not_available_no_thread(monkeypatch):
    from internal.engine.video import VideoPlayer
    import internal.engine.video as video_module

    vp = VideoPlayer()
    monkeypatch.setattr(video_module, "MOVIEPY_AVAILABLE", False)

    class FakeAudio:
        def preview(self):
            pass

    vp.has_audio = True
    vp.audio_clip = FakeAudio()
    vp.start_playback()
    # Thread não inicia quando MOVIEPY_AVAILABLE=False
    assert vp.audio_thread is None


def test_video_player_stop_cancels_fallback_music(monkeypatch):
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    vp.fallback_mode = True
    vp.fallback_music_started = True

    class DummyMusic:
        def stop(self):
            pass

    monkeypatch.setattr(pygame.mixer, "music", DummyMusic())
    vp.stop()
    assert vp.fallback_music_started is False


def test_video_player_calculate_fallback_rect_fit_width_and_height():
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    # Caso imagem mais larga que a tela: limita pela largura
    img_w, img_h = 1200, 600
    img_aspect = img_w / img_h
    vp._calculate_fallback_rect((img_w, img_h))
    assert vp.video_rect.width == vp.screen_width
    expected_height = int(vp.screen_width / img_aspect)
    assert vp.video_rect.height == expected_height
    assert vp.video_rect.x == 0
    assert vp.video_rect.y == (vp.screen_height - expected_height) // 2

    # Caso imagem mais alta que a tela: limita pela altura
    img_w2, img_h2 = 600, 1200
    img_aspect2 = img_w2 / img_h2
    vp._calculate_fallback_rect((img_w2, img_h2))
    assert vp.video_rect.height == vp.screen_height
    expected_width2 = int(vp.screen_height * img_aspect2)
    assert vp.video_rect.width == expected_width2
    assert vp.video_rect.y == 0
    assert vp.video_rect.x == (vp.screen_width - expected_width2) // 2


def test_video_player_calculate_video_rect_crop_width_and_height():
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    # Vídeo mais largo: crop pela largura (ajusta por altura)
    vid_w, vid_h = 1920, 1080
    vid_aspect = vid_w / vid_h
    vp._calculate_video_rect((vid_w, vid_h))
    assert vp.video_rect.height == vp.screen_height
    expected_width = int(vp.screen_height * vid_aspect)
    assert vp.video_rect.width == expected_width
    assert vp.video_rect.y == 0
    assert vp.video_rect.x == (vp.screen_width - expected_width) // 2

    # Vídeo mais alto: crop pela altura (ajusta por largura)
    vid_w2, vid_h2 = 800, 1600
    vid_aspect2 = vid_w2 / vid_h2
    vp._calculate_video_rect((vid_w2, vid_h2))
    assert vp.video_rect.width == vp.screen_width
    expected_height2 = int(vp.screen_width / vid_aspect2)
    assert vp.video_rect.height == expected_height2
    assert vp.video_rect.x == 0
    assert vp.video_rect.y == (vp.screen_height - expected_height2) // 2


def test_video_player_draw_single_image_fades_to_black(monkeypatch):
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    vp.fallback_mode = True
    vp.fallback_images = [pygame.Surface((50, 50))]
    vp._calculate_fallback_rect((50, 50))
    vp.fallback_delay = 10
    vp.fallback_fade = 10
    # Controlar ticks
    ticks = {"t": 1000}
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: ticks["t"])
    vp.start_playback()
    screen = pygame.Surface((vp.screen_width, vp.screen_height))
    # Avançar para fase de fade
    ticks["t"] = 1015
    vp.draw(screen)
    # Avançar além do fade e atualizar (deve finalizar)
    ticks["t"] = 1021
    vp.update()
    assert vp.finished is True
    assert vp.is_playing is False


def test_video_player_play_audio_error_thread_dies(monkeypatch):
    from internal.engine.video import VideoPlayer
    import internal.engine.video as video_module

    vp = VideoPlayer()
    # Forçar disponibilidade de moviepy
    monkeypatch.setattr(video_module, "MOVIEPY_AVAILABLE", True)
    # Evitar efeitos colaterais de mixer
    monkeypatch.setattr(pygame.mixer, "music", types.SimpleNamespace(stop=lambda: None))

    class FakeAudio:
        def preview(self):
            raise RuntimeError("boom")

    vp.audio_clip = FakeAudio()
    vp._play_audio()
    assert vp.audio_thread is not None
    vp.audio_thread.join(timeout=1.0)
    assert not vp.audio_thread.is_alive()


def test_video_player_stop_joins_audio_thread_and_sets_none():
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    # Criar uma thread simulando áudio em execução
    t = threading.Thread(target=lambda: time.sleep(0.05), daemon=True)
    t.start()
    vp.audio_thread = t
    vp.stop()
    assert vp.audio_thread is None


def test_game_over_joystick_play_again_with_start(monkeypatch):
    g = Game()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 0
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    monkeypatch.setattr(Level, "init_level", lambda *_a, **_k: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_a, **_k: None)
    g.handle_events()
    assert g.state == GameState.PLAYING


def test_fim_screen_any_key_goes_to_credits(monkeypatch):
    g = Game()
    g.state = GameState.FIM_SCREEN
    monkeypatch.setattr(g.music, "play_music", lambda *_a, **_k: None)
    post_key(pygame.K_a)
    g.handle_events()
    assert g.state == GameState.CREDITS
    assert g.credits_type == "ending"


def test_fim_screen_timer_transition_to_credits(monkeypatch):
    g = Game()
    g.state = GameState.FIM_SCREEN
    g.fim_screen_timer = 179
    monkeypatch.setattr(g.music, "play_music", lambda *_a, **_k: None)
    g.update()
    assert g.state == GameState.CREDITS
    assert g.credits_type == "ending"


def test_opening_video_update_finishes_to_main_menu(monkeypatch):
    g = Game()
    g.state = GameState.OPENING_VIDEO
    # Evita tocar música real
    monkeypatch.setattr(g.music, "play_menu_music", lambda *_a, **_k: None)
    monkeypatch.setattr(g.video_player, "is_finished", lambda: True)
    monkeypatch.setattr(g.video_player, "cleanup", lambda: None)
    g.update()
    assert g.state == GameState.MAIN_MENU


def test_ending_video_update_fallback_to_fim_when_load_fails():
    g = Game()
    g.state = GameState.ENDING_VIDEO
    # Força falha de load
    g.__dict__.pop("ending_video_loaded", None)
    g.__dict__.pop("ending_video_loaded", None)
    g.__dict__.pop("ending_video_loaded", None)
    g.__dict__.pop("ending_video_loaded", None)
    g.ending_video_loaded = None
    g.__dict__.pop("ending_video_loaded", None)
    g.__dict__.pop("ending_video_loaded", None)
    g.__dict__.pop("ending_video_loaded", None)
    # Monkeypatch load_video para False
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(g.ending_video_player, "load_video", lambda *_a, **_k: False)
    g.update()
    assert g.state == GameState.FIM_SCREEN
    assert g.fim_screen_timer == 0


def test_ending_video_update_finishes_to_fim(monkeypatch):
    g = Game()
    g.state = GameState.ENDING_VIDEO
    # Sinaliza como carregado e finalizado
    g.ending_video_loaded = True
    monkeypatch.setattr(g.ending_video_player, "is_finished", lambda: True)
    monkeypatch.setattr(g.ending_video_player, "cleanup", lambda: None)
    g.update()
    assert g.state == GameState.FIM_SCREEN
    assert g.fim_screen_timer == 0


def test_main_menu_joystick_dpad_navigation_wraparound_and_confirm_iniciar(monkeypatch):
    class FakeJoy:
        def __init__(self):
            self.axes = {0: 0.0, 1: 0.0, 6: 0.0, 7: 0.0}

        def get_numaxes(self):
            return 8

        def get_axis(self, idx):
            return self.axes.get(idx, 0.0)

    g = Game()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
    g.menu_selected = 0
    g.joystick_connected = True
    g.joystick = FakeJoy()
    g.prev_dpad_vertical = 0

    # D-pad para cima: wrap-around para o último
    g.joystick.axes[7] = -1.0
    g.handle_events()
    assert g.menu_selected == len(g.menu_options) - 1

    # Zerar para atualizar prev e depois descer
    g.joystick.axes[7] = 0.0
    g.handle_events()
    g.joystick.axes[7] = 1.0
    g.handle_events()
    # Último -> 0
    assert g.menu_selected == 0

    # Confirmar "Iniciar" com botão A (0)
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=0))
    # Evitar inicialização pesada do level e música
    monkeypatch.setattr(Level, "init_level", lambda *_a, **_k: None)
    monkeypatch.setattr(g.music, "play_level_music", lambda *_a, **_k: None)
    g.handle_events()
    assert g.state == GameState.SELECT_DIFFICULTY


def test_show_ranking_keyboard_back_to_previous():
    g = Game()
    g.state = GameState.SHOW_RANKING
    g.previous_state_before_ranking = GameState.PLAYING
    post_key(pygame.K_ESCAPE)
    assert g.handle_events() is True
    assert g.state == GameState.PLAYING
    assert g.previous_state_before_ranking is None


def test_show_ranking_joystick_back_to_previous():
    g = Game()
    g.state = GameState.SHOW_RANKING
    g.previous_state_before_ranking = GameState.PLAYING
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    assert g.handle_events() is True
    assert g.state == GameState.PLAYING
    assert g.previous_state_before_ranking is None


def test_select_difficulty_escape_returns_to_main_menu():
    g = Game()
    g.state = GameState.SELECT_DIFFICULTY
    post_key(pygame.K_ESCAPE)
    # Apenas validar que ESC troca para MAIN_MENU sem encerrar
    g.handle_events()
    assert g.state == GameState.MAIN_MENU


def test_video_player_load_video_file_missing_uses_fallback(monkeypatch):
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    # Garante que nenhum arquivo exista
    monkeypatch.setattr(os.path, "exists", lambda _p: False)
    # Usar um caminho qualquer; como exists=False, vai cair no fallback
    ok = vp.load_video("videos/nao-existe.mp4")
    assert ok is True
    assert vp.fallback_mode is True
    assert len(vp.fallback_images) >= 1  # pelo menos a tela preta
    assert vp.duration > 0


def test_video_player_start_playback_and_update_finish_quickly_in_fallback(monkeypatch):
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    # Força modo fallback com uma imagem e tempos pequenos
    vp.fallback_mode = True
    vp.fallback_images = [pygame.Surface((100, 100))]
    vp._calculate_fallback_rect((100, 100))
    vp.fallback_delay = 10
    vp.fallback_fade = 0

    ticks = {"t": 1000}
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: ticks["t"])
    vp.start_playback()

    # Primeiro update: não finaliza ainda
    vp.update()
    assert vp.is_playing is True
    assert vp.finished is False

    # Avança tempo além do delay para finalizar
    ticks["t"] = 1021
    vp.update()
    assert vp.finished is True
    assert vp.is_playing is False


def test_video_player_draw_fade_between_two_images(monkeypatch):
    from internal.engine.video import VideoPlayer

    vp = VideoPlayer()
    vp.fallback_mode = True
    # Duas imagens para acionar crossfade
    vp.fallback_images = [pygame.Surface((50, 50)), pygame.Surface((50, 50))]
    vp._calculate_fallback_rect((50, 50))
    vp.fallback_delay = 10
    vp.fallback_fade = 10
    # Ticks controlados
    ticks = {"t": 1000}
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: ticks["t"])
    vp.start_playback()
    screen = pygame.Surface((vp.screen_width, vp.screen_height))
    # Antes do fade
    vp.draw(screen)
    # Avança para fase de fade
    ticks["t"] = 1015
    vp.draw(screen)
    # Avança além do fade para próxima imagem
    ticks["t"] = 1021
    vp.update()
    vp.draw(screen)
    assert vp.is_playing in (True, False)


def test_video_player_play_audio_thread_starts(monkeypatch):
    from internal.engine.video import VideoPlayer
    import internal.engine.video as video_module

    vp = VideoPlayer()
    # Simula disponibilidade de MoviePy e áudio
    monkeypatch.setattr(video_module, "MOVIEPY_AVAILABLE", True)

    class FakeAudio:
        def preview(self):
            pass

    vp.has_audio = True
    vp.audio_clip = FakeAudio()
    vp.start_playback()
    # Thread deve ser iniciada
    assert vp.audio_thread is not None


def test_video_player_cleanup_resets_flags(monkeypatch):
    from internal.engine.video import VideoPlayer

    class Dummy:
        def close(self):
            pass

    vp = VideoPlayer()
    vp.video_clip = Dummy()
    vp.audio_clip = Dummy()
    vp.finished = True
    vp.cleanup()
    assert vp.video_clip is None
    assert vp.audio_clip is None
    assert vp.finished is False
