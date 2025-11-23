import pygame


class Generator:
    _id_counter = 0

    def __init__(self, x: int, y: int, image: pygame.Surface | None):
        Generator._id_counter += 1
        self.id = Generator._id_counter
        self.x = x
        self.y = y
        self.image = image
        w = image.get_width() if image else 32
        h = image.get_height() if image else 32
        self.width = w
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.light_flash_timer = 0
        self.is_flashing = False

    def update(self):
        self.rect.topleft = (self.x, self.y)
        # Gerador não pisca
        self.is_flashing = False

    def draw(self, screen: pygame.Surface, camera_x: int):
        if self.image:
            screen.blit(self.image, (self.x - camera_x, self.y))
        else:
            pygame.draw.rect(
                screen,
                (200, 200, 255),
                (self.x - camera_x, self.y, self.width, self.height),
                1,
            )
        # Sem halo de iluminação
