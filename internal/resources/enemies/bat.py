import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Bat:
    _id_counter = 0  # Contador de ID para morcegos

    def __init__(self, x, y, bat_images=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 2  # Velocidade similar aos pássaros
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.direction = -1  # -1 para esquerda, 1 para direita

        # Atribuir ID único
        Bat._id_counter += 1
        self.id = Bat._id_counter

        # Animação
        self.bat_images = bat_images
        self.animation_frame = 0
        self.animation_speed = 8  # Velocidade de animação similar aos pássaros

    def update(self):
        # Mover morcego na direção atual
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Atualizar animação
        self.animation_frame += 1

        # Remover se saiu da tela (com margem)
        if self.x < -100 or self.x > 2000:
            return False
        return True

    def draw(self, screen):
        if self.bat_images and len(self.bat_images) > 0:
            # Usar animação com as imagens carregadas
            current_image_index = (self.animation_frame // self.animation_speed) % len(
                self.bat_images
            )
            current_image = self.bat_images[current_image_index]
            if current_image:
                # Espelhar imagem se necessário
                if self.direction == 1:
                    flipped_image = pygame.transform.flip(current_image, True, False)
                    screen.blit(flipped_image, (self.x, self.y))
                else:
                    screen.blit(current_image, (self.x, self.y))
                return

        # Fallback para o desenho original se as imagens não carregaram
        pygame.draw.ellipse(screen, DARK_GRAY, self.rect)  # Cinza escuro para morcego
        # Adicionar detalhes simples (asas)
        wing_y = self.y + 5
        pygame.draw.polygon(
            screen,
            BLACK,
            [(self.x, wing_y), (self.x + 10, wing_y - 5), (self.x + 15, wing_y + 10)],
        )
        pygame.draw.polygon(
            screen,
            BLACK,
            [
                (self.x + self.width - 15, wing_y + 10),
                (self.x + self.width - 10, wing_y - 5),
                (self.x + self.width, wing_y),
            ],
        )
