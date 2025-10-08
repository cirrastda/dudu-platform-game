import pygame
from internal.utils.constants import *


class Bullet:
    def __init__(self, x, y, direction=1, image=None):
        self.x = x
        self.y = y
        self.width = 15 if image else 10
        self.height = 8 if image else 5
        self.speed = 8
        self.direction = direction  # 1 para direita, -1 para esquerda
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = image

    def update(self):
        """Atualizar posição do tiro"""
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Manter tiro ativo (remoção será feita no método update do Player)
        return True

    def draw(self, screen):
        """Desenhar o tiro"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Fallback: desenhar retângulo amarelo
            pygame.draw.rect(screen, YELLOW, self.rect)
