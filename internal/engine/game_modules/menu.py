from internal.engine.state import GameState
from internal.engine.level.level import Level


class Menu:
    def __init__(self, game):
        self.g = game
        # Módulos injetados pelo delegador do Game para permitir monkeypatch em testes
        self._sys = None
        self._pygame = None

    def set_runtime_modules(self, sys_mod, pygame_mod):
        self._sys = sys_mod
        self._pygame = pygame_mod

    def handle_menu_selection(self):
        """Processar seleção do menu principal"""
        g = self.g
        selected_option = g.menu_options[g.menu_selected]

        if selected_option == "Continuar":
            if getattr(g, "_autosave_data", None):
                data = g._autosave_data
                try:
                    g.current_level = int(data.get("level", 1))
                except Exception:
                    g.current_level = 1
                try:
                    g.score = int(data.get("score", 0))
                except Exception:
                    g.score = 0
                try:
                    g.lives = int(data.get("lives_at_stage_start", g.get_initial_lives()))
                except Exception:
                    g.lives = g.get_initial_lives()
                g.platforms_jumped.clear()
                g.birds_dodged.clear()
                g.player_name = ""
                g.state = GameState.PLAYING
                Level.init_level(g)
                g.music.play_level_music(g, g.current_level)
            else:
                # Sem autosave, cair para novo jogo
                g.menu_selected = 1 if len(g.menu_options) > 1 else 0
        elif selected_option == "Novo Jogo":
            # Se existir autosave, pedir confirmação
            if getattr(g, "_autosave_data", None):
                g.confirm_dialog_type = "new_game"
                g.confirm_selected = 0
                g.state = GameState.CONFIRM_NEW_GAME
            else:
                # Iniciar novo jogo sempre no nível 1
                g.current_level = 1
                g.score = 0
                g.platforms_jumped.clear()
                g.birds_dodged.clear()
                g.lives = g.max_lives
                g.player_name = ""
                # Ir para seleção de dificuldade
                g.state = GameState.SELECT_DIFFICULTY
        elif selected_option == "Iniciar":
            g.current_level = 1
            g.score = 0
            g.platforms_jumped.clear()
            g.birds_dodged.clear()
            g.lives = g.max_lives
            g.player_name = ""
            g.state = GameState.SELECT_DIFFICULTY
        elif selected_option == "Recordes":
            g.state = GameState.RECORDS
        elif selected_option == "Créditos":
            g.state = GameState.CREDITS
            g.credits_type = "menu"
        elif selected_option == "Configurações":
            g.options_selected = 0
            g.pause_selected = None
            g.state = GameState.OPTIONS_MENU
        elif selected_option == "Sair":
            # Encerrar chamando pygame.quit e sys.exit (testes podem patchar sys.exit via módulo game)
            if self._pygame is not None:
                try:
                    self._pygame.quit()
                except Exception:
                    pass
            if self._sys is not None:
                try:
                    self._sys.exit()
                except SystemExit:
                    # Propagar para quem estiver esperando a exceção
                    raise