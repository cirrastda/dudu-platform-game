import pygame
import random
from internal.utils.constants import *


class Alien:
    _id_counter = 0  # Contador de ID para aliens

    def __init__(self, x, y, left_limit, right_limit, alien_images=None):
        self.x = x
        self.y = y
        self.width = 57
        self.height = 57
        self.speed = 1.5
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.platform_left = left_limit
        self.platform_right = right_limit
        self.direction = -1  # -1 para esquerda, 1 para direita

        Alien._id_counter += 1
        self.id = Alien._id_counter

        # Animação
        self.alien_images = alien_images  # Dicionário com imagens de movimento e tiro (esquerda)
        self.animation_frame = 0
        self.animation_speed = 12

        # Sistema de tiro (laser)
        self.shoot_timer = 0
        self.shoot_interval = random.randint(120, 240)  # 2-4s
        self.is_shooting = False
        self.shoot_animation_timer = 0
        self.shoot_animation_duration = 30
        self.lasers = []  # Lista de lasers ativos

    def update(self, camera_x=0):
        # Atualizar timer de tiro
        self.shoot_timer += 1

        # Atirar apenas quando virado para a esquerda
        if (
            self.shoot_timer >= self.shoot_interval
            and not self.is_shooting
            and self.direction == -1
        ):
            self.start_shooting()

        # Atualizar estado de tiro
        if self.is_shooting:
            self.shoot_animation_timer += 1
            if self.shoot_animation_timer >= self.shoot_animation_duration:
                self.is_shooting = False
                self.shoot_animation_timer = 0
                self.shoot_timer = 0
                self.shoot_interval = random.randint(120, 240)
        else:
            # Movimento apenas quando não atirando
            self.x += self.speed * self.direction
            if self.x <= self.platform_left:
                self.x = self.platform_left
                self.direction = 1
            elif self.x >= self.platform_right:
                self.x = self.platform_right
                self.direction = -1

        self.rect.x = self.x
        self.animation_frame += 1

        # Atualizar lasers
        active_lasers = []
        for laser in self.lasers:
            if laser.update(camera_x):
                active_lasers.append(laser)
        self.lasers = active_lasers

        return True

    def start_shooting(self):
        """Inicia a animação de tiro e cria um laser"""
        self.is_shooting = True
        self.shoot_animation_timer = 0

        from internal.resources.laser import Laser
        laser_x = self.x + (self.width // 2) - 10  # origem aproximada
        laser_y = self.y + (self.height // 2)
        # Laser sempre para a esquerda
        laser = Laser(laser_x, laser_y, -1)
        self.lasers.append(laser)

    def draw(self, screen):
        if self.alien_images:
            if self.is_shooting:
                images = self.alien_images.get("shot_left", [])
            else:
                images = (
                    self.alien_images.get("right", [])
                    if self.direction == 1
                    else self.alien_images.get("left", [])
                )

            if images and len(images) > 0:
                current_image_index = (
                    self.animation_frame // self.animation_speed
                ) % len(images)
                current_image = images[current_image_index]
                if current_image:
                    screen.blit(current_image, (self.x, self.y))
                    return

        # Fallback
        color = (50, 200, 50) if not self.is_shooting else (255, 50, 50)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        for laser in self.lasers:
            laser.draw(screen)