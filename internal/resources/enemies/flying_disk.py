import math
import pygame
from internal.utils.constants import *


class FlyingDisk:
    _id_counter = 0

    def __init__(self, x, y, disk_images=None, amplitude=40, frequency=0.08):
        # Posição inicial
        self.x = x
        self.y = y
        # Guardar referência de y base para movimento senoidal
        self.base_y = y
        # Tamanho aproximado
        self.width = 40
        self.height = 40
        # Velocidade horizontal (similar ao avião, um pouco menor)
        self.speed = 3
        self.direction = -1  # Move da direita para esquerda
        # Retângulo de colisão
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Atribuir ID único
        FlyingDisk._id_counter += 1
        self.id = FlyingDisk._id_counter

        # Animação
        self.disk_images = disk_images or []
        self.animation_frame = 0
        self.animation_speed = 8

        # Movimento senoidal
        self.amplitude = amplitude
        self.frequency = frequency

    def update(self, camera_x=0):
        # Atualizar posição horizontal
        self.x += self.speed * self.direction

        # Atualizar animação/movimento
        self.animation_frame += 1

        # Movimento senoidal no eixo Y
        self.y = self.base_y + self.amplitude * math.sin(self.animation_frame * self.frequency)

        # Atualizar retângulo de colisão
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Remover se saiu da tela (com margem) - relativo à câmera
        if self.x < camera_x - 300 or self.x > camera_x + 1400:
            return False
        return True

    def draw(self, screen):
        if self.disk_images and len(self.disk_images) > 0:
            current_image_index = (self.animation_frame // self.animation_speed) % len(self.disk_images)
            current_image = self.disk_images[current_image_index]
            if current_image:
                # Disco não precisa espelhamento
                screen.blit(current_image, (self.x, self.y))
                return

        # Fallback simples caso imagens não carreguem
        pygame.draw.circle(screen, LIGHT_GRAY, (int(self.x + self.width/2), int(self.y + self.height/2)), self.width//2)