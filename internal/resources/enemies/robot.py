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

        # Estado de morte
        self.is_dead = False
        self.death_timer = 0
        self.fall_speed = 0.0
        self.rotation_angle = 0

    def update(self, camera_x=0):
        if not self.is_dead:
            # Atualizar timer de tiro
            self.shoot_timer += 1

            # Verificar se deve atirar (apenas quando virado para a esquerda)
            if (
                self.shoot_timer >= self.shoot_interval
                and not self.is_shooting
                and self.direction == -1
            ):
                self.start_shooting(self.missile_images)

            # Atualizar animação de tiro
            if self.is_shooting:
                self.shoot_animation_timer += 1
                if self.shoot_animation_timer >= self.shoot_animation_duration:
                    self.is_shooting = False
                    self.shoot_animation_timer = 0
                    self.shoot_timer = 0
                    self.shoot_interval = random.randint(120, 240)
            else:
                # Mover robô apenas quando não está atirando
                self.x += self.speed * self.direction

                # Verificar limites da plataforma e inverter direção
                if self.x <= self.platform_left:
                    self.x = self.platform_left
                    self.direction = 1
                elif self.x >= self.platform_right:
                    self.x = self.platform_right
                    self.direction = -1

            self.rect.x = self.x

            # Atualizar animação
            self.animation_frame += 1
        else:
            # Morte: queda com aceleração e leve rotação
            self.fall_speed += 0.5
            self.y += self.fall_speed
            self.rotation_angle = min(self.rotation_angle + 4, 40)
            self.rect.y = self.y
            self.death_timer += 1
            # Remover após sair da tela ou após duração
            if self.y > HEIGHT + 60:
                return False
            if self.death_timer > 240:
                return False

        # Atualizar mísseis
        active_missiles = []
        for missile in self.missiles:
            if missile.update(camera_x):
                active_missiles.append(missile)
        self.missiles = active_missiles

        return True

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
            if self.is_dead:
                # Usar primeira imagem da orientação atual, levemente rotacionada
                images = (
                    self.robot_images.get('right', []) if self.direction == 1
                    else self.robot_images.get('left', [])
                )
                current_image = images[0] if images else None
                if current_image:
                    rotated = pygame.transform.rotate(current_image, self.rotation_angle)
                    screen.blit(rotated, (self.x, self.y))
                    # Não desenhar mísseis do robô morto
                    return
            elif self.is_shooting:
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
        color = (200, 60, 60) if self.is_dead else ((150, 75, 0) if not self.is_shooting else (255, 100, 0))
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Desenhar mísseis
        if not self.is_dead:
            for missile in self.missiles:
                missile.draw(screen)

    def die(self):
        # Iniciar estado de morte: parar tiro e iniciar queda
        self.is_dead = True
        self.is_shooting = False
        self.death_timer = 0
        self.fall_speed = 0.0
        self.rotation_angle = 0