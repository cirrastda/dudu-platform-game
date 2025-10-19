import pygame
from internal.utils.constants import *


class Fire:
    _id_counter = 0  # Contador de ID para foguinhos

    def __init__(self, x, y, fire_image=None):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 1.5  # Velocidade moderada
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.direction = -1  # -1 para esquerda (sempre se move para a esquerda)

        # Atribuir ID único
        Fire._id_counter += 1
        self.id = Fire._id_counter

        # Imagem do foguinho
        self.fire_image = fire_image

        # Animação simples (sem frames múltiplos)
        self.animation_frame = 0
        self.animation_speed = 8

    def update(self, camera_x=0):
        """Atualizar posição do foguinho"""
        # Mover para a esquerda
        self.x += self.direction * self.speed

        # Atualizar rect
        self.rect.x = self.x
        self.rect.y = self.y

        # Atualizar animação
        self.animation_frame += 1

        # Remover se saiu muito da tela (à esquerda da câmera)
        if self.x < camera_x - 200:
            return False

        return True

    def draw(self, screen):
        """Desenhar o foguinho"""
        if self.fire_image:
            screen.blit(self.fire_image, (self.x, self.y))
        else:
            # Fallback: desenhar como círculo laranja/vermelho
            pygame.draw.circle(
                screen,
                (255, 100, 0),
                (int(self.x + self.width / 2), int(self.y + self.height / 2)),
                self.width // 2,
            )
            # Adicionar efeito de fogo (círculo interno amarelo)
            pygame.draw.circle(
                screen,
                (255, 255, 0),
                (int(self.x + self.width / 2), int(self.y + self.height / 2)),
                self.width // 3,
            )
