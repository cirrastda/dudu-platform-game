import pygame

from internal.utils.constants import HEIGHT


class Raindrop:
    def __init__(self, x: int, y: int, image: pygame.Surface):
        # Basic placement and visuals
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Lifecycle
        self.is_dead = False
        self.dead_timer = 0
        # Simple particle-style splash: three mini drops flying away
        self.particles = []

    def update(self) -> bool:
        """
        Update returns False when the raindrop should be culled from the game.
        """
        if not self.is_dead:
            self.y += self.speed
            self.rect.topleft = (self.x, self.y)
            # Off-screen cull
            if self.y > HEIGHT + self.height:
                return False
            return True

        # Dead: animate splash particles then cull
        self.dead_timer += 1
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.2  # a tiny gravity for arc movement
        # After short animation, remove
        return self.dead_timer < 30

    def die(self):
        if self.is_dead:
            return
        self.is_dead = True
        self.dead_timer = 0
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        # Create three particles moving outward
        self.particles = [
            {"x": cx, "y": cy, "vx": -2.0, "vy": -2.5, "angle": -25},
            {"x": cx, "y": cy, "vx": 2.0, "vy": -2.0, "angle": 25},
            {"x": cx, "y": cy, "vx": -1.0, "vy": 1.5, "angle": 75},
        ]

    def draw(self, surface: pygame.Surface, camera_x: int = 0):
        if not self.is_dead:
            surface.blit(self.image, (self.x, self.y))
            return

        # Draw three small rotated droplets as a splash effect (camera-aware)
        for p in self.particles:
            img = pygame.transform.rotozoom(self.image, p["angle"], 0.6)
            px = int(p["x"] - camera_x) - img.get_width() // 2
            py = int(p["y"]) - img.get_height() // 2
            surface.blit(img, (px, py))