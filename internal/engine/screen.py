import platform
import pygame
from internal.utils.constants import WIDTH, HEIGHT


class Screen:
    def init(game):
        # Detectar se está rodando em PC/Mac para usar fullscreen
        system = platform.system().lower()
        is_desktop = system in ["windows", "linux", "darwin"]  # darwin = macOS
        is_fullscreen = is_desktop and (game.env_config.get("environment") == "production")
            

        if is_fullscreen:
            # Usar fullscreen em PC/Mac
            game.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            # Usar modo janela em outras plataformas (como Android)
            game.screen = pygame.display.set_mode((WIDTH, HEIGHT))
