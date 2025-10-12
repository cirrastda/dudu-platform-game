import pygame
import random
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Robot:
    _id_counter = 0  # Contador de ID para robôs

    def __init__(self, x, y, left_limit, right_limit, robot_images=None, missile_images=None):
        self.x = x
        self.y = y
        self.width = 57
        self.height = 57
        self.speed = 1.5  # Velocidade um pouco maior que tartarugas
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.platform_left = left_limit  # Limite esquerdo da plataforma
        self.platform_right = right_limit  # Limite direito da plataforma
        self.direction = -1  # -1 para esquerda, 1 para direita

        # Atribuir ID único
        Robot._id_counter += 1
        self.id = Robot._id_counter

        # Animação
        self.robot_images = robot_images  # Dicionário com imagens de movimento e tiro
        self.missile_images = missile_images  # Dicionário com imagens dos mísseis
        self.animation_frame = 0
        self.animation_speed = 12  # Velocidade de animação
        
        # Sistema de tiro
        self.shoot_timer = 0
        self.shoot_interval = random.randint(120, 240)  # 2-4 segundos entre tiros
        self.is_shooting = False
        self.shoot_animation_timer = 0
        self.shoot_animation_duration = 30  # Duração da animação de tiro (0.5 segundos)
        self.missiles = []  # Lista de mísseis ativos

    def update(self, camera_x=0):
        # Atualizar timer de tiro
        self.shoot_timer += 1
        
        # Verificar se deve atirar (apenas quando virado para a esquerda)
        if self.shoot_timer >= self.shoot_interval and not self.is_shooting and self.direction == -1:
            self.start_shooting(self.missile_images)
            
        # Atualizar animação de tiro
        if self.is_shooting:
            self.shoot_animation_timer += 1
            if self.shoot_animation_timer >= self.shoot_animation_duration:
                self.is_shooting = False
                self.shoot_animation_timer = 0
                self.shoot_timer = 0
                self.shoot_interval = random.randint(120, 240)  # Novo intervalo aleatório
        else:
            # Mover robô apenas quando não está atirando
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

        # Atualizar mísseis
        active_missiles = []
        for missile in self.missiles:
            if missile.update(camera_x):
                active_missiles.append(missile)
        self.missiles = active_missiles

        return True  # Robô sempre permanece ativo

    def start_shooting(self, missile_images=None):
        """Inicia a animação de tiro e cria um míssil"""
        self.is_shooting = True
        self.shoot_animation_timer = 0
        
        # Criar míssil na posição do robô
        from internal.resources.missile import Missile
        missile_x = self.x + (self.width // 2)
        missile_y = self.y + (self.height // 2)
        missile = Missile(missile_x, missile_y, self.direction, missile_images)
        self.missiles.append(missile)

    def draw(self, screen):
        if self.robot_images:
            # Escolher conjunto de imagens baseado no estado
            if self.is_shooting:
                # Usar imagens de tiro
                if self.direction == 1:  # Direita
                    images = self.robot_images.get('shot_right', [])
                else:  # Esquerda
                    images = self.robot_images.get('shot_left', [])
            else:
                # Usar imagens de movimento
                if self.direction == 1:  # Direita
                    images = self.robot_images.get('right', [])
                else:  # Esquerda
                    images = self.robot_images.get('left', [])
            
            if images and len(images) > 0:
                # Usar animação com as imagens carregadas
                current_image_index = (self.animation_frame // self.animation_speed) % len(images)
                current_image = images[current_image_index]
                if current_image:
                    screen.blit(current_image, (self.x, self.y))
                    return
        
        # Fallback: desenhar retângulo se imagens não estão disponíveis
        color = (150, 75, 0) if not self.is_shooting else (255, 100, 0)  # Marrom ou laranja quando atirando
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Desenhar mísseis
        for missile in self.missiles:
            missile.draw(screen)