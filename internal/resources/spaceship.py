import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120  # Largura da nave
        self.height = 80  # Altura da nave
        self.abduction_height = 150  # Altura da área de abdução (raio de luz)
        
        # Rect da nave (parte superior)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Rect da área de abdução (parte inferior - raio de luz)
        self.abduction_rect = pygame.Rect(
            x + self.width // 4,  # Centralizar a área de abdução
            y + self.height,      # Começar logo abaixo da nave
            self.width // 2,      # Largura menor que a nave
            self.abduction_height # Altura da área de abdução
        )

        # Carregar imagem da nave
        try:
            spaceship_path = resource_path("imagens/elementos/nave.png")
            self.spaceship_image = pygame.image.load(spaceship_path)
            # Redimensionar para o tamanho desejado
            self.spaceship_image = pygame.transform.scale(
                self.spaceship_image, (self.width, self.height)
            )
        except pygame.error:
            self.spaceship_image = None

    def draw(self, screen):
        # Desenhar área de abdução (raio de luz) - semi-transparente
        abduction_surface = pygame.Surface(
            (self.abduction_rect.width, self.abduction_rect.height), 
            pygame.SRCALPHA
        )
        # Cor amarela semi-transparente para o raio de abdução
        abduction_surface.fill((255, 255, 0, 60))  # Amarelo com alpha 60
        screen.blit(abduction_surface, (self.abduction_rect.x, self.abduction_rect.y))
        
        # Desenhar nave espacial
        if self.spaceship_image:
            screen.blit(self.spaceship_image, (self.x, self.y))
        else:
            # Fallback: desenhar nave como retângulo cinza
            pygame.draw.rect(screen, GRAY, self.rect)
            # Desenhar alguns detalhes simples
            pygame.draw.circle(screen, WHITE, 
                             (self.x + self.width // 2, self.y + self.height // 2), 
                             10)