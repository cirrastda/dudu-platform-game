import pygame
from internal.utils.constants import *


class Explosion:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.timer = 30  # Duração da explosão em frames (0.5 segundos a 60 FPS)
        self.image = image

    def update(self):
        """Atualizar explosão"""
        self.timer -= 1
        return self.timer > 0

    def draw(self, screen):
        """Desenhar explosão"""
        if self.timer > 0:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                # Fallback: desenhar círculo vermelho piscando
                if self.timer % 6 < 3:  # Piscar
                    pygame.draw.circle(
                        screen,
                        RED,
                        (self.x + self.width // 2, self.y + self.height // 2),
                        self.width // 2,
                    )
