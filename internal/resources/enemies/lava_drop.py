import pygame

from internal.utils.constants import HEIGHT


class LavaDrop:
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width() if image else 20
        self.height = image.get_height() if image else 20
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self) -> bool:
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
        if self.y > HEIGHT + self.height:
            return False
        return True

    def draw(self, surface: pygame.Surface, camera_x: int = 0):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.circle(
                surface,
                (255, 80, 0),
                (int(self.x), int(self.y)),
                10,
            )
