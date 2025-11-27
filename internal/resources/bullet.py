import pygame
from internal.utils.constants import *


class Bullet:
    def __init__(self, x, y, direction=1, image=None):
        self.x = x
        self.y = y
        self.width = 15 if image else 10
        self.height = 8 if image else 5
        self.speed = 8
        self.direction = direction  # 1 para direita, -1 para esquerda
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = image
        self.is_super = False

    def update(self):
        """Atualizar posição do tiro"""
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Manter tiro ativo (remoção será feita no método update do Player)
        return True

    def draw(self, screen):
        """Desenhar o tiro"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, YELLOW, self.rect)
        if getattr(self, "is_super", False):
            try:
                glow_w = max(10, int(self.width * 1.2))
                glow_h = max(8, int(self.height * 1.5))
                overlay = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
                cx = glow_w // 2
                cy = glow_h // 2
                pygame.draw.circle(overlay, (0, 255, 255, 110), (cx, cy), max(3, int(glow_h * 0.3)))
                pygame.draw.circle(overlay, (135, 206, 235, 90), (cx, cy), max(5, int(glow_h * 0.45)))
                ox = - (glow_w - self.width) // 2
                oy = - (glow_h - self.height) // 2
                screen.blit(overlay, (int(self.x + ox), int(self.y + oy)))
            except Exception:
                pass
