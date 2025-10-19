import pygame
import random
from internal.utils.constants import *


class BossAlien:
    def __init__(self, x, y, platforms, boss_images=None):
        self.x = x
        self.y = y
        self.width = 57
        self.height = 57
        self.speed = 8.0  # Velocidade do boss (significativamente maior que o jogador)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.platforms = platforms  # Lista de plataformas para navegação
        self.current_platform_index = 0
        self.direction = 1  # Sempre correndo para a direita
        self.state = "running"  # "running", "jumping", "stopped"
        
        # Posição alvo (sempre à frente do jogador)
        self.target_x = x + 75  # 50-100px à frente
        self.last_platform = platforms[-1] if platforms else None
        self.stop_position = None
        if self.last_platform:
            self.stop_position = self.last_platform[0] + self.last_platform[2] - 20  # 20px do final
        
        # Animação
        self.boss_images = boss_images
        self.animation_frame = 0
        self.animation_speed = 8
        
        # Sistema de salto
        self.vel_y = 0
        self.on_ground = True
        self.gravity = 0.65  # Gravidade ligeiramente reduzida (19% menor que o jogador)
        self.jump_strength = -25.0  # Salto muito mais forte para alcançar plataformas altas
        self.is_jumping_to_next_platform = False  # Controla se está saltando para próxima plataforma
        
        # Estado de parada
        self.is_stopped = False
        self.reached_stop_position = False
        
        # Sistema de recuperação quando preso
        self.stuck_counter = 0
        self.last_x = x
        self.stuck_threshold = 60  # frames sem movimento significativo
        
    def update(self, player_x, camera_x):
        """Atualizar boss alien"""
        if self.is_stopped:
            # Boss parado, apenas animar
            self.animation_frame += 1
            return
            
        # Verificar se chegou na posição de parada
        if self.stop_position and self.x >= self.stop_position - 20:
            self.is_stopped = True
            self.reached_stop_position = True
            self.state = "stopped"
            return
            
        # Sistema de posicionamento à frente do jogador (mais cauteloso no início)
        target_distance = 120  # Distância desejada à frente do jogador
        target_x = player_x + target_distance
        distance_to_target = target_x - self.x
        
        # Se o alien estiver atrás do jogador, acelerar gradualmente
        if self.x < player_x:
            target_distance = 150  # Distância maior quando atrás
            target_x = player_x + target_distance
            distance_to_target = target_x - self.x
        
        # Velocidade adaptativa mais cautelosa para evitar saltos prematuros
        if distance_to_target > 200:  # Muito atrás - velocidade alta mas controlada
            self.speed = 8.0
        elif distance_to_target > 150:  # Moderadamente atrás - velocidade moderada
            self.speed = 7.0
        elif distance_to_target > 100:  # Ligeiramente atrás - velocidade normal
            self.speed = 6.0
        elif distance_to_target > 50:  # Próximo do alvo - velocidade reduzida
            self.speed = 5.0
        elif distance_to_target > 0:  # Muito próximo - velocidade baixa
            self.speed = 4.0
        else:  # À frente - velocidade mínima
            self.speed = 3.0
        
        # Sistema de detecção de travamento
        if abs(self.x - self.last_x) < 0.5:  # Movimento muito pequeno
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0
        self.last_x = self.x
        
        # Movimento horizontal simplificado
        if self.on_ground:
            # Ajustar threshold baseado na situação
            movement_threshold = -15 if abs(distance_to_target) > 100 else -25
            
            if distance_to_target > movement_threshold:
                next_x = self.x + self.speed
                
                # Movimento direto - apenas verificar se não vai cair em buraco mortal
                if not self.detect_hole_ahead(next_x):
                    self.x += self.speed
                else:
                    # Se há buraco, tentar movimento mais lento
                    if not self.detect_hole_ahead(self.x + 1.0):
                        self.x += 1.0
                    else:
                        # Parar se há buraco perigoso
                        self.stuck_counter += 1
            
        # Aplicar gravidade e movimento vertical
        if not self.on_ground:
            self.vel_y += self.gravity
            self.state = "jumping"
            
            # Movimento horizontal durante o salto para alcançar próxima plataforma
            if self.is_jumping_to_next_platform:
                # Quando está saltando para próxima plataforma, sempre continuar para frente
                # independente da posição do jogador
                jump_speed = self.speed * 1.8  # Velocidade horizontal muito aumentada durante o salto
                next_x = self.x + jump_speed
                
                # Movimento mais permissivo durante o salto
                if self.is_safe_to_move_during_jump(next_x):
                    self.x += jump_speed
                elif self.x + jump_speed < self.stop_position if self.stop_position else True:
                    # Movimento forçado durante salto se não ultrapassar limite
                    self.x += jump_speed * 0.9  # Movimento mais agressivo
            elif distance_to_target > -20:  # Lógica original para outros casos
                jump_speed = self.speed * 1.8
                next_x = self.x + jump_speed
                
                if self.is_safe_to_move_during_jump(next_x):
                    self.x += jump_speed
                elif self.x + jump_speed < self.stop_position if self.stop_position else True:
                    self.x += jump_speed * 0.9
        else:
            self.state = "running"
            
        # Atualizar posição vertical
        self.y += self.vel_y
        
        # Atualizar rect ANTES da verificação de colisão
        self.rect.x = self.x
        self.rect.y = self.y
            
        # Verificar colisão com plataformas
        self.check_platform_collision()
        
        # Verificar se precisa pular (apenas quando no chão)
        if self.on_ground:
            self.check_jump_needed()
        
        # Atualizar animação
        self.animation_frame += 1
        
    def check_platform_collision(self):
        """Verificar colisão com plataformas com detecção mais tolerante"""
        self.on_ground = False
        
        # Encontrar a plataforma mais próxima para pouso
        best_platform = None
        min_distance = float('inf')
        
        for platform_data in self.platforms:
            platform_x, platform_y, platform_w, platform_h = platform_data
            platform_rect = pygame.Rect(platform_x, platform_y, platform_w, platform_h)
            
            # Verificar se está caindo e há sobreposição horizontal (mais tolerante)
            if (self.vel_y >= 0 and 
                self.rect.bottom >= platform_rect.top - 15 and 
                self.rect.bottom <= platform_rect.top + 35):
                
                # Calcular sobreposição horizontal
                overlap_left = max(self.rect.left, platform_rect.left)
                overlap_right = min(self.rect.right, platform_rect.right)
                overlap_width = overlap_right - overlap_left
                
                # Reduzir exigência de sobreposição para 40% da largura do alien
                min_overlap = self.width * 0.4
                if overlap_width >= min_overlap:
                    distance = abs(self.rect.bottom - platform_rect.top)
                    if distance < min_distance:
                        min_distance = distance
                        best_platform = platform_rect
        
        # Pousar na melhor plataforma encontrada
        if best_platform:
            self.y = best_platform.top - self.height
            self.vel_y = 0
            self.on_ground = True
            self.is_jumping_to_next_platform = False  # Resetar controle de salto ao pousar
            # Atualizar rect após correção de posição
            self.rect.y = self.y
                
    def detect_hole_ahead(self, next_x, check_distance=80):
        """Detecta se há um buraco perigoso à frente (menos restritivo)"""
        alien_bottom = self.y + self.height
        
        # Verificar apenas o ponto central à frente (menos pontos de verificação)
        check_x = next_x + self.width/2
        
        # Verificar se há plataforma sólida neste ponto
        has_support = False
        
        for platform_data in self.platforms:
            platform_x, platform_y, platform_w, platform_h = platform_data
            
            # Verificar se o ponto está sobre uma plataforma (mais tolerante)
            if (check_x >= platform_x - 10 and check_x <= platform_x + platform_w + 10 and
                platform_y >= alien_bottom - 10 and platform_y <= alien_bottom + 50):
                has_support = True
                break
        
        # Se não há suporte, verificar se há uma plataforma próxima para saltar
        if not has_support:
            # Procurar por plataforma próxima que possa ser alcançada com salto
            for platform_data in self.platforms:
                platform_x, platform_y, platform_w, platform_h = platform_data
                distance_to_platform = platform_x - next_x
                height_diff = abs(platform_y - (self.y + self.height))
                
                # Se há uma plataforma alcançável, não é um buraco perigoso
                if (distance_to_platform > 0 and distance_to_platform <= 120 and
                    height_diff <= 60):
                    return False
            
            return True  # Só retorna True se realmente não há plataforma alcançável
        
        return False
    
    def is_safe_to_move(self, next_x):
        """Verificar se é seguro mover para a posição next_x (menos restritivo para permitir aproximação da borda)"""
        # Posição futura do alien
        alien_bottom = self.y + self.height
        alien_left = next_x
        alien_right = next_x + self.width
        alien_center_x = next_x + self.width / 2
        
        # Primeiro, verificar se ainda está na plataforma atual (prioridade)
        current_platform = self.get_current_platform()
        if current_platform:
            curr_x, curr_y, curr_w, curr_h = current_platform
            # Permitir movimento até muito próximo da borda (apenas 5px de margem)
            if (alien_center_x >= curr_x - 5 and 
                alien_center_x <= curr_x + curr_w + 5):
                return True
        
        # Encontrar a melhor plataforma para suporte
        best_platform = None
        best_overlap = 0
        
        for platform_data in self.platforms:
            platform_x, platform_y, platform_w, platform_h = platform_data
            platform_rect = pygame.Rect(platform_x, platform_y, platform_w, platform_h)
            
            # Verificar se a plataforma está numa altura adequada (muito tolerante)
            if (platform_rect.top >= alien_bottom - 20 and 
                platform_rect.top <= alien_bottom + 50):
                
                # Calcular sobreposição horizontal
                overlap_left = max(alien_left, platform_rect.left)
                overlap_right = min(alien_right, platform_rect.right)
                overlap_width = overlap_right - overlap_left
                
                # Verificar se há sobreposição suficiente
                if overlap_width > 0:
                    overlap_percentage = overlap_width / self.width
                    if overlap_percentage > best_overlap:
                        best_overlap = overlap_percentage
                        best_platform = platform_data
        
        # Reduzir ainda mais a exigência de sobreposição para 30%
        if best_overlap >= 0.30:
            return True
        
        # Verificar buraco apenas como último recurso
        if self.detect_hole_ahead(next_x):
            return False
            
        return True  # Por padrão, permitir movimento (menos restritivo)
    
    def is_safe_to_move_during_jump(self, next_x):
        """Verificação mais cautelosa para movimento durante salto"""
        # Primeiro, verificar se há buraco no destino (mesmo durante salto)
        if self.detect_hole_ahead(next_x):
            return False
        
        # Durante o salto, projetar onde o alien vai pousar
        alien_bottom = self.y + self.height + 60  # Projeção mais baixa para detectar plataformas de destino
        alien_center_x = next_x + self.width / 2
        alien_left = next_x
        alien_right = next_x + self.width
        
        # Verificar se há plataforma adequada para pouso
        suitable_platform_found = False
        
        for platform_data in self.platforms:
            platform_x, platform_y, platform_w, platform_h = platform_data
            platform_rect = pygame.Rect(platform_x, platform_y, platform_w, platform_h)
            
            # Verificar se há plataforma na direção do movimento
            if (alien_center_x >= platform_rect.left - 10 and 
                alien_center_x <= platform_rect.right + 10):
                
                # Verificar se a plataforma está numa altura razoável para pouso
                if (platform_rect.top >= self.y and 
                    platform_rect.top <= alien_bottom + 40):  # Menos tolerante
                    
                    # Verificar sobreposição horizontal adequada
                    overlap_left = max(alien_left, platform_rect.left)
                    overlap_right = min(alien_right, platform_rect.right)
                    overlap_width = overlap_right - overlap_left
                    
                    if overlap_width > 0:
                        overlap_percentage = overlap_width / self.width
                        if overlap_percentage >= 0.4:  # Pelo menos 40% de sobreposição
                            suitable_platform_found = True
                            break
        
        # Só permitir movimento se encontrou plataforma adequada
        if suitable_platform_found:
            return next_x < (self.stop_position - 50) if self.stop_position else True
        
        return False
    
    def get_current_platform(self):
        """Encontra a plataforma atual onde o alien está"""
        for platform_data in self.platforms:
            platform_x, platform_y, platform_w, platform_h = platform_data
            if (self.x + self.width/2 >= platform_x and 
                self.x + self.width/2 <= platform_x + platform_w and
                abs(self.y + self.height - platform_y) < 20):
                return platform_data
        return None
    
    def has_platform_ahead(self):
        """Verifica se há uma plataforma à frente para saltar (detecção mais inteligente)"""
        current_platform = self.get_current_platform()
        if not current_platform:
            return False
            
        platform_x, platform_y, platform_w, platform_h = current_platform
        
        # Verificar se está próximo da borda da plataforma atual
        distance_to_edge = (platform_x + platform_w) - (self.x + self.width)
        if distance_to_edge > 50:  # Ainda longe da borda
            return False
        
        # Procurar por plataforma à frente
        best_platform = None
        min_gap = float('inf')
        
        for platform_data in self.platforms:
            next_x, next_y, next_w, next_h = platform_data
            if next_x > platform_x + platform_w - 40:  # Plataforma à frente
                gap_distance = next_x - (platform_x + platform_w)
                height_diff = next_y - platform_y  # Diferença de altura (positivo = mais alto)
                
                # Considerar plataformas alcançáveis com salto
                if (gap_distance <= 140 and  # Gap maior permitido
                    height_diff >= -80 and height_diff <= 40):  # Pode pular para cima ou descer um pouco
                    if gap_distance < min_gap:
                        min_gap = gap_distance
                        best_platform = platform_data
        
        return best_platform is not None
    
    def check_jump_needed(self):
        """Lógica simples de salto baseada em pontos fixos das plataformas do nível 51"""
        if not self.on_ground:
            return
        
        # Verificar se está na última plataforma (não deve saltar)
        if self.is_on_last_platform():
            return
        
        # Pontos de salto calculados para o nível 51 (posição X onde deve saltar)
        # Baseado nas plataformas: (10,400), (500,400), (1000,400), (1500,400), etc.
        # Saltar quando estiver a ~80px do fim de cada plataforma
        jump_points = [
            330,   # Primeira plataforma (10 + 400 - 80)
            820,   # Segunda plataforma (500 + 400 - 80) 
            1320,  # Terceira plataforma (1000 + 400 - 80)
            1820,  # Quarta plataforma (1500 + 400 - 80)
            2320,  # Quinta plataforma (2000 + 400 - 80)
            2820,  # Sexta plataforma (2500 + 400 - 80)
            3320,  # Sétima plataforma (3000 + 400 - 80)
            3820,  # Oitava plataforma (3500 + 400 - 80)
            4320,  # Nona plataforma (4000 + 400 - 80)
            4820,  # Décima plataforma (4500 + 400 - 80)
            5320,  # Décima primeira plataforma (5000 + 400 - 80)
            5820,  # Décima segunda plataforma (5500 + 400 - 80)
            6320,  # Décima terceira plataforma (6000 + 400 - 80)
            6820,  # Décima quarta plataforma (6500 + 400 - 80)
            # Removido: 7320 - Décima quinta plataforma (última) - não deve saltar
        ]
        
        # Verificar se o alien passou de algum ponto de salto
        alien_x = self.x + self.width/2  # Centro do alien
        
        for jump_x in jump_points:
            # Se o alien passou do ponto de salto (com margem de 10px)
            if alien_x >= jump_x - 10 and alien_x <= jump_x + 10:
                self.jump()
                return
                
    def jump(self):
        """Fazer o boss pular (salto diagonal como o jogador)"""
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.state = "jumping"
            self.is_jumping_to_next_platform = True  # Marcar que está saltando para próxima plataforma
            
    def draw(self, screen):
        """Desenhar o boss alien"""
        if self.boss_images:
            if self.state == "stopped":
                # Usar imagem de parado
                if "stopped" in self.boss_images:
                    screen.blit(self.boss_images["stopped"], (self.x, self.y))
                    return
            elif self.state == "jumping":
                # Usar animação de salto
                if "jumping" in self.boss_images:
                    images = self.boss_images["jumping"]
                    if images and len(images) > 0:
                        current_image_index = (self.animation_frame // self.animation_speed) % len(images)
                        current_image = images[current_image_index]
                        if current_image:
                            screen.blit(current_image, (self.x, self.y))
                            return
            else:
                # Usar animação de corrida
                if "running" in self.boss_images:
                    images = self.boss_images["running"]
                    if images and len(images) > 0:
                        current_image_index = (self.animation_frame // self.animation_speed) % len(images)
                        current_image = images[current_image_index]
                        if current_image:
                            screen.blit(current_image, (self.x, self.y))
                            return
                            
        # Fallback: desenhar retângulo
        color = (255, 0, 0) if self.is_stopped else (255, 100, 0)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
    def is_on_last_platform(self):
        """Verifica se o alien está na última plataforma do nível 51"""
        if not self.platforms:
            return False
        
        # A última plataforma do nível 51 está em x=7000 com largura 400
        last_platform_x = 7000
        last_platform_width = 400
        
        alien_center_x = self.x + self.width/2
        
        # Verificar se o alien está na última plataforma
        if (alien_center_x >= last_platform_x and 
            alien_center_x <= last_platform_x + last_platform_width):
            return True
        
        return False
    
    def is_captured(self, player_rect):
        """Verifica se o alien foi capturado pelo jogador (apenas na última plataforma)"""
        if not self.rect.colliderect(player_rect):
            return False
            
        # Verificar se está na última plataforma
        if not self.platforms:
            return True
            
        # Encontrar a plataforma mais à direita (última plataforma)
        last_platform = None
        max_x = -1
        
        for platform_data in self.platforms:
            platform_x, platform_y, platform_w, platform_h = platform_data
            if platform_x + platform_w > max_x:
                max_x = platform_x + platform_w
                last_platform = platform_data
                
        if last_platform:
            platform_x, platform_y, platform_w, platform_h = last_platform
            # Verificar se o alien está na última plataforma
            if (self.x + self.width/2 >= platform_x and 
                self.x + self.width/2 <= platform_x + platform_w and
                abs(self.y + self.height - platform_y) < 20):
                return True
                
        return False