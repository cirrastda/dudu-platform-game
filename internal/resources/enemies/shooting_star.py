import pygame
from internal.utils.constants import HEIGHT, DARK_GRAY, YELLOW, WHITE


class ShootingStar:
    _id_counter = 0

    def __init__(self, x: int, y: int, image: pygame.Surface | None = None):
        self.x = x
        self.y = y
        self.width = 26
        self.height = 26
        # Very fast horizontal speed; slight downward drift
        self.speed_x = 6.0
        self.speed_y = 0.8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = -1  # moves left

        ShootingStar._id_counter += 1
        self.id = ShootingStar._id_counter

        self.image = image
        self.animation_frame = 0
        self.animation_speed = 8

        # Death/fall state similar to birds/bats
        self.is_dead = False
        self.death_timer = 0
        self.fall_speed = 3.2

    def update(self, camera_x: int = 0):
        if not self.is_dead:
            # Move fast to the left with slight downward drift
            self.x += self.speed_x * self.direction
            self.y += self.speed_y
            self.rect.x = self.x
            self.rect.y = self.y
            self.animation_frame += 1
            # Cull when far outside camera view
            if self.x < camera_x - 300 or self.x > camera_x + 1400:
                return False
            return True
        else:
            # Simple fall on death
            self.y += self.fall_speed
            self.death_timer += 1
            self.rect.x = self.x
            self.rect.y = self.y
            if self.y > HEIGHT + 100 or self.death_timer > 180:
                return False
            return True

    def die(self):
        self.is_dead = True
        self.death_timer = 0
        self.speed_x = 0
        self.speed_y = 0
        self.direction = 0

    def draw(self, screen: pygame.Surface):
        # If an image is supplied, draw it; otherwise draw a simple star with a trail
        if self.image and not self.is_dead:
            screen.blit(self.image, (self.x, self.y))
            return

        # Basic star representation with trail
        if not self.is_dead:
            cx, cy = int(self.x + self.width / 2), int(self.y + self.height / 2)
            # Draw a small star
            pygame.draw.circle(screen, YELLOW, (cx, cy), 4)
            pygame.draw.line(screen, WHITE, (cx - 8, cy - 2), (cx + 8, cy - 2), 1)
            pygame.draw.line(screen, WHITE, (cx - 8, cy + 2), (cx + 8, cy + 2), 1)
            # Trail
            tail_points = [
                (self.x - 2, self.y + 10),
                (self.x - 12, self.y + 8),
                (self.x - 22, self.y + 6),
                (self.x - 32, self.y + 4),
            ]
            for i in range(len(tail_points) - 1):
                pygame.draw.line(screen, WHITE, tail_points[i], tail_points[i + 1], 1)
        else:
            # Dead: rotated cross to indicate destruction
            cx, cy = int(self.x + self.width / 2), int(self.y + self.height / 2)
            pygame.draw.line(screen, DARK_GRAY, (cx - 6, cy - 6), (cx + 6, cy + 6), 2)
            pygame.draw.line(screen, DARK_GRAY, (cx - 6, cy + 6), (cx + 6, cy - 6), 2)
