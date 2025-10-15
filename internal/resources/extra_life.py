import pygame


class ExtraLife:
    def __init__(self, x, y, image=None, size=(24, 24)):
        self.x = int(x)
        self.y = int(y)
        self.width = size[0]
        self.height = size[1]

        # Imagem do item; preferir surface fornecida pelo Image.load_images
        if image is not None:
            self.image = image
        else:
            # Tentar carregar do caminho padrão do projeto como fallback
            try:
                self.image = pygame.image.load("imagens/elementos/vida.png")
                self.image = pygame.transform.scale(self.image, size)
            except Exception:
                # Fallback: círculo simples para evitar falhas
                self.image = pygame.Surface(size, pygame.SRCALPHA)
                pygame.draw.circle(
                    self.image,
                    (255, 0, 0, 255),
                    (size[0] // 2, size[1] // 2),
                    min(size) // 2,
                )

        # Controle de piscar (transparência alternando)
        self.blink_timer = 0
        self.blink_period = 20  # frames por fase
        self.current_alpha = 255

        # Retângulo para colisão
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.blink_timer = (self.blink_timer + 1) % (self.blink_period * 2)
        # Metade do tempo mais opaco, metade mais translúcido
        if self.blink_timer < self.blink_period:
            self.current_alpha = 255
        else:
            self.current_alpha = 90

        # Atualizar retângulo para colisão
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen, camera_x=0):
        if not self.image:
            return
        # Aplicar alpha atual e desenhar com offset da câmera
        self.image.set_alpha(self.current_alpha)
        screen.blit(self.image, (self.x - camera_x, self.y))