import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 250  # Largura da nave (aumentada)
        self.height = 200  # Altura da nave (aumentada proporcionalmente)
        self.abduction_height = 250  # Altura da área de abdução (raio de luz)
        
        # Rect da nave (parte superior)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Rect da área de abdução (sobrepondo a nave)
        self.abduction_rect = pygame.Rect(
            x,                    # Mesma posição x da nave
            y,                    # Mesma posição y da nave (sobrepondo)
            self.width,           # Mesma largura da nave
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
    
    def update_position(self, x, y):
        """Atualizar posição da nave e seus rects"""
        self.x = x
        self.y = y
        # Atualizar rect da nave
        self.rect.x = x
        self.rect.y = y
        # Atualizar rect da área de abdução
        self.abduction_rect.x = x
        self.abduction_rect.y = y

    def draw(self, screen):
        # Área de abdução invisível (sem coloração)
        # A área de overlap existe para detecção de colisão mas não é visível
        
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