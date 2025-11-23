import pygame


class Meteor:
    _id_counter = 0

    def __init__(self, x: int, y: int, image: pygame.Surface | None = None):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed_x = -4.5
        self.speed_y = 4.5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = image
        self.is_dead = False
        self.death_timer = 0
        self.fall_speed = 4.0

        Meteor._id_counter += 1
        self.id = Meteor._id_counter

    def update(self, camera_x: int = 0):
        if not self.is_dead:
            self.x += self.speed_x
            self.y += self.speed_y
            self.rect.x = self.x
            self.rect.y = self.y
            if self.x < camera_x - 300 or self.x > camera_x + 1400:
                return False
            return True
        else:
            self.y += self.fall_speed
            self.death_timer += 1
            self.rect.x = self.x
            self.rect.y = self.y
            return self.death_timer <= 180

    def die(self):
        self.is_dead = True
        self.speed_x = 0
        self.speed_y = 0

    def draw(self, screen: pygame.Surface):
        if self.image and not self.is_dead:
            screen.blit(self.image, (self.x, self.y))
            return
        cx, cy = int(self.x + self.width / 2), int(self.y + self.height / 2)
        pygame.draw.circle(screen, (160, 160, 160), (cx, cy), 12)