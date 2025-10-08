import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.flag_width = 60
        self.flag_height = 40
        self.rect = pygame.Rect(x, y, self.width + self.flag_width, self.height)

        # Carregar imagem da bandeira
        try:
            flag_path = resource_path("imagens/elementos/bandeira.png")
            self.flag_image = pygame.image.load(flag_path)
            # Redimensionar para ocupar toda a área (mastro + bandeira)
            total_width = self.width + self.flag_width
            self.flag_image = pygame.transform.scale(
                self.flag_image, (total_width, self.height)
            )
        except pygame.error:
            self.flag_image = None

    def draw(self, screen):
        # Desenhar bandeira completa (imagem ou fallback)
        if self.flag_image:
            # A imagem substitui completamente mastro e bandeira
            screen.blit(self.flag_image, (self.x, self.y))
        else:
            # Fallback para desenho original completo
            # Desenhar mastro
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
            # Desenhar bandeira
            flag_rect = pygame.Rect(
                self.x + self.width, self.y, self.flag_width, self.flag_height
            )
            pygame.draw.rect(screen, RED, flag_rect)
            pygame.draw.polygon(
                screen,
                RED,
                [
                    (self.x + self.width + self.flag_width, self.y),
                    (
                        self.x + self.width + self.flag_width + 20,
                        self.y + self.flag_height // 2,
                    ),
                    (self.x + self.width + self.flag_width, self.y + self.flag_height),
                ],
            )
