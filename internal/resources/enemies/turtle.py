import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Turtle:
    _id_counter = 0  # Contador de ID para tartarugas

    def __init__(self, x, y, left_limit, right_limit, turtle_images=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 1  # Movimento lento
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.platform_left = left_limit  # Limite esquerdo da plataforma
        self.platform_right = right_limit  # Limite direito da plataforma
        self.direction = (
            -1
        )  # -1 para esquerda, 1 para direita (começa indo para esquerda)

        # Atribuir ID único
        Turtle._id_counter += 1
        self.id = Turtle._id_counter

        # Animação
        self.turtle_images = turtle_images  # Dicionário com left e right arrays
        self.animation_frame = 0
        self.animation_speed = (
            15  # Frames para trocar de imagem (mais lento que pássaro)
        )
        # Estado de morte
        self.is_dead = False
        self.death_timer = 0
        self.fall_speed = 2

    def update(self):
        if not self.is_dead:
            # Mover tartaruga na direção atual
            self.x += self.speed * self.direction

            # Verificar limites da plataforma e inverter direção
            if self.x <= self.platform_left:
                self.x = self.platform_left
                self.direction = 1  # Mudar para direita
            elif self.x >= self.platform_right:
                self.x = self.platform_right
                self.direction = -1  # Mudar para esquerda

            self.rect.x = self.x

            # Atualizar animação
            self.animation_frame += 1

            return True  # Tartaruga permanece ativa
        else:
            # Morte: queda fora da plataforma
            self.y += self.fall_speed
            self.death_timer += 1
            self.rect.x = self.x
            self.rect.y = self.y
            # Remover quando sair da tela ou após duração
            if self.y > HEIGHT + 100 or self.death_timer > 240:
                return False
            return True

    def die(self):
        self.is_dead = True
        self.death_timer = 0
        # Parar movimento horizontal
        self.speed = 0
        self.direction = 0

    def draw(self, screen):
        if (
            self.turtle_images
            and "left" in self.turtle_images
            and "right" in self.turtle_images
        ):
            if not self.is_dead:
                # Usar animação com as imagens carregadas
                current_images = (
                    self.turtle_images["left"]
                    if self.direction == -1
                    else self.turtle_images["right"]
                )
                if current_images and len(current_images) > 0:
                    current_image_index = (
                        self.animation_frame // self.animation_speed
                    ) % len(current_images)
                    current_image = current_images[current_image_index]
                    if current_image:
                        screen.blit(current_image, (self.x, self.y))
                        return
            else:
                # Mostrar sprite invertido para indicar morte
                current_images = self.turtle_images.get("left") or []
                if current_images:
                    img = current_images[0]
                    flipped = pygame.transform.flip(img, False, True)
                    screen.blit(flipped, (self.x, self.y))
                    return

        # Fallback para o desenho original se as imagens não carregaram
        color = (34, 139, 34) if not self.is_dead else (200, 50, 50)
        pygame.draw.ellipse(
            screen, color, self.rect
        )  # Verde escuro para tartaruga
        # Adicionar detalhes simples (cabeça)
        head_x = self.x + (5 if self.direction == 1 else self.width - 15)
        if not self.is_dead:
            pygame.draw.circle(screen, (0, 100, 0), (head_x, self.y + 10), 8)
        # Patas
        if not self.is_dead:
            pygame.draw.circle(screen, (0, 80, 0), (self.x + 8, self.y + 20), 4)
            pygame.draw.circle(
                screen, (0, 80, 0), (self.x + self.width - 8, self.y + 20), 4
            )
