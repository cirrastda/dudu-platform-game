import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Airplane:
    _id_counter = 0  # Contador de ID para aviões

    def __init__(self, x, y, airplane_images=None):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = 4  # Velocidade mais rápida que pássaros (3) e morcegos (2)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.direction = -1  # -1 para esquerda, 1 para direita

        # Atribuir ID único
        Airplane._id_counter += 1
        self.id = Airplane._id_counter

        # Animação
        self.airplane_images = airplane_images
        self.animation_frame = 0
        self.animation_speed = 6  # Velocidade de animação um pouco mais lenta

    def update(self, camera_x=0):
        # Mover avião na direção atual
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Atualizar animação
        self.animation_frame += 1

        # Remover se saiu da tela (com margem) - relativo à câmera
        if self.x < camera_x - 300 or self.x > camera_x + 1400:
            return False
        return True

    def draw(self, screen):
        if self.airplane_images and len(self.airplane_images) > 0:
            # Usar animação com as imagens carregadas
            current_image_index = (self.animation_frame // self.animation_speed) % len(
                self.airplane_images
            )
            current_image = self.airplane_images[current_image_index]
            if current_image:
                # Espelhar imagem se necessário
                if self.direction == 1:
                    flipped_image = pygame.transform.flip(current_image, True, False)
                    screen.blit(flipped_image, (self.x, self.y))
                else:
                    screen.blit(current_image, (self.x, self.y))
                return

        # Fallback para o desenho original se as imagens não carregaram
        pygame.draw.rect(screen, GRAY, self.rect)  # Cinza para avião
        # Adicionar detalhes simples (asas)
        wing_y = self.y + 10
        pygame.draw.polygon(
            screen,
            DARK_GRAY,
            [(self.x + 5, wing_y), (self.x + 15, wing_y - 8), (self.x + 25, wing_y + 5)],
        )
        pygame.draw.polygon(
            screen,
            DARK_GRAY,
            [
                (self.x + self.width - 25, wing_y + 5),
                (self.x + self.width - 15, wing_y - 8),
                (self.x + self.width - 5, wing_y),
            ],
        )