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
        # Estado de morte
        self.is_dead = False
        self.death_timer = 0
        self.fall_speed = 3

    def update(self, camera_x=0):
        if not self.is_dead:
            # Mover morcego na direção atual
            self.x += self.speed * self.direction
            self.rect.x = self.x
            # Atualizar animação
            self.animation_frame += 1
            # Remover se saiu da tela (com margem) - relativo à câmera
            if self.x < camera_x - 300 or self.x > camera_x + 1400:
                return False
            return True
        else:
            # Animação de morte: queda
            self.y += self.fall_speed
            self.death_timer += 1
            self.rect.x = self.x
            self.rect.y = self.y
            # Remover após sair da tela ou após duração
            if self.y > HEIGHT + 100 or self.death_timer > 180:
                return False
            return True

    def die(self):
        self.is_dead = True
        self.death_timer = 0
        # Ao morrer, parar deslocamento horizontal
        self.speed = 0
        self.direction = 0

    def draw(self, screen):
        if self.bat_images and len(self.bat_images) > 0:
            if not self.is_dead:
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
            else:
                # Mostrar sprite rotacionado
                current_image = self.bat_images[0]
                rotated = pygame.transform.rotate(current_image, 90)
                screen.blit(rotated, (self.x, self.y))
                return

        # Fallback para o desenho original se as imagens não carregaram
        color = DARK_GRAY if not self.is_dead else (200, 50, 50)
        pygame.draw.ellipse(screen, color, self.rect)  # Cinza escuro para morcego
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
