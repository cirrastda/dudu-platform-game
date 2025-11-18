import pygame
from dataclasses import dataclass
from typing import Optional


@dataclass
class PowerUpSpec:
    kind: str  # 'invencibilidade', 'pulo_duplo', 'escudo'
    image: Optional[pygame.Surface]
    width: int = 24
    height: int = 24


class PowerUp:
    def __init__(self, x: int, y: int, spec: PowerUpSpec):
        self.x = x
        self.y = y
        self.spec = spec

        self.width = spec.width if hasattr(spec, "width") else 24
        self.height = spec.height if hasattr(spec, "height") else 24
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible = True
        self.blink_counter = 0
        self.blink_interval = 20  # frames por alternância
        self.collected = False

        # Cache de imagem escalada para evitar resize por frame
        self._scaled_image: Optional[pygame.Surface] = None
        if spec.image is not None:
            try:
                self._scaled_image = pygame.transform.smoothscale(
                    spec.image, (self.width, self.height)
                )
            except Exception:
                self._scaled_image = pygame.transform.scale(
                    spec.image, (self.width, self.height)
                )

    def update(self) -> None:
        if self.collected:
            return
        self.blink_counter += 1
        if self.blink_counter >= self.blink_interval:
            self.visible = not self.visible
            self.blink_counter = 0
        # Sincronizar rect
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        if self.collected or not self.visible:
            return
        img = self._scaled_image
        if img is None:
            return
        screen.blit(img, (self.x - camera_x, self.y))

    def collect(self) -> None:
        self.collected = True
from dataclasses import dataclass


@dataclass
class PowerUpSpec:
    kind: str  # 'invincibilidade' | 'pulo_duplo' | 'escudo'
    image: pygame.Surface
    width: int
    height: int


class PowerUp:
    def __init__(self, x, y, spec: PowerUpSpec):
        self.x = x
        self.y = y
        self.spec = spec
        self.width = spec.width
        self.height = spec.height

        # Rect used for collision checks
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Blinking control (match ExtraLife timing/feel)
        self.blink_period = 20
        self.blink_timer = 0
        self.current_alpha = 255

    def update(self):
        # Blink: alternate alpha between visible and dimmed
        self.blink_timer = (self.blink_timer + 1) % self.blink_period
        self.current_alpha = 255 if self.blink_timer < self.blink_period // 2 else 90
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen: pygame.Surface, camera_offset_x: int, camera_offset_y: int = 0):
        # Only draw within camera viewport bounds check is external (like ExtraLife)
        img = self.spec.image.copy()
        # Apply alpha blink
        img.set_alpha(self.current_alpha)
        screen.blit(img, (self.x - camera_offset_x, self.y - camera_offset_y))