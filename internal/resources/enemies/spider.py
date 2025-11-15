import pygame
import math
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Spider:
    _id_counter = 0  # Contador de ID para aranhas

    def __init__(self, x, y, top_limit, bottom_limit, spider_images=None):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 25
        self.speed = 1.5  # Velocidade de movimento vertical
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.top_limit = top_limit  # Limite superior do movimento
        self.bottom_limit = (
            bottom_limit  # Limite inferior do movimento (máximo na linha da plataforma)
        )
        self.direction = 1  # 1 para baixo, -1 para cima
        self.web_start_y = top_limit  # Ponto inicial da teia

        # Atribuir ID único
        Spider._id_counter += 1
        self.id = Spider._id_counter

        # Animação
        self.spider_images = spider_images
        self.animation_frame = 0
        self.animation_speed = 12  # Velocidade de animação mais lenta que pássaros
        # Estado de morte
        self.is_dead = False
        self.death_timer = 0
        # Parâmetros da animação de morte (linha balançando e rompendo)
        self.sway_timer = 0
        self.sway_duration = 40
        self.sway_amplitude = 12
        self.sway_frequency = 0.35
        self.detached = False
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.gravity = 0.2
        self.die_base_x = x

    def update(self, camera_x=0):
        if not self.is_dead:
            # Mover aranha na direção atual
            self.y += self.speed * self.direction

            # Verificar limites e inverter direção
            if self.y <= self.top_limit:
                self.y = self.top_limit
                self.direction = 1  # Mudar para baixo
            elif self.y >= self.bottom_limit:
                self.y = self.bottom_limit
                self.direction = -1  # Mudar para cima

            self.rect.y = self.y

            # Atualizar animação
            self.animation_frame += 1

            return True  # Aranha permanece ativa
        else:
            # Morte: primeiro balançar preso à teia, depois voar longe (linha rompe)
            self.death_timer += 1
            if not self.detached:
                # Balanço lateral em torno da posição base
                self.sway_timer += 1
                offset = math.sin(self.sway_timer * self.sway_frequency) * self.sway_amplitude
                # Oscilar apenas no eixo X, mantendo Y
                self.x = self.die_base_x + offset
                # Após duração, romper a linha e iniciar voo
                if self.sway_timer >= self.sway_duration:
                    self.detached = True
                    # Direção de fuga: para a direita e para cima
                    self.vel_x = 4.0
                    self.vel_y = -3.0
                self.rect.x = self.x
                self.rect.y = self.y
                return True
            else:
                # Voo após linha romper: movimento balístico simples
                self.vel_y += self.gravity
                self.x += self.vel_x
                self.y += self.vel_y
                self.rect.x = self.x
                self.rect.y = self.y
                # Remover quando sair da tela ou após duração
                if (
                    self.x > camera_x + WIDTH + 100
                    or self.y > HEIGHT + 120
                    or self.death_timer > 240
                ):
                    return False
                return True

    def die(self):
        self.is_dead = True
        self.death_timer = 0
        self.sway_timer = 0
        self.detached = False
        self.die_base_x = self.x

    def draw(self, screen):
        # Desenhar teia somente enquanto não rompeu
        if not self.is_dead or (self.is_dead and not self.detached):
            pygame.draw.line(
                screen,
                WHITE,
                (self.x + self.width // 2, self.web_start_y),
                (self.x + self.width // 2, self.y),
                2,
            )

        if self.spider_images and len(self.spider_images) > 0:
            if not self.is_dead:
                # Usar animação com as imagens carregadas
                current_image_index = (self.animation_frame // self.animation_speed) % len(
                    self.spider_images
                )
                current_image = self.spider_images[current_image_index]
                if current_image:
                    screen.blit(current_image, (self.x, self.y))
                    return
            else:
                # Durante morte, rotacionar levemente enquanto voa
                current_image = self.spider_images[0]
                if current_image:
                    angle = -20 if not self.detached else -35
                    rotated = pygame.transform.rotate(current_image, angle)
                    screen.blit(rotated, (self.x, self.y))
                    return

        # Fallback para o desenho original se as imagens não carregaram
        color = BLACK if not self.is_dead else (50, 50, 50)
        pygame.draw.ellipse(screen, color, self.rect)
        # Adicionar detalhes simples (patas) apenas se não estiver morto
        if not self.is_dead:
            leg_length = 8
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            pygame.draw.line(screen, BLACK, (center_x - 5, center_y - 3), (center_x - leg_length, center_y - 8), 2)
            pygame.draw.line(screen, BLACK, (center_x - 5, center_y), (center_x - leg_length, center_y), 2)
            pygame.draw.line(screen, BLACK, (center_x - 5, center_y + 3), (center_x - leg_length, center_y + 8), 2)
            pygame.draw.line(screen, BLACK, (center_x + 5, center_y - 3), (center_x + leg_length, center_y - 8), 2)
            pygame.draw.line(screen, BLACK, (center_x + 5, center_y), (center_x + leg_length, center_y), 2)
            pygame.draw.line(screen, BLACK, (center_x + 5, center_y + 3), (center_x + leg_length, center_y + 8), 2)
