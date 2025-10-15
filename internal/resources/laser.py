import pygame
from internal.utils.constants import *


class Laser:
    _id_counter = 0

    def __init__(self, x, y, direction=-1):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 3
        self.speed = 5  # Velocidade do laser
        self.direction = direction  # -1 para esquerda, 1 para direita
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        Laser._id_counter += 1
        self.id = Laser._id_counter

    def update(self, camera_x=0):
        # Movimento horizontal do laser
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Remover apenas se sair MUITO longe da área visível para evitar desaparecimento prematuro
        # Aumentando a margem para 800 pixels para garantir que lasers não desapareçam enquanto podem colidir
        if self.x < camera_x - 800 or self.x > camera_x + WIDTH + 800:
            return False
        return True

    def draw(self, screen):
        # Desenhar como uma linha/retângulo vermelho
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return self.rect
