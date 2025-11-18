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

        if selected_option == "Iniciar":
            # Iniciar novo jogo sempre no nível 1, ignorando seleção de debugger
            g.current_level = 1
            g.score = 0
            g.platforms_jumped.clear()
            g.birds_dodged.clear()
            g.lives = g.max_lives
            g.player_name = ""
            g.state = GameState.PLAYING
            Level.init_level(g)
            # Tocar música do nível atual
            g.music.play_level_music(g, g.current_level)
            # Ir para seleção de dificuldade antes de iniciar o jogo
            g.state = GameState.SELECT_DIFFICULTY
        elif selected_option == "Recordes":
            g.state = GameState.RECORDS
        elif selected_option == "Créditos":
            g.state = GameState.CREDITS
            g.credits_type = "menu"
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