# import platform
import pygame
from internal.utils.constants import WIDTH, HEIGHT


class Screen:
    def init(game):
        # Detectar se está rodando em PC/Mac para usar fullscreen
        # system = platform.system().lower()
        # is_desktop = system in ["windows", "linux", "darwin"]  # darwin = macOS

        # if is_desktop:
        if (not game.is_development()) or (Screen.is_fullscreen(game)):
            # Usar fullscreen com resolução do jogo
            game.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            # Usar modo janela
            game.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def is_fullscreen(game):
        env = game.env_config
        return env.get("fullscreen", False)
