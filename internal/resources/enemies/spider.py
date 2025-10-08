import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Spider:
    _id_counter = 0  # Contador de ID para aranhas

    def __init__(self, x, y, top_limit, bottom_limit, spider_images=None):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 25
        self.speed = 1.5  # Velocidade de movimento vertical
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.top_limit = top_limit  # Limite superior do movimento
        self.bottom_limit = (
            bottom_limit  # Limite inferior do movimento (máximo na linha da plataforma)
        )
        self.direction = 1  # 1 para baixo, -1 para cima
        self.web_start_y = top_limit  # Ponto inicial da teia

        # Atribuir ID único
        Spider._id_counter += 1
        self.id = Spider._id_counter

        # Animação
        self.spider_images = spider_images
        self.animation_frame = 0
        self.animation_speed = 12  # Velocidade de animação mais lenta que pássaros

    def update(self):
        # Mover aranha na direção atual
        self.y += self.speed * self.direction

        # Verificar limites e inverter direção
        if self.y <= self.top_limit:
            self.y = self.top_limit
            self.direction = 1  # Mudar para baixo
        elif self.y >= self.bottom_limit:
            self.y = self.bottom_limit
            self.direction = -1  # Mudar para cima

        self.rect.y = self.y

        # Atualizar animação
        self.animation_frame += 1

        return True  # Aranha sempre permanece ativa

    def draw(self, screen):
        # Desenhar a teia (linha branca do ponto inicial até a posição atual)
        pygame.draw.line(
            screen,
            WHITE,
            (self.x + self.width // 2, self.web_start_y),
            (self.x + self.width // 2, self.y),
            2,
        )

        if self.spider_images and len(self.spider_images) > 0:
            # Usar animação com as imagens carregadas
            current_image_index = (self.animation_frame // self.animation_speed) % len(
                self.spider_images
            )
            current_image = self.spider_images[current_image_index]
            if current_image:
                screen.blit(current_image, (self.x, self.y))
                return

        # Fallback para o desenho original se as imagens não carregaram
        pygame.draw.ellipse(screen, BLACK, self.rect)  # Preto para aranha
        # Adicionar detalhes simples (patas)
        leg_length = 8
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        # Patas da esquerda
        pygame.draw.line(
            screen,
            BLACK,
            (center_x - 5, center_y - 3),
            (center_x - leg_length, center_y - 8),
            2,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (center_x - 5, center_y),
            (center_x - leg_length, center_y),
            2,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (center_x - 5, center_y + 3),
            (center_x - leg_length, center_y + 8),
            2,
        )
        # Patas da direita
        pygame.draw.line(
            screen,
            BLACK,
            (center_x + 5, center_y - 3),
            (center_x + leg_length, center_y - 8),
            2,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (center_x + 5, center_y),
            (center_x + leg_length, center_y),
            2,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (center_x + 5, center_y + 3),
            (center_x + leg_length, center_y + 8),
            2,
        )
