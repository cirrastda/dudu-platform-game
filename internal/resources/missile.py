import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Missile:
    _id_counter = 0  # Contador de ID para mísseis

    def __init__(self, x, y, direction, missile_images=None):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 8
        self.speed = 4  # Velocidade do míssil
        self.direction = direction  # -1 para esquerda, 1 para direita
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Atribuir ID único
        Missile._id_counter += 1
        self.id = Missile._id_counter
        
        # Imagens
        self.missile_images = missile_images
        
        # Limites da tela para remoção automática
        self.screen_width = WIDTH

    def update(self, camera_x=0):
        """Atualiza a posição do míssil e retorna False se deve ser removido"""
        # Mover míssil na direção especificada
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Verificar se saiu da área visível (com margem) - relativo à câmera
        if self.x < camera_x - 300 or self.x > camera_x + WIDTH + 300:
            return False  # Míssil deve ser removido
            
        return True  # Míssil continua ativo

    def draw(self, screen):
        """Desenha o míssil na tela"""
        if self.missile_images:
            # Escolher imagem baseada na direção
            if self.direction == 1:  # Direita
                image = self.missile_images.get('right')
            else:  # Esquerda
                image = self.missile_images.get('left')
            
            if image:
                screen.blit(image, (self.x, self.y))
                return
        
        # Fallback: desenhar retângulo se imagens não estão disponíveis
        color = (255, 255, 0)  # Amarelo para míssil
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        """Retorna o retângulo de colisão do míssil"""
        return self.rect