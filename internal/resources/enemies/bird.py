import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Bird:
    _id_counter = 0  # Contador de ID para pássaros

    def __init__(self, x, y, bird_images=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 3
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # Atribuir ID único
        Bird._id_counter += 1
        self.id = Bird._id_counter
        # Animação
        self.bird_images = bird_images  # Tupla com (bird_img1, bird_img2)
        self.animation_frame = 0
        self.animation_speed = 10  # Frames para trocar de imagem
        # Estado de morte
        self.is_dead = False
        self.death_timer = 0
        self.fall_speed = 3

    def update(self):
        if not self.is_dead:
            # Mover pássaro da direita para a esquerda
            self.x -= self.speed
            self.rect.x = self.x
            # Atualizar animação
            self.animation_frame += 1
            # Retornar True se ainda está na tela, False se saiu
            return self.x + self.width > 0
        else:
            # Animação de morte: queda vertical
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

    def draw(self, screen):
        if self.bird_images and self.bird_images[0] and self.bird_images[1]:
            if not self.is_dead:
                # Usar animação com as imagens carregadas
                current_image_index = (self.animation_frame // self.animation_speed) % 2
                current_image = self.bird_images[current_image_index]
                screen.blit(current_image, (self.x, self.y))
            else:
                # Mostrar sprite rotacionado para indicar queda
                current_image = self.bird_images[0]
                rotated = pygame.transform.rotate(current_image, 90)
                screen.blit(rotated, (self.x, self.y))
        else:
            # Fallback para o desenho original se as imagens não carregaram
            color = (150, 75, 0) if not self.is_dead else (200, 50, 50)
            pygame.draw.ellipse(screen, color, self.rect)
            # Adicionar detalhes simples (asas)
            wing_y = self.y + 5
            if not self.is_dead:
                pygame.draw.ellipse(screen, BLACK, (self.x + 5, wing_y, 8, 4))
                pygame.draw.ellipse(screen, BLACK, (self.x + 17, wing_y, 8, 4))
            # Bico
            pygame.draw.polygon(
                screen,
                YELLOW if not self.is_dead else (255, 200, 100),
                [
                    (self.x, self.y + 8),
                    (self.x - 5, self.y + 10),
                    (self.x, self.y + 12),
                ],
            )
