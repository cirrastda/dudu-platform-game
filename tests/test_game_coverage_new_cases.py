import pygame
import pytest

from internal.engine.game import Game
from internal.engine.state import GameState
from internal.engine.level.level import Level


def _init_game_for_draw():
    g = Game()
    # Evitar dependências reais de imagens/áudio
    g.music.play_menu_music = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None
    g.music.play_music = lambda *_a, **_k: None
    return g


def test_draw_credits_menu_branches_cover_links_names_blanks(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.CREDITS
    g.credits_type = "menu"

    # Garantir que draw não falhe e execute ramificações do menu
    g.draw()

    # Permanecer em CREDITS durante o draw do menu
    assert g.state == GameState.CREDITS


def test_draw_credits_ending_reaches_end_and_resets_to_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.CREDITS
    g.credits_type = "ending"

    # Aumentar bastante o scroll para cruzar o fim dos créditos
    g.credits_scroll_y = 100000

    # Evitar chamadas reais de mixer
    monkeypatch.setattr(pygame.mixer.music, "stop", lambda: None)

    g.draw()

    # Após fim dos créditos, voltar ao menu e resetar contadores
    assert g.state == GameState.MAIN_MENU
    assert g.credits_scroll_y == 0
    assert g.credits_reset_timer == 0


def test_draw_credits_ending_renders_various_sections(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.CREDITS
    g.credits_type = "ending"

    # Percorrer diferentes posições de scroll para renderizar categorias distintas
    # Escolher valores abaixo do fim para não sair para MAIN_MENU
    for scroll in [0, 500, 1000, 1500, 2000, 2500, 3000]:
        g.credits_scroll_y = scroll
        g.draw()

    # Após múltiplos draws, ainda estamos na tela de créditos
    assert g.state == GameState.CREDITS


def test_draw_records_displays_rankings(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.RECORDS

    # Preencher ranking com alguns valores
    g.ranking_manager.add_score("AAA", 12345)
    g.ranking_manager.add_score("BBBBBBBBBBBBBBBBBB", 987654)  # Nome longo

    # Desenhar tela de recordes; deve executar o loop de linhas
    g.draw()

    # Permanece na tela de recordes após draw
    assert g.state == GameState.RECORDS


def test_keyboard_records_return_to_previous_or_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.RECORDS
    g.previous_state_before_records = GameState.GAME_OVER

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pygame.event.post(evt)
    g.handle_events()
    assert g.state == GameState.GAME_OVER

    # Sem estado anterior, deve voltar ao menu
    g.state = GameState.RECORDS
    g.previous_state_before_records = None
    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pygame.event.post(evt)
    g.handle_events()
    assert g.state == GameState.MAIN_MENU


def test_joystick_title_skip_opening_in_production(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.TITLE_SCREEN
    g.joystick_connected = True
    g.music_started = False

    # Produção e sinalizador ativo para pular abertura
    g.env_config["environment"] = "production"
    g.env_config["skip-opening-video"] = "1"

    g.music.play_menu_music = lambda *_a, **_k: None

    # Simular evento de botão pressionado no joystick
    evt = pygame.event.Event(pygame.JOYBUTTONDOWN, button=0)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_joystick_splash_advances_in_development(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SPLASH
    g.joystick_connected = True

    # Ambiente development permite avançar com joystick
    g.env_config["environment"] = "development"

    evt = pygame.event.Event(pygame.JOYBUTTONDOWN, button=0)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.TITLE_SCREEN


def test_game_over_restart_via_joystick_start_options(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.GAME_OVER
    g.joystick_connected = True

    # Selecionado "Jogar novamente"
    g.game_over_selected = 0
    # Simular presença de itens coletados para cobrir limpeza
    g.collected_extra_life_levels = {1, 2, 3}

    # Stub de init_level e música do nível
    monkeypatch.setattr(Level, "init_level", lambda _g: None)
    g.music.play_level_music = lambda *_a, **_k: None

    # Start/Options (botão 6) para reiniciar
    evt = pygame.event.Event(pygame.JOYBUTTONDOWN, button=6)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert getattr(g, "collected_extra_life_levels", set()) == set()


def test_title_screen_no_skip_opening_path(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.TITLE_SCREEN
    g.joystick_connected = True

    # Produção sem sinalizador de skip; caminho não altera estado
    g.env_config["environment"] = "production"
    g.env_config.pop("skip-opening-video", None)

    evt = pygame.event.Event(pygame.JOYBUTTONDOWN, button=0)
    pygame.event.post(evt)
    g.handle_events()
    # Sem skip, deve ir para vídeo de abertura
    assert g.state == GameState.OPENING_VIDEO


def test_opening_and_ending_video_draw_paths(monkeypatch):
    g = _init_game_for_draw()

    # Abrir vídeo de abertura
    g.state = GameState.OPENING_VIDEO
    g.video_player.draw = lambda *_a, **_k: None
    g.draw()

    # Abrir vídeo de ending
    g.state = GameState.ENDING_VIDEO
    g.ending_video_player.draw = lambda *_a, **_k: None
    g.draw()


def test_keyboard_title_skip_opening_to_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.TITLE_SCREEN
    g.music_started = False

    # Produção com skip-opening ativado via ENV_CONFIG
    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"
    game_module.ENV_CONFIG["skip-opening-video"] = "1"

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_keyboard_title_opening_video_load_fails_fallback_to_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.TITLE_SCREEN

    # Produção sem skip; forçar falha de load_video
    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"
    game_module.ENV_CONFIG.pop("skip-opening-video", None)

    g.video_player.load_video = lambda _path: False

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_keyboard_opening_video_any_key_skips_to_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.OPENING_VIDEO
    g.music_started = False

    g.video_player.stop = lambda: None

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_keyboard_fim_screen_to_credits_ending(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.FIM_SCREEN

    # Garantir que a música de créditos não cause efeitos colaterais
    g.music.play_music = lambda *_a, **_k: None

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.CREDITS
    assert g.credits_type == "ending"


def test_keyboard_select_difficulty_escape_back_to_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SELECT_DIFFICULTY

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_keyboard_main_menu_navigation_calls_selection(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.MAIN_MENU
    g.menu_options = ["Jogar", "Recordes", "Sair"]

    called = {"select": False}
    def fake_handle_selection():
        called["select"] = True
    g.handle_menu_selection = fake_handle_selection

    # Navegar para baixo e confirmar
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    g.handle_events()

    assert called["select"] is True


def test_keyboard_title_skip_opening_env_exception_path(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.TITLE_SCREEN
    g.music_started = False

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"
    game_module.ENV_CONFIG.pop("skip-opening-video", None)

    # Provocar exceção ao acessar env_config.get
    g.env_config = None

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.OPENING_VIDEO


def test_keyboard_select_difficulty_apply_invalid_initial_stage_dev(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SELECT_DIFFICULTY
    g.difficulty_selected = 1

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "development"
    game_module.ENV_CONFIG["initial-stage"] = "abc"  # inválido para acionar except

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_keyboard_game_over_restart_invalid_initial_stage_dev(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 0

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "development"
    game_module.ENV_CONFIG["initial-stage"] = "x"  # inválido

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_keyboard_show_ranking_restart_to_playing_production(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SHOW_RANKING
    g.max_lives = 3

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"  # aciona ramo else

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_joystick_title_skip_opening_env_exception_path(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.TITLE_SCREEN
    g.joystick_connected = True
    g.env_config = None  # provocar exceção

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"

    evt = pygame.event.Event(pygame.JOYBUTTONDOWN, button=0)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.OPENING_VIDEO


def test_joystick_select_difficulty_confirm_starts_game(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SELECT_DIFFICULTY
    g.difficulty_selected = 2
    g.joystick_connected = True

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=7))
    g.handle_events()

    assert g.state == GameState.PLAYING


def test_joystick_show_ranking_button_back_to_menu(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SHOW_RANKING
    g.joystick_connected = True
    # Sem estado anterior para forçar fallback

    evt = pygame.event.Event(pygame.JOYBUTTONDOWN, button=7)
    pygame.event.post(evt)
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_joystick_show_ranking_button_back_to_previous_state(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SHOW_RANKING
    g.joystick_connected = True
    g.previous_state_before_ranking = GameState.GAME_OVER

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=7))
    g.handle_events()

    assert g.state == GameState.GAME_OVER


def test_joystick_select_difficulty_confirm_normal_starts_game(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SELECT_DIFFICULTY
    g.difficulty_selected = 1  # NORMAL via else
    g.joystick_connected = True

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    g.handle_events()

    assert g.state == GameState.PLAYING


def test_joystick_restart_invalid_initial_stage_dev(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.VICTORY
    g.joystick_connected = True

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "development"
    game_module.ENV_CONFIG["initial-stage"] = "bad"  # inválido

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_joystick_show_ranking_b_button_fallback_to_game_over(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SHOW_RANKING
    g.joystick_connected = True
    g.previous_state_before_ranking = None

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=1))
    g.handle_events()

    assert g.state == GameState.MAIN_MENU


def test_keyboard_credits_ending_esc_does_not_exit(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.CREDITS
    g.credits_type = "ending"

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    result = g.handle_events()

    assert g.state == GameState.CREDITS
    assert result is None or result is True


def test_keyboard_esc_in_playing_exits_game(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.PLAYING

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    result = g.handle_events()

    assert result is False


def test_joystick_game_over_restart_invalid_initial_stage_dev(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 0
    g.joystick_connected = True

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "development"
    game_module.ENV_CONFIG["initial-stage"] = "bad"  # inválido

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert g.current_level == 1


def test_joystick_show_ranking_b_button_returns_previous(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.SHOW_RANKING
    g.joystick_connected = True
    g.previous_state_before_ranking = GameState.GAME_OVER

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=1))
    g.handle_events()

    assert g.state == GameState.GAME_OVER


def test_joystick_restart_clears_collected_items(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.GAME_OVER
    g.game_over_selected = 0
    g.joystick_connected = True
    g.collected_extra_life_levels = {1, 2}
    g.max_lives = 3

    import internal.engine.game as game_module
    game_module.ENV_CONFIG["environment"] = "production"

    Level.init_level = lambda *_a, **_k: None
    g.music.play_level_music = lambda *_a, **_k: None

    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, button=6))
    g.handle_events()

    assert g.state == GameState.PLAYING
    assert getattr(g, "collected_extra_life_levels", set()) == set()


def test_keyboard_credits_menu_esc_back_to_main(monkeypatch):
    g = _init_game_for_draw()
    g.state = GameState.CREDITS
    g.credits_type = "menu"

    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pygame.event.post(evt)
    g.handle_events()
    assert g.state == GameState.MAIN_MENU