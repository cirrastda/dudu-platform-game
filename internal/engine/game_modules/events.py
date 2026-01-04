import pygame
from internal.engine.state import GameState
from internal.engine.difficulty import Difficulty
from internal.engine.level.level import Level


class Events:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        game = self.game
        env = getattr(game, "env_config", {})
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                try:
                    uni = event.unicode if hasattr(event, "unicode") else ""
                except Exception:
                    uni = ""
                game._process_cheat_token(
                    game._map_key_to_cheat_token(event.key, uni)
                )
                if game.state == GameState.SPLASH:
                    if env.get("environment", "production") == "development":
                        game.state = GameState.TITLE_SCREEN
                elif game.state == GameState.TITLE_SCREEN:
                    game.state = GameState.OPENING_VIDEO
                    if game.video_player.load_video("videos/opening.mp4"):
                        game.video_player.start_playback()
                    else:
                        game.state = GameState.MAIN_MENU
                        if not game.music_started:
                            game.music.play_menu_music(game)
                            game.music_started = True
                elif game.state == GameState.OPENING_VIDEO:
                    pass
                elif game.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_UP:
                        game.menu_selected = (game.menu_selected - 1) % len(
                            game.menu_options
                        )
                    elif event.key == pygame.K_DOWN:
                        game.menu_selected = (game.menu_selected + 1) % len(
                            game.menu_options
                        )
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game.handle_menu_selection()
                elif game.state == GameState.SELECT_DIFFICULTY:
                    if event.key == pygame.K_UP:
                        game.difficulty_selected = (
                            (game.difficulty_selected - 1)
                            % len(game.difficulty_options)
                        )
                    elif event.key == pygame.K_DOWN:
                        game.difficulty_selected = (
                            (game.difficulty_selected + 1)
                            % len(game.difficulty_options)
                        )
                    elif event.key == pygame.K_ESCAPE:
                        game.state = GameState.MAIN_MENU
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if game.difficulty_selected == 0:
                            game.difficulty = Difficulty.EASY
                        elif game.difficulty_selected == 2:
                            game.difficulty = Difficulty.HARD
                        else:
                            game.difficulty = Difficulty.NORMAL
                        (
                            game.extra_life_milestones,
                            game.extra_life_increment_after_milestones,
                        ) = game.get_extra_life_milestones_and_increment()
                        game.next_extra_life_score = (
                            game.extra_life_milestones[0]
                        )
                        game.extra_lives_earned = 0
                        if (
                            env.get("environment") == "development"
                            and "initial-stage" in env
                        ):
                            try:
                                game.current_level = int(env["initial-stage"])
                                if (
                                    game.current_level < 1
                                    or game.current_level > 50
                                ):
                                    game.current_level = 1
                            except (ValueError, TypeError):
                                game.current_level = 1
                        else:
                            game.current_level = 1
                        game.score = 0
                        game.platforms_jumped.clear()
                        game.birds_dodged.clear()
                        game.player_name = ""
                        game.max_lives = game.get_initial_lives()
                        game.lives = game.max_lives
                        if hasattr(game, "collected_extra_life_levels"):
                            game.collected_extra_life_levels.clear()
                        game.state = GameState.PLAYING
                        Level.init_level(game)
                        game.music.play_level_music(game, game.current_level)
                elif game.state == GameState.FIM_SCREEN:
                    game.state = GameState.CREDITS
                    game.credits_type = "ending"
                    game.music.play_music("credits")
                elif game.state == GameState.PLAYING and (
                    event.key in getattr(game, "controls", {}).get("pause", [pygame.K_ESCAPE])
                ):
                    game.state = GameState.PAUSED
                    game.pause_selected = 0
                    return True
                elif game.state == GameState.PAUSED:
                    if event.key == pygame.K_UP:
                        game.pause_selected = (game.pause_selected - 1) % len(game.pause_menu_options)
                    elif event.key == pygame.K_DOWN:
                        game.pause_selected = (game.pause_selected + 1) % len(game.pause_menu_options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        sel = game.pause_menu_options[game.pause_selected]
                        if sel == "Continuar":
                            game.state = GameState.PLAYING
                        elif sel == "Botões/Teclas":
                            game.options_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_CONTROLS
                        elif sel == "Áudio":
                            game.audio_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_AUDIO
                        elif sel == "Vídeo":
                            game.video_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_VIDEO
                        elif sel == "Acessibilidade":
                            game.access_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_ACCESSIBILITY
                        elif sel == "Sair":
                            game.confirm_dialog_type = "exit_to_menu"
                            game.confirm_selected = 0
                            game.state = GameState.CONFIRM_EXIT_TO_MENU
                    elif event.key == pygame.K_ESCAPE:
                        # ESC também continua
                        game.state = GameState.PLAYING
                        return True
                elif game.state == GameState.OPTIONS_MENU:
                    if event.key == pygame.K_UP:
                        game.options_selected = (game.options_selected - 1) % 5
                    elif event.key == pygame.K_DOWN:
                        game.options_selected = (game.options_selected + 1) % 5
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game.pause_selected = None
                        if game.options_selected == 0:
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_CONTROLS
                        elif game.options_selected == 1:
                            game.audio_selected = 0
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_AUDIO
                        elif game.options_selected == 2:
                            game.video_selected = 0
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_VIDEO
                        elif game.options_selected == 3:
                            game.access_selected = 0
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_ACCESSIBILITY
                        elif game.options_selected == 4:
                            game.state = GameState.MAIN_MENU
                    elif event.key == pygame.K_ESCAPE:
                        game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.OPTIONS_AUDIO:
                    if event.key == pygame.K_UP:
                        game.audio_selected = (game.audio_selected - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        game.audio_selected = (game.audio_selected + 1) % 2
                    elif event.key == pygame.K_LEFT:
                        if game.audio_selected == 0:
                            game.music_volume = max(0.0, game.music_volume - 0.1)
                            try:
                                import pygame as _pg
                                _pg.mixer.music.set_volume(game.music_volume)
                            except Exception:
                                pass
                        else:
                            game.sound_effects.sound_volume = max(0.0, game.sound_effects.sound_volume - 0.1)
                            try:
                                for s in game.sound_effects.sound_effects.values():
                                    s.set_volume(game.sound_effects.sound_volume)
                            except Exception:
                                pass
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_RIGHT:
                        if game.audio_selected == 0:
                            game.music_volume = min(1.0, game.music_volume + 0.1)
                            try:
                                import pygame as _pg
                                _pg.mixer.music.set_volume(game.music_volume)
                            except Exception:
                                pass
                        else:
                            game.sound_effects.sound_volume = min(1.0, game.sound_effects.sound_volume + 0.1)
                            try:
                                for s in game.sound_effects.sound_effects.values():
                                    s.set_volume(game.sound_effects.sound_volume)
                            except Exception:
                                pass
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_r:
                        game.music_volume = 0.7
                        game.sound_effects.sound_volume = 0.8
                        try:
                            import pygame as _pg
                            _pg.mixer.music.set_volume(game.music_volume)
                            for s in game.sound_effects.sound_effects.values():
                                s.set_volume(game.sound_effects.sound_volume)
                        except Exception:
                            pass
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_ESCAPE:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.OPTIONS_VIDEO:
                    if event.key == pygame.K_UP:
                        game.video_selected = (game.video_selected - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        game.video_selected = (game.video_selected + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if game.video_selected == 1:
                            try:
                                game.env_config["fullscreen"] = not game.env_config.get("fullscreen", False)
                                from internal.engine.screen import Screen as _Screen
                                _Screen.init(game)
                            except Exception:
                                pass
                            try:
                                game._save_settings()
                            except Exception:
                                pass
                        elif game.video_selected == 2:
                            try:
                                game.visual_mode = "normal" if getattr(game, "visual_mode", "normal") == "8bit" else "8bit"
                                game._save_settings()
                            except Exception:
                                pass
                    elif event.key == pygame.K_LEFT:
                        if game.video_selected == 0:
                            try:
                                idx = game.window_scales.index(game.env_config.get("window_scale", 1.0))
                            except Exception:
                                idx = 0
                            idx = (idx - 1) % len(game.window_scales)
                            game.env_config["window_scale"] = game.window_scales[idx]
                            try:
                                from internal.engine.screen import Screen as _Screen
                                _Screen.init(game)
                            except Exception:
                                pass
                        elif game.video_selected == 2:
                            try:
                                game.visual_mode = "normal" if getattr(game, "visual_mode", "normal") == "8bit" else "8bit"
                                game._save_settings()
                            except Exception:
                                pass
                    elif event.key == pygame.K_RIGHT:
                        if game.video_selected == 0:
                            try:
                                idx = game.window_scales.index(game.env_config.get("window_scale", 1.0))
                            except Exception:
                                idx = 0
                            idx = (idx + 1) % len(game.window_scales)
                            game.env_config["window_scale"] = game.window_scales[idx]
                            try:
                                from internal.engine.screen import Screen as _Screen
                                _Screen.init(game)
                            except Exception:
                                pass
                        elif game.video_selected == 2:
                            try:
                                game.visual_mode = "normal" if getattr(game, "visual_mode", "normal") == "8bit" else "8bit"
                                game._save_settings()
                            except Exception:
                                pass
                    elif event.key == pygame.K_r:
                        try:
                            game.env_config["fullscreen"] = False
                            game.env_config["window_scale"] = 1.0
                            from internal.engine.screen import Screen as _Screen
                            _Screen.init(game)
                        except Exception:
                            pass
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_ESCAPE:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.OPTIONS_ACCESSIBILITY:
                    if event.key == pygame.K_UP:
                        game.access_selected = (getattr(game, "access_selected", 0) - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        game.access_selected = (getattr(game, "access_selected", 0) + 1) % 2
                    elif event.key == pygame.K_LEFT:
                        if getattr(game, "access_selected", 0) == 0:
                            try:
                                modes = ["none", "deuteranopia", "protanopia", "tritanopia"]
                                idx = modes.index(getattr(game, "colorblind_mode", "none"))
                            except Exception:
                                idx = 0
                            game.colorblind_mode = modes[(idx - 1) % len(modes)]
                        else:
                            game.vibration_enabled = not getattr(game, "vibration_enabled", False)
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_RIGHT:
                        if getattr(game, "access_selected", 0) == 0:
                            try:
                                modes = ["none", "deuteranopia", "protanopia", "tritanopia"]
                                idx = modes.index(getattr(game, "colorblind_mode", "none"))
                            except Exception:
                                idx = 0
                            game.colorblind_mode = modes[(idx + 1) % len(modes)]
                        else:
                            game.vibration_enabled = not getattr(game, "vibration_enabled", False)
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_r:
                        game.colorblind_mode = "none"
                        game.vibration_enabled = False
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    elif event.key == pygame.K_ESCAPE:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.OPTIONS_CONTROLS:
                    if getattr(game, "controls_editing", False):
                        if event.key == pygame.K_ESCAPE:
                            game.controls_editing = False
                            return True
                        else:
                            label, action = game.controls_actions[game.controls_selected]
                            try:
                                game.controls[action] = [event.key]
                                game._save_settings()
                            except Exception:
                                pass
                            game.controls_editing = False
                    else:
                        if event.key == pygame.K_UP:
                            game.controls_selected = (
                                (game.controls_selected - 1) % len(game.controls_actions)
                            )
                        elif event.key == pygame.K_DOWN:
                            game.controls_selected = (
                                (game.controls_selected + 1) % len(game.controls_actions)
                            )
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            game.controls_editing = True
                        elif event.key == pygame.K_r:
                            try:
                                game.controls = {
                                    "left": [pygame.K_LEFT, pygame.K_a],
                                    "right": [pygame.K_RIGHT, pygame.K_d],
                                    "jump": [pygame.K_UP, pygame.K_w],
                                    "shoot": [pygame.K_SPACE],
                                    "crouch": [pygame.K_DOWN, pygame.K_s],
                                    "pause": [pygame.K_ESCAPE],
                                }
                                game.joystick_controls = {
                                    "jump": 0,
                                    "shoot": 1,
                                    "pause": 7,
                                }
                                if getattr(game, "joystick_connected", False):
                                    name = getattr(game, "joystick_name", "")
                                    if name:
                                        game.joystick_profiles[name] = dict(game.joystick_controls)
                                game._save_settings()
                            except Exception:
                                pass
                        elif event.key == pygame.K_ESCAPE:
                            if game.previous_state_before_options:
                                game.state = game.previous_state_before_options
                                game.previous_state_before_options = None
                            else:
                                game.state = GameState.MAIN_MENU
                            return True
                elif game.state == GameState.CONFIRM_NEW_GAME:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        # Confirmar: apagar autosave e ir para novo jogo
                        try:
                            game._clear_autosave()
                        except Exception:
                            pass
                        game.current_level = 1
                        game.score = 0
                        game.platforms_jumped.clear()
                        game.birds_dodged.clear()
                        game.lives = game.max_lives
                        game.player_name = ""
                        game.state = GameState.SELECT_DIFFICULTY
                    elif event.key == pygame.K_ESCAPE:
                        game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.CONFIRM_EXIT_TO_MENU:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        # Confirmar: voltar ao menu principal
                        game.state = GameState.MAIN_MENU
                        # Não salva progresso parcial da fase atual
                    elif event.key == pygame.K_ESCAPE:
                        game.state = GameState.PAUSED
                        return True
                elif game.state == GameState.CREDITS:
                    if (
                        game.credits_type == "menu"
                        and (
                            event.key == pygame.K_ESCAPE
                            or event.key == pygame.K_RETURN
                        )
                    ):
                        game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.RECORDS:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        if game.previous_state_before_records:
                            game.state = game.previous_state_before_records
                            game.previous_state_before_records = None
                        else:
                            game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.GAME_OVER:
                    if event.key == pygame.K_UP:
                        game.game_over_selected = (
                            (game.game_over_selected - 1)
                            % len(game.game_over_options)
                        )
                    elif event.key == pygame.K_DOWN:
                        game.game_over_selected = (
                            (game.game_over_selected + 1)
                            % len(game.game_over_options)
                        )
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if game.game_over_selected == 0:
                            if (
                                env.get("environment") == "development"
                                and "initial-stage" in env
                            ):
                                try:
                                    game.current_level = int(
                                        env["initial-stage"]
                                    )
                                    if (
                                        game.current_level < 1
                                        or game.current_level > 50
                                    ):
                                        game.current_level = 1
                                except (ValueError, TypeError):
                                    game.current_level = 1
                            else:
                                game.current_level = 1
                            game.score = 0
                            game.platforms_jumped.clear()
                            game.birds_dodged.clear()
                            game.lives = game.max_lives
                            game.player_name = ""
                            game.game_over_selected = 0
                            game.state = GameState.PLAYING
                            Level.init_level(game)
                            game.music.play_level_music(
                                game,
                                game.current_level,
                            )
                        elif game.game_over_selected == 1:
                            game.previous_state_before_records = (
                                GameState.GAME_OVER
                            )
                            game.state = GameState.RECORDS
                        elif game.game_over_selected == 2:
                            return False
                if game.state == GameState.ENTER_NAME:
                    if event.key == pygame.K_RETURN:
                        if game.player_name.strip():
                            game.ranking_manager.add_score(
                                game.player_name.strip(), game.score
                            )
                            game.previous_state_before_ranking = (
                                GameState.GAME_OVER
                            )
                            game.state = GameState.SHOW_RANKING
                    elif event.key == pygame.K_BACKSPACE:
                        game.player_name = game.player_name[:-1]
                    else:
                        if (
                            len(game.player_name) < 25
                            and event.unicode.isprintable()
                        ):
                            game.player_name += event.unicode
                elif event.key == pygame.K_r and (
                    game.state == GameState.VICTORY
                    or game.state == GameState.SHOW_RANKING
                ):
                    game.current_level = 1
                    game.score = 0
                    game.platforms_jumped.clear()
                    game.birds_dodged.clear()
                    game.lives = game.max_lives
                    game.player_name = ""
                    game.state = GameState.PLAYING
                    Level.init_level(game)
                    game.music.play_level_music(game, game.current_level)
                elif (
                    event.key == pygame.K_ESCAPE
                    and game.state == GameState.SHOW_RANKING
                ):
                    if game.previous_state_before_ranking:
                        game.state = game.previous_state_before_ranking
                        game.previous_state_before_ranking = None
                    else:
                        game.state = GameState.GAME_OVER
                    Level.init_level(game)
                    return True
                elif event.key == pygame.K_ESCAPE:
                    if game.state == GameState.CREDITS:
                        if getattr(game, "credits_type", None) == "menu":
                            game.state = GameState.MAIN_MENU
                        else:
                            pass
                    elif game.state == GameState.RECORDS:
                        if getattr(
                            game,
                            "previous_state_before_records",
                            None,
                        ):
                            game.state = game.previous_state_before_records
                            game.previous_state_before_records = None
                        else:
                            game.state = GameState.MAIN_MENU
                    elif game.state == GameState.SHOW_RANKING:
                        if getattr(
                            game,
                            "previous_state_before_ranking",
                            None,
                        ):
                            game.state = game.previous_state_before_ranking
                            game.previous_state_before_ranking = None
                        else:
                            game.state = GameState.MAIN_MENU
                    elif game.state == GameState.SELECT_DIFFICULTY:
                        game.state = GameState.MAIN_MENU
                    elif game.state == GameState.TITLE_SCREEN:
                        game.state = GameState.MAIN_MENU
                        if not getattr(game, "music_started", False):
                            try:
                                game.music.play_menu_music(game)
                                game.music_started = True
                            except Exception:
                                pass
                    elif game.state == GameState.OPENING_VIDEO:
                        return True
                    # Não fechar durante OPENING_VIDEO; ESC não faz nada especial
                    else:
                        # Em qualquer outro estado, ESC não encerra o jogo
                        # apenas retorna ao menu principal
                        game.state = GameState.MAIN_MENU
                    return True

            elif event.type == pygame.JOYBUTTONDOWN:
                # Mapear botões p/ cheat tokens se joystick presente
                if getattr(game, "joystick_connected", False):
                    if event.button == 1:
                        game._process_cheat_token("B")
                    elif event.button == 0:
                        game._process_cheat_token("A")
                if game.state == GameState.SPLASH:
                    if env.get("environment", "production") == "development":
                        game.state = GameState.TITLE_SCREEN
                elif game.state == GameState.TITLE_SCREEN:
                    game.state = GameState.OPENING_VIDEO
                    if game.video_player.load_video("videos/opening.mp4"):
                        game.video_player.start_playback()
                    else:
                        game.state = GameState.MAIN_MENU
                        if not game.music_started:
                            game.music.play_menu_music(game)
                            game.music_started = True
                elif game.state == GameState.OPENING_VIDEO:
                    pass
                elif game.state == GameState.MAIN_MENU:
                    if event.button == 0 or event.button in [6, 7, 8, 9]:
                        game.handle_menu_selection()
                elif game.state == GameState.PLAYING and event.button == getattr(game, "joystick_controls", {}).get("pause", 7):
                    # Botão Start/Options pausa
                    game.state = GameState.PAUSED
                    game.pause_selected = 0
                elif game.state == GameState.PAUSED:
                    if event.button == 0:
                        sel = game.pause_menu_options[game.pause_selected]
                        if sel == "Continuar":
                            game.state = GameState.PLAYING
                        elif sel == "Botões/Teclas":
                            game.options_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_CONTROLS
                        elif sel == "Áudio":
                            game.audio_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_AUDIO
                        elif sel == "Vídeo":
                            game.video_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_VIDEO
                        elif sel == "Acessibilidade":
                            game.access_selected = 0
                            game.previous_state_before_options = GameState.PAUSED
                            game.state = GameState.OPTIONS_ACCESSIBILITY
                        elif sel == "Sair":
                            game.confirm_dialog_type = "exit_to_menu"
                            game.confirm_selected = 0
                            game.state = GameState.CONFIRM_EXIT_TO_MENU
                    elif event.button == 1:
                        game.state = GameState.PLAYING
                elif game.state == GameState.OPTIONS_MENU:
                    if event.button == 0:
                        if game.options_selected == 0:
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_CONTROLS
                        elif game.options_selected == 1:
                            game.audio_selected = 0
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_AUDIO
                        elif game.options_selected == 2:
                            game.video_selected = 0
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_VIDEO
                        elif game.options_selected == 3:
                            game.access_selected = 0
                            game.previous_state_before_options = GameState.OPTIONS_MENU
                            game.state = GameState.OPTIONS_ACCESSIBILITY
                        elif game.options_selected == 4:
                            game.state = GameState.MAIN_MENU
                    elif event.button == 1:
                        game.state = GameState.MAIN_MENU
                elif game.state == GameState.OPTIONS_AUDIO:
                    if event.button == 1:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                elif game.state == GameState.OPTIONS_VIDEO:
                    if event.button == 0:
                        if game.video_selected == 1:
                            try:
                                game.env_config["fullscreen"] = not game.env_config.get("fullscreen", False)
                                from internal.engine.screen import Screen as _Screen
                                _Screen.init(game)
                            except Exception:
                                pass
                            try:
                                game._save_settings()
                            except Exception:
                                pass
                        elif game.video_selected == 2:
                            try:
                                game.visual_mode = "normal" if getattr(game, "visual_mode", "normal") == "8bit" else "8bit"
                                game._save_settings()
                            except Exception:
                                pass
                    elif event.button == 1:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                elif game.state == GameState.OPTIONS_CONTROLS:
                    if game.controls_editing:
                        label, action = game.controls_actions[game.controls_selected]
                        try:
                            game.joystick_controls[action] = int(event.button)
                            game._save_settings()
                        except Exception:
                            pass
                        game.controls_editing = False
                    elif event.button == 0:
                        game.controls_editing = True
                    elif event.button == 1:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                elif game.state == GameState.OPTIONS_ACCESSIBILITY:
                    if event.button == 1:
                        if game.previous_state_before_options:
                            game.state = game.previous_state_before_options
                            game.previous_state_before_options = None
                        else:
                            game.state = GameState.MAIN_MENU
                elif game.state == GameState.CONFIRM_NEW_GAME:
                    if event.button == 0:
                        try:
                            game._clear_autosave()
                        except Exception:
                            pass
                        game.current_level = 1
                        game.score = 0
                        game.platforms_jumped.clear()
                        game.birds_dodged.clear()
                        game.lives = game.max_lives
                        game.player_name = ""
                        game.state = GameState.SELECT_DIFFICULTY
                    elif event.button == 1:
                        game.state = GameState.MAIN_MENU
                elif game.state == GameState.CONFIRM_EXIT_TO_MENU:
                    if event.button == 0:
                        game.state = GameState.MAIN_MENU
                    elif event.button == 1:
                        game.state = GameState.PAUSED
                elif game.state == GameState.SELECT_DIFFICULTY:
                    if event.button == 0 or event.button in [6, 7, 8, 9]:
                        if game.difficulty_selected == 0:
                            game.difficulty = Difficulty.EASY
                        elif game.difficulty_selected == 2:
                            game.difficulty = Difficulty.HARD
                        else:
                            game.difficulty = Difficulty.NORMAL
                        (
                            game.extra_life_milestones,
                            game.extra_life_increment_after_milestones,
                        ) = game.get_extra_life_milestones_and_increment()
                        game.next_extra_life_score = (
                            game.extra_life_milestones[0]
                        )
                        game.extra_lives_earned = 0
                        if (
                            env.get("environment") == "development"
                            and "initial-stage" in env
                        ):
                            try:
                                game.current_level = int(env["initial-stage"])
                                if (
                                    game.current_level < 1
                                    or game.current_level > 50
                                ):
                                    game.current_level = 1
                            except (ValueError, TypeError):
                                game.current_level = 1
                        else:
                            game.current_level = 1
                        game.score = 0
                        game.platforms_jumped.clear()
                        game.birds_dodged.clear()
                        game.player_name = ""
                        game.max_lives = game.get_initial_lives()
                        game.lives = game.max_lives
                        if hasattr(game, "collected_extra_life_levels"):
                            game.collected_extra_life_levels.clear()
                        game.state = GameState.PLAYING
                        Level.init_level(game)
                        game.music.play_level_music(game, game.current_level)
                    elif event.button == 1:
                        game.state = GameState.MAIN_MENU
                elif game.state == GameState.FIM_SCREEN:
                    game.state = GameState.CREDITS
                    game.credits_type = "ending"
                    game.music.play_music("credits")
                elif game.state == GameState.CREDITS:
                    if game.credits_type == "menu" and (
                        event.button == 1 or event.button in [6, 7, 8, 9]
                    ):
                        game.state = GameState.MAIN_MENU
                        return True
                elif game.state == GameState.RECORDS:
                    if event.button == 1 or event.button in [6, 7, 8, 9]:
                        if game.previous_state_before_records:
                            game.state = game.previous_state_before_records
                            game.previous_state_before_records = None
                        else:
                            game.state = GameState.MAIN_MENU
                elif game.state == GameState.SHOW_RANKING:
                    if event.button == 1 or event.button in [6, 7, 8, 9]:
                        if getattr(
                            game,
                            "previous_state_before_ranking",
                            None,
                        ):
                            game.state = game.previous_state_before_ranking
                            game.previous_state_before_ranking = None
                        else:
                            game.state = GameState.MAIN_MENU
                elif game.state == GameState.GAME_OVER:
                    if event.button == 0 or event.button in [6, 7, 8, 9]:
                        if game.game_over_selected == 0:
                            if (
                                env.get("environment") == "development"
                                and "initial-stage" in env
                            ):
                                try:
                                    game.current_level = int(
                                        env["initial-stage"]
                                    )
                                    if (
                                        game.current_level < 1
                                        or game.current_level > 50
                                    ):
                                        game.current_level = 1
                                except (ValueError, TypeError):
                                    game.current_level = 1
                            else:
                                game.current_level = 1
                            game.score = 0
                            game.platforms_jumped.clear()
                            game.birds_dodged.clear()
                            game.lives = game.max_lives
                            game.player_name = ""
                            game.game_over_selected = 0
                            if hasattr(game, "collected_extra_life_levels"):
                                game.collected_extra_life_levels.clear()
                            game.state = GameState.PLAYING
                            Level.init_level(game)
                            game.music.play_level_music(
                                game,
                                game.current_level,
                            )
                        elif game.game_over_selected == 1:
                            game.previous_state_before_records = (
                                GameState.GAME_OVER
                            )
                            game.state = GameState.RECORDS
                        elif game.game_over_selected == 2:
                            return False
                elif event.button == 0:
                    keys = pygame.key.get_pressed()
                    keys = list(keys)
                    keys[pygame.K_SPACE] = True
                    keys = tuple(keys)
                elif event.button == 1:
                    keys = pygame.key.get_pressed()
                    keys = list(keys)
                    keys[pygame.K_SPACE] = True
                    keys = tuple(keys)
                elif event.button in [6, 7, 8, 9]:
                    if game.state == GameState.ENTER_NAME:
                        if game.player_name.strip():
                            game.ranking_manager.add_score(
                                game.player_name.strip(), game.score
                            )
                            game.previous_state_before_ranking = (
                                GameState.GAME_OVER
                            )
                            game.state = GameState.SHOW_RANKING
                    elif game.state in (
                        GameState.GAME_OVER,
                        GameState.VICTORY,
                        GameState.SHOW_RANKING,
                    ):
                        game.current_level = 1
                        game.score = 0
                        game.platforms_jumped.clear()
                        game.birds_dodged.clear()
                        game.lives = game.max_lives
                        game.player_name = ""
                        if hasattr(game, "collected_extra_life_levels"):
                            game.collected_extra_life_levels.clear()
                        game.state = GameState.PLAYING
                        Level.init_level(game)
                elif (
                    event.button == 1
                    and game.state == GameState.SHOW_RANKING
                ):
                    if game.previous_state_before_ranking:
                        game.state = game.previous_state_before_ranking
                        game.previous_state_before_ranking = None
                    else:
                        game.state = GameState.GAME_OVER

        if getattr(game, "joystick_connected", False) and getattr(game, "joystick", None):
            analog_vertical = 0
            analog_horizontal = 0
            if game.joystick.get_numaxes() >= 2:
                analog_vertical = game.joystick.get_axis(1)
                if abs(analog_vertical) < 0.1:
                    analog_vertical = 0
            if game.joystick.get_numaxes() >= 1:
                analog_horizontal = game.joystick.get_axis(0)
                if abs(analog_horizontal) < 0.1:
                    analog_horizontal = 0
            dpad_vertical = 0
            dpad_horizontal = 0
            if game.joystick.get_numaxes() > 7:
                dpad_vertical = game.joystick.get_axis(7)
            if game.joystick.get_numaxes() > 6:
                dpad_horizontal = game.joystick.get_axis(6)
            analog_up = (
                analog_vertical < -0.5
                and game.prev_analog_vertical >= -0.5
            )
            analog_down = (
                analog_vertical > 0.5
                and game.prev_analog_vertical <= 0.5
            )
            dpad_up = (
                dpad_vertical < -0.5
                and game.prev_dpad_vertical >= -0.5
            )
            dpad_down = (
                dpad_vertical > 0.5
                and game.prev_dpad_vertical <= 0.5
            )
            if analog_up or dpad_up:
                game._process_cheat_token("UP")
                if game.state == GameState.MAIN_MENU:
                    game.menu_selected = (game.menu_selected - 1) % len(
                        game.menu_options
                    )
                elif game.state == GameState.SELECT_DIFFICULTY:
                    game.difficulty_selected = (
                        (game.difficulty_selected - 1)
                        % len(game.difficulty_options)
                    )
                elif game.state == GameState.PAUSED:
                    game.pause_selected = (game.pause_selected - 1) % len(
                        game.pause_menu_options
                    )
                elif game.state == GameState.OPTIONS_MENU:
                    game.options_selected = (game.options_selected - 1) % 5
                elif game.state == GameState.OPTIONS_AUDIO:
                    game.audio_selected = (game.audio_selected - 1) % 2
                elif game.state == GameState.OPTIONS_VIDEO:
                    game.video_selected = (game.video_selected - 1) % 3
                elif game.state == GameState.OPTIONS_ACCESSIBILITY:
                    game.access_selected = (getattr(game, "access_selected", 0) - 1) % 2
                elif game.state == GameState.OPTIONS_CONTROLS and not getattr(game, "controls_editing", False):
                    game.controls_selected = (
                        (game.controls_selected - 1) % len(game.controls_actions)
                    )
                elif game.state == GameState.GAME_OVER:
                    game.game_over_selected = (
                        (game.game_over_selected - 1)
                        % len(game.game_over_options)
                    )
            elif analog_down or dpad_down:
                game._process_cheat_token("DOWN")
                if game.state == GameState.MAIN_MENU:
                    game.menu_selected = (game.menu_selected + 1) % len(
                        game.menu_options
                    )
                elif game.state == GameState.SELECT_DIFFICULTY:
                    game.difficulty_selected = (
                        (game.difficulty_selected + 1)
                        % len(game.difficulty_options)
                    )
                elif game.state == GameState.PAUSED:
                    game.pause_selected = (game.pause_selected + 1) % len(
                        game.pause_menu_options
                    )
                elif game.state == GameState.OPTIONS_MENU:
                    game.options_selected = (game.options_selected + 1) % 5
                elif game.state == GameState.OPTIONS_AUDIO:
                    game.audio_selected = (game.audio_selected + 1) % 2
                elif game.state == GameState.OPTIONS_VIDEO:
                    game.video_selected = (game.video_selected + 1) % 3
                elif game.state == GameState.OPTIONS_ACCESSIBILITY:
                    game.access_selected = (getattr(game, "access_selected", 0) + 1) % 2
                elif game.state == GameState.OPTIONS_CONTROLS and not getattr(game, "controls_editing", False):
                    game.controls_selected = (
                        (game.controls_selected + 1) % len(game.controls_actions)
                    )
                elif game.state == GameState.GAME_OVER:
                    game.game_over_selected = (
                        (game.game_over_selected + 1)
                        % len(game.game_over_options)
                    )
            analog_left = (
                analog_horizontal < -0.5
                and game.prev_analog_horizontal >= -0.5
            )
            analog_right = (
                analog_horizontal > 0.5
                and game.prev_analog_horizontal <= 0.5
            )
            dpad_left = (
                dpad_horizontal < -0.5
                and game.prev_dpad_horizontal >= -0.5
            )
            dpad_right = (
                dpad_horizontal > 0.5
                and game.prev_dpad_horizontal <= 0.5
            )
            if analog_left or dpad_left:
                game._process_cheat_token("LEFT")
                if game.state == GameState.OPTIONS_AUDIO:
                    if game.audio_selected == 0:
                        game.music_volume = max(0.0, game.music_volume - 0.1)
                        try:
                            import pygame as _pg
                            _pg.mixer.music.set_volume(game.music_volume)
                            game._save_settings()
                        except Exception:
                            pass
                    else:
                        game.sound_effects.sound_volume = max(0.0, game.sound_effects.sound_volume - 0.1)
                        try:
                            for s in game.sound_effects.sound_effects.values():
                                s.set_volume(game.sound_effects.sound_volume)
                            game._save_settings()
                        except Exception:
                            pass
                elif game.state == GameState.OPTIONS_VIDEO:
                    if game.video_selected == 1:
                        try:
                            game.env_config["fullscreen"] = not game.env_config.get("fullscreen", False)
                            from internal.engine.screen import Screen as _Screen
                            _Screen.init(game)
                            game._save_settings()
                        except Exception:
                            pass
                    elif game.video_selected == 2:
                        try:
                            game.visual_mode = "normal" if getattr(game, "visual_mode", "normal") == "8bit" else "8bit"
                            game._save_settings()
                        except Exception:
                            pass
                elif game.state == GameState.OPTIONS_ACCESSIBILITY:
                    if getattr(game, "access_selected", 0) == 0:
                        try:
                            modes = ["none", "deuteranopia", "protanopia", "tritanopia"]
                            idx = modes.index(getattr(game, "colorblind_mode", "none"))
                        except Exception:
                            idx = 0
                        game.colorblind_mode = modes[(idx - 1) % len(modes)]
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    else:
                        game.vibration_enabled = not getattr(game, "vibration_enabled", False)
                        try:
                            game._save_settings()
                        except Exception:
                            pass
            if analog_right or dpad_right:
                game._process_cheat_token("RIGHT")
                if game.state == GameState.OPTIONS_AUDIO:
                    if game.audio_selected == 0:
                        game.music_volume = min(1.0, game.music_volume + 0.1)
                        try:
                            import pygame as _pg
                            _pg.mixer.music.set_volume(game.music_volume)
                            game._save_settings()
                        except Exception:
                            pass
                    else:
                        game.sound_effects.sound_volume = min(1.0, game.sound_effects.sound_volume + 0.1)
                        try:
                            for s in game.sound_effects.sound_effects.values():
                                s.set_volume(game.sound_effects.sound_volume)
                            game._save_settings()
                        except Exception:
                            pass
                elif game.state == GameState.OPTIONS_VIDEO:
                    if game.video_selected == 1:
                        try:
                            game.env_config["fullscreen"] = not game.env_config.get("fullscreen", False)
                            from internal.engine.screen import Screen as _Screen
                            _Screen.init(game)
                            game._save_settings()
                        except Exception:
                            pass
                    elif game.video_selected == 2:
                        try:
                            game.visual_mode = "normal" if getattr(game, "visual_mode", "normal") == "8bit" else "8bit"
                            game._save_settings()
                        except Exception:
                            pass
                elif game.state == GameState.OPTIONS_ACCESSIBILITY:
                    if getattr(game, "access_selected", 0) == 0:
                        try:
                            modes = ["none", "deuteranopia", "protanopia", "tritanopia"]
                            idx = modes.index(getattr(game, "colorblind_mode", "none"))
                        except Exception:
                            idx = 0
                        game.colorblind_mode = modes[(idx + 1) % len(modes)]
                        try:
                            game._save_settings()
                        except Exception:
                            pass
                    else:
                        game.vibration_enabled = not getattr(game, "vibration_enabled", False)
                        try:
                            game._save_settings()
                        except Exception:
                            pass
            game.prev_analog_vertical = analog_vertical
            game.prev_analog_horizontal = analog_horizontal
            game.prev_dpad_vertical = dpad_vertical
            game.prev_dpad_horizontal = dpad_horizontal

        return True
