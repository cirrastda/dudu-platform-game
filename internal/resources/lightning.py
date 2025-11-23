import pygame


class LightningBeam:
    def __init__(
        self,
        start_pos,
        end_pos,
        orientation: str,
        segment_image: pygame.Surface | None,
    ):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.orientation = orientation  # 'h' or 'v'
        self.segment_image = segment_image
        self.active = True
        self.blink_period = 16
        self.blink_timer = 0
        self.alpha_strong = 255
        self.alpha_weak = 120
        # Área de colisão contínua
        # Lista de segmentos válidos (cada um como pygame.Rect)
        self.segments: list[pygame.Rect] = []
        if orientation == 'h':
            x1, y1 = start_pos
            x2, _ = end_pos
            width = abs(x2 - x1)
            height = segment_image.get_height() if segment_image else 8
            self.rect = pygame.Rect(min(x1, x2), y1, width, height)
        else:
            x1, y1 = start_pos
            _, y2 = end_pos
            width = segment_image.get_width() if segment_image else 8
            height = abs(y2 - y1)
            self.rect = pygame.Rect(x1, min(y1, y2), width, height)

    def update(self):
        if not self.active:
            return
        self.blink_timer = (self.blink_timer + 1) % self.blink_period

    def draw(self, screen: pygame.Surface, camera_x: int):
        if not self.active:
            return
        alpha = (
            self.alpha_strong
            if self.blink_timer < self.blink_period // 2
            else self.alpha_weak
        )
        if self.segment_image:
            img = self.segment_image.copy()
            img.set_alpha(alpha)
            for seg in self.segments:
                screen.blit(img, (seg.x - camera_x, seg.y))
        else:
            color = (
                (255, 255, 0)
                if self.blink_timer < self.blink_period // 2
                else (240, 240, 120)
            )
            for seg in self.segments:
                r = seg.copy()
                r.x -= camera_x
                pygame.draw.rect(screen, color, r)

    def build_segments(self, platform_rects: list[pygame.Rect]):
        # Construir segmentos repetindo a imagem sem esticar e evitando plataformas
        self.segments = []
        if not self.segment_image:
            return
        if self.orientation == 'h':
            step = max(1, self.segment_image.get_width())
            x = min(self.start_pos[0], self.end_pos[0])
            y = self.start_pos[1]
            total = abs(self.end_pos[0] - self.start_pos[0])
            cur = 0
            h = self.segment_image.get_height()
            while cur + step <= total:
                rect = pygame.Rect(x + cur, y, step, h)
                if not any(rect.colliderect(p) for p in platform_rects):
                    self.segments.append(rect)
                cur += step

        else:
            step = max(1, self.segment_image.get_height())
            x = self.start_pos[0]
            y = min(self.start_pos[1], self.end_pos[1])
            total = abs(self.end_pos[1] - self.start_pos[1])
            cur = 0
            w = self.segment_image.get_width()
            while cur + step <= total:
                rect = pygame.Rect(x, y + cur, w, step)
                if not any(rect.colliderect(p) for p in platform_rects):
                    self.segments.append(rect)
                cur += step
