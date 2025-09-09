import pygame
import sys
import math
import os
import json
from enum import Enum

# Inicializar pygame
pygame.init()

# Constantes do jogo
WIDTH = 1200
HEIGHT = 800
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Constantes da câmera
CAMERA_OFFSET_X = WIDTH // 3  # Jogador fica no terço esquerdo da tela

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
LIGHT_BLUE = (135, 206, 235)
DARK_BLUE = (0, 50, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Função para carregar configurações do arquivo .env
def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {'environment': 'production'}  # Valor padrão
    
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        # Se o arquivo .env não existir, usar valores padrão
        pass
    except Exception as e:
        print(f"Erro ao carregar .env: {e}")
    
    return config

# Carregar configurações
ENV_CONFIG = load_env_config()

class RankingManager:
    def __init__(self):
        self.records_dir = "records"
        self.ranking_file = os.path.join(self.records_dir, "top10.log")
        self.rankings = []
        self.ensure_records_dir()
        self.load_rankings()
    
    def ensure_records_dir(self):
        """Cria o diretório records se não existir"""
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)
    
    def load_rankings(self):
        """Carrega os rankings do arquivo"""
        try:
            if os.path.exists(self.ranking_file):
                with open(self.ranking_file, 'r', encoding='utf-8') as f:
                    self.rankings = json.load(f)
            else:
                self.rankings = []
        except (json.JSONDecodeError, FileNotFoundError):
            self.rankings = []
    
    def save_rankings(self):
        """Salva os rankings no arquivo"""
        try:
            with open(self.ranking_file, 'w', encoding='utf-8') as f:
                json.dump(self.rankings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar rankings: {e}")
    
    def is_high_score(self, score):
        """Verifica se a pontuação entra no top 10"""
        if len(self.rankings) < 10:
            return True
        return score > self.rankings[-1]['score']
    
    def add_score(self, name, score):
        """Adiciona uma nova pontuação ao ranking"""
        # Limitar nome a 25 caracteres
        name = name[:25] if len(name) > 25 else name
        
        # Adicionar nova pontuação
        self.rankings.append({'name': name, 'score': score})
        
        # Ordenar por pontuação (maior para menor)
        self.rankings.sort(key=lambda x: x['score'], reverse=True)
        
        # Manter apenas top 10
        self.rankings = self.rankings[:10]
        
        # Salvar no arquivo
        self.save_rankings()
    
    def get_rankings(self):
        """Retorna a lista de rankings"""
        return self.rankings.copy()

class GameState(Enum):
    SPLASH = 1  # Tela de splash com logos
    MAIN_MENU = 2  # Menu principal
    PLAYING = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5
    VICTORY = 6  # Nova tela de vitória com troféu
    ENTER_NAME = 7  # Estado para inserir nome no ranking
    SHOW_RANKING = 8  # Estado para mostrar ranking
    CREDITS = 9  # Tela de créditos
    RECORDS = 10  # Tela de recordes

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 65
        self.original_height = 95
        self.crouched_height = 47
        self.height = self.original_height
        self.vel_x = 0
        self.vel_y = 0
        self.prev_vel_y = 0  # Velocidade anterior para detectar mudança
        self.on_ground = False
        self.just_landed = False  # Flag para detectar pouso
        self.is_crouching = False
        self.is_hit = False  # Flag para quando o personagem é atingido
        self.hit_timer = 0  # Timer para controlar duração do estado de hit
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Sistema de animação
        self.sprites = {}
        self.current_animation = 'idle'
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # Frames por segundo da animação
        
        # Sistema de tiro
        self.bullets = []
        self.shoot_cooldown = 0  # Cooldown entre tiros
        self.max_shoot_cooldown = 15  # 15 frames = 0.25 segundos a 60 FPS
        
        self.load_sprites()
        
    def load_sprites(self):
        """Carregar todos os sprites do personagem"""
        try:
            # Sprite parado (idle)
            self.sprites['idle'] = [pygame.image.load("imagens/personagem/1.png")]
            
            # Sprites de caminhada
            self.sprites['walk'] = [
                pygame.image.load("imagens/personagem/1.png"),
                pygame.image.load("imagens/personagem/2.png"),
                pygame.image.load("imagens/personagem/3.png"),
                pygame.image.load("imagens/personagem/4.png")
            ]
            
            # Sprites de pulo
            self.sprites['jump'] = [
                pygame.image.load("imagens/personagem/j1.png"),
                pygame.image.load("imagens/personagem/j2.png"),
                pygame.image.load("imagens/personagem/j3.png"),
                pygame.image.load("imagens/personagem/j4.png"),
                pygame.image.load("imagens/personagem/j5.png")  # Aterrissagem
            ]
            
            # Sprite agachado
            self.sprites['crouch'] = [pygame.image.load("imagens/personagem/dn1.png")]
            
            # Sprite quando atingido
            self.sprites['hit'] = [pygame.image.load("imagens/personagem/d1.png")]
            
            # Redimensionar todos os sprites para o tamanho do personagem
            for animation in self.sprites:
                for i, sprite in enumerate(self.sprites[animation]):
                    self.sprites[animation][i] = pygame.transform.scale(sprite, (self.width, self.original_height))
                    
        except pygame.error as e:
            print(f"Erro ao carregar sprites do personagem: {e}")
            # Fallback: criar sprites coloridos simples
            self.sprites = {
                'idle': [pygame.Surface((self.width, self.original_height))],
                'walk': [pygame.Surface((self.width, self.original_height)) for _ in range(4)],
                'jump': [pygame.Surface((self.width, self.original_height)) for _ in range(5)],
                'crouch': [pygame.Surface((self.width, self.crouched_height))],
                'hit': [pygame.Surface((self.width, self.original_height))]
            }
            # Preencher com cores para fallback
            for animation in self.sprites:
                for sprite in self.sprites[animation]:
                    sprite.fill(BLUE)
                    
    def update_animation(self):
        """Atualizar a animação do personagem baseada no estado atual"""
        # Determinar qual animação usar
        if self.is_hit and self.hit_timer > 0:
            new_animation = 'hit'
        elif self.is_crouching:
            new_animation = 'crouch'
        elif not self.on_ground:
            new_animation = 'jump'
        elif abs(self.vel_x) > 0:
            new_animation = 'walk'
        else:
            new_animation = 'idle'
            
        # Se mudou de animação, resetar frame
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.animation_frame = 0
            self.animation_timer = 0
            
        # Atualizar timer da animação
        self.animation_timer += 1
        
        # Avançar frame da animação
        if self.animation_timer >= 60 // self.animation_speed:  # 60 FPS / animation_speed
            self.animation_timer = 0
            
            # Lógica especial para animação de pulo
            if self.current_animation == 'jump':
                if self.vel_y < -10:  # Subindo rápido
                    self.animation_frame = 0
                elif self.vel_y < -5:  # Subindo devagar
                    self.animation_frame = 1
                elif self.vel_y < 5:   # No ar
                    self.animation_frame = 2
                elif self.vel_y < 10:  # Descendo
                    self.animation_frame = 3
                else:  # Aterrissando
                    self.animation_frame = 4
            else:
                # Para outras animações, ciclar normalmente
                self.animation_frame = (self.animation_frame + 1) % len(self.sprites[self.current_animation])
                
        # Atualizar timer de hit
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.is_hit = False
                
    def take_hit(self):
        """Método para quando o personagem é atingido"""
        self.is_hit = True
        self.hit_timer = 30  # 30 frames = 0.5 segundos a 60 FPS
        
    def shoot(self, bullet_image=None):
        """Criar um novo tiro"""
        if self.shoot_cooldown <= 0:
            # Determinar direção do tiro baseado no movimento
            direction = 1 if self.vel_x >= 0 else -1
            
            # Posição do tiro (centro do personagem)
            bullet_x = self.x + self.width // 2
            bullet_y = self.y + self.height // 2
            
            # Criar tiro
            bullet = Bullet(bullet_x, bullet_y, direction, bullet_image)
            self.bullets.append(bullet)
            
            # Resetar cooldown
            self.shoot_cooldown = self.max_shoot_cooldown
        
    def update(self, platforms, bullet_image=None, camera_x=0, joystick=None):
        # Aplicar gravidade
        self.vel_y += GRAVITY
        
        # Movimento horizontal
        keys = pygame.key.get_pressed()
        joystick_x = 0
        
        # Verificar entrada do joystick
        if joystick and joystick.get_numaxes() >= 1:
            joystick_x = joystick.get_axis(0)  # Eixo X do analógico esquerdo
            # Aplicar zona morta para evitar drift
            if abs(joystick_x) < 0.1:
                joystick_x = 0
        
        # Movimento com teclado ou joystick
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or joystick_x < -0.1:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d] or joystick_x > 0.1:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0
            
        # Sistema de agachamento
        joystick_y = 0
        joystick_crouch = False
        
        # Verificar entrada do joystick para agachamento
        if joystick and joystick.get_numaxes() >= 2:
            joystick_y = joystick.get_axis(1)  # Eixo Y do analógico esquerdo
            if joystick_y > 0.5:  # Analógico para baixo
                joystick_crouch = True
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or joystick_crouch:
            if not self.is_crouching and self.on_ground:
                # Começar a agachar
                old_y = self.y
                self.height = self.crouched_height
                self.y = old_y + (self.original_height - self.crouched_height)
                self.is_crouching = True
        else:
            if self.is_crouching:
                # Parar de agachar
                old_y = self.y
                self.height = self.original_height
                self.y = old_y - (self.original_height - self.crouched_height)
                self.is_crouching = False
            
        # Tiro com barra de espaço ou botão do joystick
        joystick_shoot = False
        if joystick and joystick.get_numbuttons() > 1:
            joystick_shoot = joystick.get_button(1)  # Botão B/Círculo para tiro
            
        if keys[pygame.K_SPACE] or joystick_shoot:
            self.shoot(bullet_image)
            
        # Pulo com setas/WASD ou botão/analógico do joystick
        joystick_jump = False
        if joystick:
            # Botão A/X para pulo
            if joystick.get_numbuttons() > 0:
                joystick_jump = joystick.get_button(0)
            # Ou analógico para cima
            if joystick.get_numaxes() >= 2 and joystick_y < -0.5:
                joystick_jump = True
                
        if ((keys[pygame.K_UP] or keys[pygame.K_w]) or joystick_jump) and self.on_ground and not self.is_crouching:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        
        # Atualizar posição
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Limitar movimento horizontal apenas no lado esquerdo
        if self.x < 0:
            self.x = 0
            
        # Verificar se caiu da tela
        if self.y > HEIGHT:
            return False  # Game over
            
        # Atualizar rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Verificar colisões com plataformas
        self.prev_vel_y = self.vel_y  # Salvar velocidade anterior
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Colisão por cima (jogador pousando na plataforma) - com tolerância de 3px
                if self.vel_y > 0 and self.y <= platform.y + 3:
                    self.y = platform.y - self.height
                    # Detectar se acabou de pousar (estava caindo e agora parou)
                    if self.prev_vel_y > 0:
                        self.just_landed = True
                        self.landed_platform_id = platform.id
                    self.vel_y = 0
                    self.on_ground = True
                    self.rect.y = self.y
                    
        # Atualizar tiros e remover os que saíram da área visível
        for bullet in self.bullets[:]:
            bullet.update()
            # Remover tiro se saiu muito da área visível da câmera
            if bullet.x < camera_x - 300 or bullet.x > camera_x + WIDTH + 300:
                self.bullets.remove(bullet)
        
        # Atualizar cooldown de tiro
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
                    
        # Atualizar animação
        self.update_animation()
                    
        return True
    
    def draw(self, screen):
        # Desenhar o sprite atual do personagem
        if self.current_animation in self.sprites and self.sprites[self.current_animation]:
            current_sprite = self.sprites[self.current_animation][self.animation_frame]
            
            # Ajustar posição Y para sprites agachados (sem redimensionar)
            draw_y = self.y
            if self.current_animation == 'crouch':
                # Ajustar posição Y para que o sprite apareça na posição correta
                # quando agachado (sprite mantém tamanho original)
                draw_y = self.y + (self.height - current_sprite.get_height())
            
            screen.blit(current_sprite, (self.x, draw_y))
        else:
            # Fallback: desenhar retângulo colorido
            color = RED if self.is_hit else BLUE
            pygame.draw.rect(screen, color, self.rect)
            
        # Tiros são desenhados no método draw da classe Game com offset da câmera

class Platform:
    _id_counter = 0  # Contador de ID para plataformas
    
    def __init__(self, x, y, width, height, texture=None):
        Platform._id_counter += 1
        self.id = Platform._id_counter
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.texture = texture
        
    def draw(self, screen):
        if self.texture:
            # Obter dimensões da textura original
            texture_width = self.texture.get_width()
            texture_height = self.texture.get_height()
            
            # Calcular quantas repetições cabem na plataforma
            tiles_x = self.width // texture_width
            tiles_y = self.height // texture_height
            
            # Desenhar os azulejos completos
            for row in range(tiles_y):
                for col in range(tiles_x):
                    x_pos = self.x + (col * texture_width)
                    y_pos = self.y + (row * texture_height)
                    screen.blit(self.texture, (x_pos, y_pos))
            
            # Desenhar azulejos parciais nas bordas direita e inferior
            remainder_x = self.width % texture_width
            remainder_y = self.height % texture_height
            
            # Borda direita
            if remainder_x > 0:
                for row in range(tiles_y):
                    x_pos = self.x + (tiles_x * texture_width)
                    y_pos = self.y + (row * texture_height)
                    partial_texture = self.texture.subsurface(0, 0, remainder_x, texture_height)
                    screen.blit(partial_texture, (x_pos, y_pos))
            
            # Borda inferior
            if remainder_y > 0:
                for col in range(tiles_x):
                    x_pos = self.x + (col * texture_width)
                    y_pos = self.y + (tiles_y * texture_height)
                    partial_texture = self.texture.subsurface(0, 0, texture_width, remainder_y)
                    screen.blit(partial_texture, (x_pos, y_pos))
            
            # Canto inferior direito
            if remainder_x > 0 and remainder_y > 0:
                x_pos = self.x + (tiles_x * texture_width)
                y_pos = self.y + (tiles_y * texture_height)
                corner_texture = self.texture.subsurface(0, 0, remainder_x, remainder_y)
                screen.blit(corner_texture, (x_pos, y_pos))
        else:
            # Fallback para cor sólida
            pygame.draw.rect(screen, BROWN, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.flag_width = 60
        self.flag_height = 40
        self.rect = pygame.Rect(x, y, self.width + self.flag_width, self.height)
        
        # Carregar imagem da bandeira
        try:
            self.flag_image = pygame.image.load("imagens/elementos/bandeira.png")
            # Redimensionar para ocupar toda a área (mastro + bandeira)
            total_width = self.width + self.flag_width
            self.flag_image = pygame.transform.scale(self.flag_image, (total_width, self.height))
        except pygame.error:
            self.flag_image = None
        
    def draw(self, screen):
        # Desenhar bandeira completa (imagem ou fallback)
        if self.flag_image:
            # A imagem substitui completamente mastro e bandeira
            screen.blit(self.flag_image, (self.x, self.y))
        else:
            # Fallback para desenho original completo
            # Desenhar mastro
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
            # Desenhar bandeira
            flag_rect = pygame.Rect(self.x + self.width, self.y, self.flag_width, self.flag_height)
            pygame.draw.rect(screen, RED, flag_rect)
            pygame.draw.polygon(screen, RED, [(self.x + self.width + self.flag_width, self.y),
                                             (self.x + self.width + self.flag_width + 20, self.y + self.flag_height//2),
                                             (self.x + self.width + self.flag_width, self.y + self.flag_height)])

class Bird:
    _id_counter = 0  # Contador de ID para pássaros
    
    def __init__(self, x, y, bird_images=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 3
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # Atribuir ID único
        Bird._id_counter += 1
        self.id = Bird._id_counter
        # Animação
        self.bird_images = bird_images  # Tupla com (bird_img1, bird_img2)
        self.animation_frame = 0
        self.animation_speed = 10  # Frames para trocar de imagem
        
    def update(self):
        # Mover pássaro da direita para a esquerda
        self.x -= self.speed
        self.rect.x = self.x
        
        # Atualizar animação
        self.animation_frame += 1
        
        # Retornar True se ainda está na tela, False se saiu
        return self.x + self.width > 0
        
    def draw(self, screen):
        if self.bird_images and self.bird_images[0] and self.bird_images[1]:
            # Usar animação com as imagens carregadas
            current_image_index = (self.animation_frame // self.animation_speed) % 2
            current_image = self.bird_images[current_image_index]
            screen.blit(current_image, (self.x, self.y))
        else:
            # Fallback para o desenho original se as imagens não carregaram
            pygame.draw.ellipse(screen, BROWN, self.rect)
            # Adicionar detalhes simples (asas)
            wing_y = self.y + 5
            pygame.draw.ellipse(screen, BLACK, (self.x + 5, wing_y, 8, 4))
            pygame.draw.ellipse(screen, BLACK, (self.x + 17, wing_y, 8, 4))
            # Bico
            pygame.draw.polygon(screen, YELLOW, [(self.x, self.y + 8), (self.x - 5, self.y + 10), (self.x, self.y + 12)])

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
        self.direction = -1  # -1 para esquerda, 1 para direita (começa indo para esquerda)
        
        # Atribuir ID único
        Turtle._id_counter += 1
        self.id = Turtle._id_counter
        
        # Animação
        self.turtle_images = turtle_images  # Dicionário com left e right arrays
        self.animation_frame = 0
        self.animation_speed = 15  # Frames para trocar de imagem (mais lento que pássaro)
        
    def update(self):
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
        
        return True  # Tartaruga sempre permanece ativa
        
    def draw(self, screen):
        if self.turtle_images and 'left' in self.turtle_images and 'right' in self.turtle_images:
            # Usar animação com as imagens carregadas
            current_images = self.turtle_images['left'] if self.direction == -1 else self.turtle_images['right']
            if current_images and len(current_images) > 0:
                current_image_index = (self.animation_frame // self.animation_speed) % len(current_images)
                current_image = current_images[current_image_index]
                if current_image:
                    screen.blit(current_image, (self.x, self.y))
                    return
        
        # Fallback para o desenho original se as imagens não carregaram
        pygame.draw.ellipse(screen, (34, 139, 34), self.rect)  # Verde escuro para tartaruga
        # Adicionar detalhes simples (cabeça)
        head_x = self.x + (5 if self.direction == 1 else self.width - 15)
        pygame.draw.circle(screen, (0, 100, 0), (head_x, self.y + 10), 8)
        # Patas
        pygame.draw.circle(screen, (0, 80, 0), (self.x + 8, self.y + 20), 4)
        pygame.draw.circle(screen, (0, 80, 0), (self.x + self.width - 8, self.y + 20), 4)

class Bullet:
    def __init__(self, x, y, direction=1, image=None):
        self.x = x
        self.y = y
        self.width = 15 if image else 10
        self.height = 8 if image else 5
        self.speed = 8
        self.direction = direction  # 1 para direita, -1 para esquerda
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = image
        
    def update(self):
        """Atualizar posição do tiro"""
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Manter tiro ativo (remoção será feita no método update do Player)
        return True
        
    def draw(self, screen):
        """Desenhar o tiro"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Fallback: desenhar retângulo amarelo
            pygame.draw.rect(screen, YELLOW, self.rect)

class Explosion:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.timer = 30  # Duração da explosão em frames (0.5 segundos a 60 FPS)
        self.image = image
        
    def update(self):
        """Atualizar explosão"""
        self.timer -= 1
        return self.timer > 0
        
    def draw(self, screen):
        """Desenhar explosão"""
        if self.timer > 0:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                # Fallback: desenhar círculo vermelho piscando
                if self.timer % 6 < 3:  # Piscar
                    pygame.draw.circle(screen, RED, (self.x + self.width//2, self.y + self.height//2), self.width//2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jogo de Plataforma - Mar")
        self.clock = pygame.time.Clock()
        self.state = GameState.SPLASH
        
        # Configurar nível inicial baseado no ambiente
        if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG:
            try:
                self.current_level = int(ENV_CONFIG['initial-stage'])
                # Validar se o nível está dentro do range válido
                if self.current_level < 1 or self.current_level > 20:
                    print(f"Aviso: initial-stage {self.current_level} inválido. Usando nível 1.")
                    self.current_level = 1
                else:
                    print(f"Modo desenvolvimento: Iniciando no nível {self.current_level}")
            except (ValueError, TypeError):
                print("Aviso: initial-stage deve ser um número. Usando nível 1.")
                self.current_level = 1
        else:
            self.current_level = 1
        
        # Sistema de ranking
        self.ranking_manager = RankingManager()
        self.player_name = ""
        self.name_input_active = False
        self.max_levels = 20
        
        # Sistema de música - configuração otimizada para Windows
        try:
            pygame.mixer.quit()  # Garantir que não há instância anterior
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Erro ao inicializar mixer: {e}")
            # Fallback para inicialização padrão
            pygame.mixer.init()
        
        self.current_music = None
        self.music_volume = 0.7
        
        # Volumes individuais para cada música (equalização)
        self.music_volumes = {
            'intro': 0.6,  # Música do menu - geralmente mais alta
            'musicas/fundo1.mp3': 0.7,  # Volume padrão
            'musicas/fundo2.mp3': 0.8,  # Geralmente mais baixa
            'musicas/fundo3.mp3': 0.7,  # Volume padrão
            'musicas/fundo4.mp3': 0.6   # Geralmente mais alta
        }
        
        self.load_music()
        
        # Sistema de câmera
        self.camera_x = 0
        
        # Sistema de pontuação
        self.score = 0
        self.platforms_jumped = set()  # Conjunto para rastrear IDs de plataformas já pontuadas
        self.birds_dodged = set()  # Para rastrear pássaros já esquivados
        
        # Sistema de vidas
        self.lives = 3
        self.max_lives = 3
        

        
        # Sistema de joystick
        pygame.joystick.init()
        self.joystick = None
        self.joystick_connected = False
        
        # Verificar se há joystick conectado
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.joystick_connected = True
            print(f"Joystick conectado: {self.joystick.get_name()}")
        else:
            print("Nenhum joystick detectado. Usando controles do teclado.")
        
        # Sistema de splash screen e menu
        self.splash_timer = 0
        self.splash_duration = 360  # 6 segundos (60 FPS * 6)
        self.current_logo_index = 0
        self.logo_display_time = 120  # Tempo para cada logo (2 segundos)
        self.logos = []  # Lista de logos para splash
        self.menu_selected = 0  # Opção selecionada no menu
        self.menu_options = ['Iniciar', 'Recordes', 'Créditos', 'Sair']
        self.game_logo = None  # Logo principal do jogo
        
        # Efeitos de fade para splash screen
        self.fade_in_duration = 30  # 0.5 segundos para fade in
        self.fade_out_duration = 30  # 0.5 segundos para fade out
        self.logo_hold_time = 60   # 1 segundo para mostrar o logo
        self.music_started = False  # Controla se a música já foi iniciada
        
        # Controle de eixos do joystick para D-pad e analógicos
        self.prev_dpad_vertical = 0
        self.prev_dpad_horizontal = 0
        self.prev_analog_vertical = 0
        self.prev_analog_horizontal = 0
        
        # Sistema de menu de game over
        self.game_over_selected = 0  # Opção selecionada no menu de game over
        self.game_over_options = ['Jogar novamente', 'Recordes', 'Sair']
        
        # Variável para rastrear de onde veio o SHOW_RANKING
        self.previous_state_before_ranking = None
        
        # Variável para rastrear de onde veio o RECORDS
        self.previous_state_before_records = None
        
        # Sistema de pássaros
        self.birds = []
        
        # Sistema de tartarugas
        self.turtles = []
        
        # Sistema de explosões
        self.explosions = []
        self.bird_spawn_timer = 0
        
        # Ajustar dificuldade baseada no nível
        if self.current_level <= 5:
            # Níveis 1-5 (originais)
            if self.current_level == 1:
                self.birds_per_spawn = 1
                self.bird_spawn_interval = 180  # 3 segundos
            elif self.current_level == 2:
                self.birds_per_spawn = 2
                self.bird_spawn_interval = 150  # 2.5 segundos
            elif self.current_level == 3:
                self.birds_per_spawn = 2
                self.bird_spawn_interval = 120  # 2 segundos
            elif self.current_level == 4:
                self.birds_per_spawn = 3
                self.bird_spawn_interval = 100  # 1.67 segundos
            elif self.current_level == 5:
                self.birds_per_spawn = 3
                self.bird_spawn_interval = 80   # 1.33 segundos
        elif self.current_level <= 10:
            # Níveis 6-10
            self.birds_per_spawn = 3 + (self.current_level - 5)  # 4-8 pássaros
            self.bird_spawn_interval = max(60, 80 - (self.current_level - 5) * 4)  # 76-60 segundos
        else:
            # Níveis 11-20
            self.birds_per_spawn = 2 + (self.current_level - 10)  # 3-12 pássaros
            self.bird_spawn_interval = max(40, 150 - (self.current_level - 10) * 11)  # 139-40 segundos
        
        # Fonte para texto
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Carregar imagens
        self.load_images()
        
        # Se estiver em modo desenvolvimento e iniciando em uma fase específica,
        # pular para o estado PLAYING e tocar música do nível
        if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG and self.current_level > 1:
            self.state = GameState.PLAYING
            self.score = 0
            self.platforms_jumped = set()
            self.birds_dodged = set()
            self.lives = self.max_lives
            self.player_name = ""
            self.init_level()
            self.play_level_music(self.current_level)
        else:
            self.init_level()
        
    def load_images(self):
        """Carregar todas as imagens do jogo"""
        try:
            # Carregar fundo
            self.background_img = pygame.image.load("imagens/fundo6.png")
            self.background_img = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))
            
            # Carregar textura de plataforma 20x20px para ladrilhamento perfeito
            original_texture = pygame.image.load("imagens/texturas/platform2.png")
            self.platform_texture = pygame.transform.scale(original_texture, (20, 20))
            
            # Carregar imagens dos pássaros para animação
            self.bird_img1 = pygame.image.load("imagens/inimigos/bird1.png")
            self.bird_img2 = pygame.image.load("imagens/inimigos/bird2.png")
            # Redimensionar para manter o tamanho atual dos pássaros (30x20)
            self.bird_img1 = pygame.transform.scale(self.bird_img1, (40, 30))
            self.bird_img2 = pygame.transform.scale(self.bird_img2, (40, 30))
            
            # Carregar imagens das tartarugas para animação
            try:
                self.turtle_left1 = pygame.image.load("imagens/inimigos/turtle-left1.png")
                self.turtle_left2 = pygame.image.load("imagens/inimigos/turtle-left2.png")
                self.turtle_left3 = pygame.image.load("imagens/inimigos/turtle-left3.png")
                self.turtle_right1 = pygame.image.load("imagens/inimigos/turtle-right1.png")
                self.turtle_right2 = pygame.image.load("imagens/inimigos/turtle-right2.png")
                self.turtle_right3 = pygame.image.load("imagens/inimigos/turtle-right3.png")
                
                # Redimensionar para manter o tamanho das tartarugas (40x30)
                self.turtle_left1 = pygame.transform.scale(self.turtle_left1, (40, 30))
                self.turtle_left2 = pygame.transform.scale(self.turtle_left2, (40, 30))
                self.turtle_left3 = pygame.transform.scale(self.turtle_left3, (40, 30))
                self.turtle_right1 = pygame.transform.scale(self.turtle_right1, (40, 30))
                self.turtle_right2 = pygame.transform.scale(self.turtle_right2, (40, 30))
                self.turtle_right3 = pygame.transform.scale(self.turtle_right3, (40, 30))
                
                # Organizar imagens em dicionário para facilitar o uso
                self.turtle_images = {
                    'left': [self.turtle_left1, self.turtle_left2, self.turtle_left3],
                    'right': [self.turtle_right1, self.turtle_right2, self.turtle_right3]
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens das tartarugas: {e}")
                self.turtle_images = None
            
            # Carregar imagem do tiro
            self.bullet_img = pygame.image.load("imagens/elementos/tiro.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (15, 8))
            self.bullet_image = self.bullet_img  # Alias para compatibilidade
            
            # Carregar imagem da explosão
            self.explosion_img = pygame.image.load("imagens/elementos/explosao.png")
            self.explosion_img = pygame.transform.scale(self.explosion_img, (40, 40))
            self.explosion_image = self.explosion_img  # Alias para compatibilidade
            
            # Carregar logos para splash screen (exceto game.png)
            logo_files = ['cirrastec.png', 'cirrasretrogames.png', 'canaldodudu.png']
            self.logos = []
            for logo_file in logo_files:
                try:
                    logo_path = f"imagens/logos/{logo_file}"
                    logo_img = pygame.image.load(logo_path)
                    # Redimensionar logos para caber na tela (máximo 400x300)
                    logo_rect = logo_img.get_rect()
                    if logo_rect.width > 400 or logo_rect.height > 300:
                        scale_factor = min(400/logo_rect.width, 300/logo_rect.height)
                        new_width = int(logo_rect.width * scale_factor)
                        new_height = int(logo_rect.height * scale_factor)
                        logo_img = pygame.transform.scale(logo_img, (new_width, new_height))
                    self.logos.append(logo_img)
                except pygame.error:
                    print(f"Erro ao carregar logo: {logo_file}")
            
            # Carregar logo principal do jogo
            try:
                self.game_logo = pygame.image.load("imagens/logos/game.png")
                # Redimensionar logo do jogo para o menu
                logo_rect = self.game_logo.get_rect()
                if logo_rect.width > 300 or logo_rect.height > 200:
                    scale_factor = min(300/logo_rect.width, 200/logo_rect.height)
                    new_width = int(logo_rect.width * scale_factor)
                    new_height = int(logo_rect.height * scale_factor)
                    self.game_logo = pygame.transform.scale(self.game_logo, (new_width, new_height))
            except pygame.error:
                print("Erro ao carregar logo do jogo")
                self.game_logo = None
            
        except pygame.error as e:
            print(f"Erro ao carregar imagens: {e}")
            # Fallback para cores sólidas se as imagens não carregarem
            self.background_img = None
            self.platform_texture = None
            self.bird_img1 = None
            self.bird_img2 = None
            self.bullet_img = None
            self.bullet_image = None
            self.explosion_img = None
            self.explosion_image = None
    
    def load_music(self):
        """Carregar todas as músicas do jogo"""
        self.music_files = {
            'intro': "musicas/intro.mp3",  # Música do menu
            1: "musicas/fundo1.mp3",  # Primeira fase
            2: "musicas/fundo2.mp3",  # Segunda fase
            3: "musicas/fundo1.mp3",  # Terceira fase (também fundo1)
        }
        
        # Criar rodízio para fases 4-20 usando fundo2, fundo3 e fundo4
        background_music = ["musicas/fundo2.mp3", "musicas/fundo3.mp3", "musicas/fundo4.mp3"]
        for level in range(4, 21):  # Fases 4 a 20
            # Usar módulo para criar rodízio: fase 4 = índice 0, fase 5 = índice 1, etc.
            music_index = (level - 4) % len(background_music)
            self.music_files[level] = background_music[music_index]
        
        # Verificar se os arquivos de música existem
        for level, music_file in self.music_files.items():
            if not os.path.exists(music_file):
                print(f"Aviso: Arquivo de música não encontrado: {music_file}")
    
    def play_menu_music(self):
        """Tocar a música do menu"""
        music_file = self.music_files['intro']
        if os.path.exists(music_file):
            try:
                # Parar música atual se estiver tocando
                pygame.mixer.music.stop()
                
                # Carregar e tocar música do menu
                pygame.mixer.music.load(music_file)
                # Usar volume específico para a música do menu
                volume = self.music_volumes.get('intro', self.music_volume)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)  # -1 para loop infinito
                self.current_music = music_file
                print(f"Tocando música do menu: {music_file} (volume: {volume})")
            except pygame.error as e:
                print(f"Erro ao carregar música do menu {music_file}: {e}")
        else:
            print(f"Arquivo de música do menu não encontrado: {music_file}")
    
    def play_level_music(self, level):
        """Tocar a música correspondente ao nível"""
        if level in self.music_files:
            music_file = self.music_files[level]
            if os.path.exists(music_file):
                try:
                    # Parar música atual se estiver tocando
                    pygame.mixer.music.stop()
                    
                    # Carregar e tocar nova música
                    pygame.mixer.music.load(music_file)
                    # Usar volume específico para esta música
                    volume = self.music_volumes.get(music_file, self.music_volume)
                    pygame.mixer.music.set_volume(volume)
                    pygame.mixer.music.play(-1)  # -1 para loop infinito
                    self.current_music = music_file
                    print(f"Tocando música do nível {level}: {music_file} (volume: {volume})")
                except pygame.error as e:
                    print(f"Erro ao carregar música {music_file}: {e}")
            else:
                print(f"Arquivo de música não encontrado: {music_file}")
        
    def init_level(self):
        """Inicializar o nível atual"""
        self.player = Player(50, HEIGHT - 200)
        self.platforms = []
        self.flag = None
        self.camera_x = 0
        # Reinicializar sistema de pássaros
        self.birds = []
        self.bird_spawn_timer = 0
        # Reinicializar sistema de tartarugas
        self.turtles = []
        # Reinicializar explosões
        self.explosions = []
        # Não resetar platforms_jumped aqui para manter pontuação entre níveis
        
        # Criar plataformas baseadas no nível
        if self.current_level == 1:
            self.create_level_1()
        elif self.current_level == 2:
            self.create_level_2()
        elif self.current_level == 3:
            self.create_level_3()
        elif self.current_level == 4:
            self.create_level_4()
        elif self.current_level == 5:
            self.create_level_5()
        elif self.current_level == 6:
            self.create_level_6()
        elif self.current_level == 7:
            self.create_level_7()
        elif self.current_level == 8:
            self.create_level_8()
        elif self.current_level == 9:
            self.create_level_9()
        elif self.current_level == 10:
            self.create_level_10()
        elif self.current_level == 11:
            self.create_level_11()
        elif self.current_level == 12:
            self.create_level_12()
        elif self.current_level == 13:
            self.create_level_13()
        elif self.current_level == 14:
            self.create_level_14()
        elif self.current_level == 15:
            self.create_level_15()
        elif self.current_level == 16:
            self.create_level_16()
        elif self.current_level == 17:
            self.create_level_17()
        elif self.current_level == 18:
            self.create_level_18()
        elif self.current_level == 19:
            self.create_level_19()
        elif self.current_level == 20:
            self.create_level_20()
            
    def create_level_1(self):
        """Nível 1 - Fácil (20 plataformas)"""
        platforms = [
            (100, HEIGHT - 150, 120, 20), (300, HEIGHT - 200, 120, 20), (500, HEIGHT - 120, 120, 20),
            (700, HEIGHT - 180, 120, 20), (900, HEIGHT - 100, 120, 20), (1100, HEIGHT - 160, 120, 20),
            (1300, HEIGHT - 220, 120, 20), (1500, HEIGHT - 140, 120, 20), (1700, HEIGHT - 190, 120, 20),
            (1900, HEIGHT - 110, 120, 20), (2100, HEIGHT - 170, 120, 20), (2300, HEIGHT - 230, 120, 20),
            (2500, HEIGHT - 130, 120, 20), (2700, HEIGHT - 200, 120, 20), (2900, HEIGHT - 150, 120, 20),
            (3100, HEIGHT - 180, 120, 20), (3300, HEIGHT - 120, 120, 20), (3500, HEIGHT - 210, 120, 20),
            (3700, HEIGHT - 160, 120, 20), (3900, HEIGHT - 140, 120, 20)
        ]
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        self.platforms.append(Platform(4080, HEIGHT - 100, 120, 20, self.platform_texture))
        self.flag = Flag(4100, HEIGHT - 200)
        
    def create_level_2(self):
        """Nível 2 - Médio (30 plataformas)"""
        platforms = [
            (120, HEIGHT - 180, 100, 20), (280, HEIGHT - 250, 100, 20), (440, HEIGHT - 150, 100, 20),
            (600, HEIGHT - 300, 100, 20), (760, HEIGHT - 200, 100, 20), (920, HEIGHT - 120, 100, 20),
            (1080, HEIGHT - 280, 100, 20), (1240, HEIGHT - 160, 100, 20), (1400, HEIGHT - 320, 100, 20),
            (1560, HEIGHT - 180, 100, 20), (1720, HEIGHT - 240, 100, 20), (1880, HEIGHT - 140, 100, 20),
            (2040, HEIGHT - 300, 100, 20), (2200, HEIGHT - 200, 100, 20), (2360, HEIGHT - 120, 100, 20),
            (2520, HEIGHT - 280, 100, 20), (2680, HEIGHT - 160, 100, 20), (2840, HEIGHT - 340, 100, 20),
            (3000, HEIGHT - 220, 100, 20), (3160, HEIGHT - 140, 100, 20), (3320, HEIGHT - 300, 100, 20),
            (3480, HEIGHT - 180, 100, 20), (3640, HEIGHT - 260, 100, 20), (3800, HEIGHT - 120, 100, 20),
            (3960, HEIGHT - 320, 100, 20), (4120, HEIGHT - 200, 100, 20), (4280, HEIGHT - 140, 100, 20),
            (4440, HEIGHT - 280, 100, 20), (4600, HEIGHT - 160, 100, 20), (4760, HEIGHT - 240, 100, 20)
        ]
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        self.platforms.append(Platform(4940, HEIGHT - 200, 100, 20, self.platform_texture))
        self.flag = Flag(4960, HEIGHT - 300)
        
    def create_level_3(self):
        """Nível 3 - Médio-Difícil (40 plataformas) - Corrigido para pulos possíveis"""
        platforms = [
            (100, HEIGHT - 200, 80, 20), (240, HEIGHT - 300, 80, 20), (380, HEIGHT - 180, 80, 20),
            (520, HEIGHT - 310, 80, 20), (660, HEIGHT - 220, 80, 20), (800, HEIGHT - 350, 80, 20),
            (940, HEIGHT - 150, 80, 20), (1080, HEIGHT - 280, 80, 20), (1220, HEIGHT - 180, 80, 20),
            (1360, HEIGHT - 310, 80, 20), (1500, HEIGHT - 240, 80, 20), (1640, HEIGHT - 140, 80, 20),
            (1780, HEIGHT - 270, 80, 20), (1920, HEIGHT - 200, 80, 20), (2060, HEIGHT - 330, 80, 20),
            (2200, HEIGHT - 160, 80, 20), (2340, HEIGHT - 290, 80, 20), (2480, HEIGHT - 220, 80, 20),
            (2620, HEIGHT - 120, 80, 20), (2760, HEIGHT - 250, 80, 20), (2900, HEIGHT - 180, 80, 20),
            (3040, HEIGHT - 310, 80, 20), (3180, HEIGHT - 240, 80, 20), (3320, HEIGHT - 140, 80, 20),
            (3460, HEIGHT - 270, 80, 20), (3600, HEIGHT - 200, 80, 20), (3740, HEIGHT - 330, 80, 20),
            (3880, HEIGHT - 160, 80, 20), (4020, HEIGHT - 290, 80, 20), (4160, HEIGHT - 220, 80, 20),
            (4300, HEIGHT - 120, 80, 20), (4440, HEIGHT - 250, 80, 20), (4580, HEIGHT - 180, 80, 20),
            (4720, HEIGHT - 310, 80, 20), (4860, HEIGHT - 240, 80, 20), (5000, HEIGHT - 140, 80, 20),
            (5140, HEIGHT - 270, 80, 20), (5280, HEIGHT - 200, 80, 20), (5420, HEIGHT - 330, 80, 20),
            (5560, HEIGHT - 280, 80, 20)
        ]
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        self.platforms.append(Platform(5740, HEIGHT - 240, 80, 20, self.platform_texture))
        self.flag = Flag(5760, HEIGHT - 340)
        
    def create_level_4(self):
        """Nível 4 - Difícil (50 plataformas)"""
        platforms = [
            (80, HEIGHT - 220, 70, 20), (200, HEIGHT - 350, 70, 20), (320, HEIGHT - 180, 70, 20),
            (440, HEIGHT - 400, 70, 20), (560, HEIGHT - 250, 70, 20), (680, HEIGHT - 450, 70, 20),
            (800, HEIGHT - 160, 70, 20), (920, HEIGHT - 380, 70, 20), (1040, HEIGHT - 200, 70, 20),
            (1160, HEIGHT - 420, 70, 20), (1280, HEIGHT - 280, 70, 20), (1400, HEIGHT - 140, 70, 20),
            (1520, HEIGHT - 360, 70, 20), (1640, HEIGHT - 220, 70, 20), (1760, HEIGHT - 480, 70, 20),
            (1880, HEIGHT - 160, 70, 20), (2000, HEIGHT - 340, 70, 20), (2120, HEIGHT - 240, 70, 20),
            (2240, HEIGHT - 120, 70, 20), (2360, HEIGHT - 400, 70, 20), (2480, HEIGHT - 180, 70, 20),
            (2600, HEIGHT - 460, 70, 20), (2720, HEIGHT - 260, 70, 20), (2840, HEIGHT - 140, 70, 20),
            (2960, HEIGHT - 380, 70, 20), (3080, HEIGHT - 200, 70, 20), (3200, HEIGHT - 500, 70, 20),
            (3320, HEIGHT - 160, 70, 20), (3440, HEIGHT - 320, 70, 20), (3560, HEIGHT - 240, 70, 20),
            (3680, HEIGHT - 120, 70, 20), (3800, HEIGHT - 420, 70, 20), (3920, HEIGHT - 180, 70, 20),
            (4040, HEIGHT - 480, 70, 20), (4160, HEIGHT - 280, 70, 20), (4280, HEIGHT - 140, 70, 20),
            (4400, HEIGHT - 360, 70, 20), (4520, HEIGHT - 220, 70, 20), (4640, HEIGHT - 520, 70, 20),
            (4760, HEIGHT - 160, 70, 20), (4880, HEIGHT - 340, 70, 20), (5000, HEIGHT - 260, 70, 20),
            (5120, HEIGHT - 120, 70, 20), (5240, HEIGHT - 400, 70, 20), (5360, HEIGHT - 200, 70, 20),
            (5480, HEIGHT - 500, 70, 20), (5600, HEIGHT - 280, 70, 20), (5720, HEIGHT - 140, 70, 20),
            (5840, HEIGHT - 380, 70, 20), (5960, HEIGHT - 240, 70, 20)
        ]
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        self.platforms.append(Platform(6140, HEIGHT - 200, 70, 20, self.platform_texture))
        self.flag = Flag(6160, HEIGHT - 300)
        
    def create_level_5(self):
        """Nível 5 - Muito Difícil (60 plataformas)"""
        platforms = [
            (60, HEIGHT - 250, 60, 20), (170, HEIGHT - 400, 60, 20), (280, HEIGHT - 180, 60, 20),
            (390, HEIGHT - 450, 60, 20), (500, HEIGHT - 280, 60, 20), (610, HEIGHT - 500, 60, 20),
            (720, HEIGHT - 160, 60, 20), (830, HEIGHT - 420, 60, 20), (940, HEIGHT - 240, 60, 20),
            (1050, HEIGHT - 480, 60, 20), (1160, HEIGHT - 200, 60, 20), (1270, HEIGHT - 380, 60, 20),
            (1380, HEIGHT - 140, 60, 20), (1490, HEIGHT - 460, 60, 20), (1600, HEIGHT - 260, 60, 20),
            (1710, HEIGHT - 520, 60, 20), (1820, HEIGHT - 180, 60, 20), (1930, HEIGHT - 340, 60, 20),
            (2040, HEIGHT - 220, 60, 20), (2150, HEIGHT - 500, 60, 20), (2260, HEIGHT - 160, 60, 20),
            (2370, HEIGHT - 400, 60, 20), (2480, HEIGHT - 280, 60, 20), (2590, HEIGHT - 540, 60, 20),
            (2700, HEIGHT - 200, 60, 20), (2810, HEIGHT - 360, 60, 20), (2920, HEIGHT - 240, 60, 20),
            (3030, HEIGHT - 480, 60, 20), (3140, HEIGHT - 140, 60, 20), (3250, HEIGHT - 420, 60, 20),
            (3360, HEIGHT - 300, 60, 20), (3470, HEIGHT - 560, 60, 20), (3580, HEIGHT - 180, 60, 20),
            (3690, HEIGHT - 340, 60, 20), (3800, HEIGHT - 260, 60, 20), (3910, HEIGHT - 500, 60, 20),
            (4020, HEIGHT - 160, 60, 20), (4130, HEIGHT - 380, 60, 20), (4240, HEIGHT - 220, 60, 20),
            (4350, HEIGHT - 520, 60, 20), (4460, HEIGHT - 280, 60, 20), (4570, HEIGHT - 140, 60, 20),
            (4680, HEIGHT - 400, 60, 20), (4790, HEIGHT - 240, 60, 20), (4900, HEIGHT - 540, 60, 20),
            (5010, HEIGHT - 180, 60, 20), (5120, HEIGHT - 360, 60, 20), (5230, HEIGHT - 300, 60, 20),
            (5340, HEIGHT - 480, 60, 20), (5450, HEIGHT - 160, 60, 20), (5560, HEIGHT - 420, 60, 20),
            (5670, HEIGHT - 260, 60, 20), (5780, HEIGHT - 520, 60, 20), (5890, HEIGHT - 200, 60, 20),
            (6000, HEIGHT - 380, 60, 20), (6110, HEIGHT - 240, 60, 20), (6220, HEIGHT - 500, 60, 20),
            (6330, HEIGHT - 180, 60, 20), (6440, HEIGHT - 340, 60, 20), (6550, HEIGHT - 280, 60, 20),
            (6660, HEIGHT - 460, 60, 20)
        ]
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        self.platforms.append(Platform(6840, HEIGHT - 240, 60, 20, self.platform_texture))
        self.flag = Flag(6860, HEIGHT - 340)
        
    def create_level_6(self):
        """Nível 6 - Progressão (29 plataformas)"""
        platforms = []
        x_pos = 60
        for i in range(29):
            y_pos = HEIGHT - (150 + (i % 8) * 50 + (i // 8) * 10)
            platforms.append((x_pos, y_pos, 55, 20))
            x_pos += 90 + (i % 3) * 20
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 200, 55, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 300)
        
    def create_level_7(self):
        """Nível 7 - Progressão (38 plataformas)"""
        platforms = []
        x_pos = 50
        for i in range(38):
            y_pos = HEIGHT - (140 + (i % 9) * 45 + (i // 9) * 15)
            platforms.append((x_pos, y_pos, 55, 20))
            x_pos += 95 + (i % 4) * 15
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 180, 55, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 280)
        
    def create_level_8(self):
        """Nível 8 - Progressão (47 plataformas)"""
        platforms = []
        x_pos = 40
        for i in range(47):
            y_pos = HEIGHT - (130 + (i % 10) * 40 + (i // 10) * 20)
            platforms.append((x_pos, y_pos, 50, 20))
            x_pos += 100 + (i % 5) * 10
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 160, 50, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 260)
        
    def create_level_9(self):
        """Nível 9 - Progressão (56 plataformas)"""
        platforms = []
        x_pos = 30
        for i in range(56):
            y_pos = HEIGHT - (120 + (i % 11) * 35 + (i // 11) * 25)
            platforms.append((x_pos, y_pos, 50, 20))
            x_pos += 105 + (i % 6) * 5
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 140, 50, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 240)
        
    def create_level_10(self):
        """Nível 10 - Progressão (100 plataformas)"""
        platforms = []
        x_pos = 20
        for i in range(100):
            y_pos = HEIGHT - (110 + (i % 12) * 30 + (i // 12) * 30)
            platforms.append((x_pos, y_pos, 45, 20))
            x_pos += 110 + (i % 7) * 0
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 120, 45, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 220)
        
    def create_level_11(self):
        """Nível 11 - Reinício com tartarugas (30 plataformas)"""
        platforms = []
        x_pos = 100
        for i in range(30):
            y_pos = HEIGHT - (200 + (i % 5) * 80 + (i // 5) * 20)
            platforms.append((x_pos, y_pos, 80, 20))
            x_pos += 120 + (i % 2) * 40
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 10 plataformas)
        for i in range(10, len(platforms), 10):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2], self.turtle_images)
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 200, 80, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 300)
        
    def create_level_12(self):
        """Nível 12 - Progressão com tartarugas (39 plataformas)"""
        platforms = []
        x_pos = 90
        for i in range(39):
            y_pos = HEIGHT - (190 + (i % 6) * 75 + (i // 6) * 25)
            platforms.append((x_pos, y_pos, 75, 20))
            x_pos += 115 + (i % 3) * 35
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 9 plataformas)
        for i in range(9, len(platforms), 9):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 190, 75, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 290)
        
    def create_level_13(self):
        """Nível 13 - Progressão com tartarugas (48 plataformas)"""
        platforms = []
        x_pos = 80
        for i in range(48):
            y_pos = HEIGHT - (180 + (i % 7) * 70 + (i // 7) * 30)
            platforms.append((x_pos, y_pos, 70, 20))
            x_pos += 110 + (i % 4) * 30
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 8 plataformas)
        for i in range(8, len(platforms), 8):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 180, 70, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 280)
        
    def create_level_14(self):
        """Nível 14 - Progressão com tartarugas (57 plataformas)"""
        platforms = []
        x_pos = 70
        for i in range(57):
            y_pos = HEIGHT - (170 + (i % 8) * 65 + (i // 8) * 35)
            platforms.append((x_pos, y_pos, 65, 20))
            x_pos += 105 + (i % 5) * 25
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 7 plataformas)
        for i in range(7, len(platforms), 7):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 170, 65, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 270)
        
    def create_level_15(self):
        """Nível 15 - Progressão com tartarugas (66 plataformas)"""
        platforms = []
        x_pos = 60
        for i in range(66):
            y_pos = HEIGHT - (160 + (i % 9) * 60 + (i // 9) * 40)
            platforms.append((x_pos, y_pos, 60, 20))
            x_pos += 100 + (i % 6) * 20
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 6 plataformas)
        for i in range(6, len(platforms), 6):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 160, 60, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 260)
        
    def create_level_16(self):
        """Nível 16 - Progressão com tartarugas (75 plataformas)"""
        platforms = []
        x_pos = 50
        for i in range(75):
            y_pos = HEIGHT - (150 + (i % 10) * 55 + (i // 10) * 45)
            platforms.append((x_pos, y_pos, 55, 20))
            x_pos += 95 + (i % 7) * 15
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 5 plataformas)
        for i in range(5, len(platforms), 5):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 150, 55, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 250)
        
    def create_level_17(self):
        """Nível 17 - Progressão com tartarugas (84 plataformas)"""
        platforms = []
        x_pos = 40
        for i in range(84):
            y_pos = HEIGHT - (140 + (i % 11) * 50 + (i // 11) * 50)
            platforms.append((x_pos, y_pos, 50, 20))
            x_pos += 90 + (i % 8) * 10
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 4 plataformas)
        for i in range(4, len(platforms), 4):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 140, 50, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 240)
        
    def create_level_18(self):
        """Nível 18 - Progressão com tartarugas (93 plataformas)"""
        platforms = []
        x_pos = 30
        for i in range(93):
            y_pos = HEIGHT - (130 + (i % 12) * 45 + (i // 12) * 55)
            platforms.append((x_pos, y_pos, 45, 20))
            x_pos += 85 + (i % 9) * 5
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 3 plataformas)
        for i in range(3, len(platforms), 3):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 130, 45, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 230)
        
    def create_level_19(self):
        """Nível 19 - Progressão com tartarugas (102 plataformas)"""
        platforms = []
        x_pos = 20
        for i in range(102):
            y_pos = HEIGHT - (120 + (i % 13) * 40 + (i // 13) * 60)
            platforms.append((x_pos, y_pos, 40, 20))
            x_pos += 80 + (i % 10) * 0
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (1 a cada 2 plataformas)
        for i in range(2, len(platforms), 2):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 120, 40, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 220)
        
    def create_level_20(self):
        """Nível 20 - Máxima dificuldade com tartarugas (110 plataformas)"""
        platforms = []
        x_pos = 10
        for i in range(110):
            y_pos = HEIGHT - (110 + (i % 15) * 35 + (i // 15) * 65)
            platforms.append((x_pos, y_pos, 35, 20))
            x_pos += 75
        
        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))
            
        # Posicionar jogador na primeira plataforma
        first_platform = platforms[0]
        self.player.x = first_platform[0] + 10
        self.player.y = first_platform[1] - self.player.height
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y
        self.player.vel_y = 0
        self.player.on_ground = True
            
        # Adicionar tartarugas (máxima quantidade - 1 por plataforma)
        for i, platform in enumerate(platforms):
            if i % 1 == 0:  # Uma tartaruga por plataforma
                turtle = Turtle(platform[0], platform[1] - 30, platform[0], platform[0] + platform[2])
                self.turtles.append(turtle)
            
        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(Platform(final_x, HEIGHT - 110, 35, 20, self.platform_texture))
        self.flag = Flag(final_x + 20, HEIGHT - 210)
        
    def draw_ocean_background(self):
        """Desenhar fundo do mar"""
        if self.background_img:
            # Usar imagem de fundo
            self.screen.blit(self.background_img, (0, 0))
        else:
            # Fallback para gradiente se a imagem não carregar
            for y in range(HEIGHT):
                ratio = y / HEIGHT
                r = int(135 * (1 - ratio) + 0 * ratio)
                g = int(206 * (1 - ratio) + 50 * ratio)
                b = int(235 * (1 - ratio) + 100 * ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
                
            # Ondas simples
            wave_offset = pygame.time.get_ticks() * 0.002
            for x in range(0, WIDTH, 20):
                wave_y = HEIGHT - 50 + math.sin(x * 0.01 + wave_offset) * 10
                pygame.draw.circle(self.screen, (0, 80, 150), (x, int(wave_y)), 15)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # Navegação do splash screen
                if self.state == GameState.SPLASH:
                    # Só permite pular se estiver em modo development
                    if ENV_CONFIG.get('environment', 'production') == 'development':
                        self.state = GameState.MAIN_MENU
                        # Iniciar música do menu quando pular para o menu
                        if not self.music_started:
                            self.play_menu_music()
                            self.music_started = True
                # Navegação do menu principal
                elif self.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.handle_menu_selection()
                # Navegação das telas de créditos e recordes
                elif self.state == GameState.CREDITS:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.state = GameState.MAIN_MENU
                elif self.state == GameState.RECORDS:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        # Voltar ao estado anterior (MAIN_MENU ou GAME_OVER)
                        if self.previous_state_before_records:
                            self.state = self.previous_state_before_records
                            self.previous_state_before_records = None
                        else:
                            self.state = GameState.MAIN_MENU  # Fallback
                # Navegação do menu de game over
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_UP:
                        self.game_over_selected = (self.game_over_selected - 1) % len(self.game_over_options)
                    elif event.key == pygame.K_DOWN:
                        self.game_over_selected = (self.game_over_selected + 1) % len(self.game_over_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.game_over_selected == 0:  # Jogar novamente
                            # Configurar nível inicial baseado no ambiente
                            if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG:
                                try:
                                    self.current_level = int(ENV_CONFIG['initial-stage'])
                                    # Validar se o nível está dentro do range válido
                                    if self.current_level < 1 or self.current_level > 20:
                                        self.current_level = 1
                                except (ValueError, TypeError):
                                    self.current_level = 1
                            else:
                                self.current_level = 1
                            self.score = 0
                            self.platforms_jumped.clear()
                            self.birds_dodged.clear()
                            self.lives = self.max_lives
                            self.player_name = ""
                            self.game_over_selected = 0  # Reset menu selection
                            self.state = GameState.PLAYING
                            self.init_level()
                        elif self.game_over_selected == 1:  # Recordes
                            self.previous_state_before_records = GameState.GAME_OVER
                            self.state = GameState.RECORDS
                        elif self.game_over_selected == 2:  # Sair
                            return False
                if self.state == GameState.ENTER_NAME:
                    # Capturar entrada de nome
                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            # Adicionar ao ranking e mostrar
                            self.ranking_manager.add_score(self.player_name.strip(), self.score)
                            # Salvar o estado anterior antes de ir para SHOW_RANKING
                            self.previous_state_before_ranking = GameState.GAME_OVER
                            self.state = GameState.SHOW_RANKING
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        # Adicionar caractere (limitado a 25)
                        if len(self.player_name) < 25 and event.unicode.isprintable():
                            self.player_name += event.unicode
                elif event.key == pygame.K_r and (self.state == GameState.VICTORY or self.state == GameState.SHOW_RANKING):
                    # Configurar nível inicial baseado no ambiente
                    if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG:
                        try:
                            self.current_level = int(ENV_CONFIG['initial-stage'])
                            # Validar se o nível está dentro do range válido
                            if self.current_level < 1 or self.current_level > 20:
                                self.current_level = 1
                        except (ValueError, TypeError):
                            self.current_level = 1
                    else:
                        self.current_level = 1
                    self.score = 0  # Resetar pontuação
                    self.platforms_jumped.clear()  # Resetar plataformas pontuadas
                    self.birds_dodged.clear()  # Resetar pássaros esquivados
                    self.lives = self.max_lives  # Resetar vidas
                    self.player_name = ""  # Resetar nome
                    self.state = GameState.PLAYING
                    self.init_level()  # Inicializar o nível para posicionar jogador corretamente
                elif event.key == pygame.K_ESCAPE and self.state == GameState.SHOW_RANKING:
                    # Voltar ao estado anterior (GAME_OVER ou VICTORY)
                    if self.previous_state_before_ranking:
                        self.state = self.previous_state_before_ranking
                        self.previous_state_before_ranking = None
                    else:
                        self.state = GameState.GAME_OVER  # Fallback
                    self.init_level()
                elif event.key == pygame.K_ESCAPE:
                    return False
            
            # Eventos do joystick
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.joystick_connected:
                    # Navegação do splash screen com joystick
                    if self.state == GameState.SPLASH:
                        # Só permite pular se estiver em modo development
                        if ENV_CONFIG.get('environment', 'production') == 'development':
                            self.state = GameState.MAIN_MENU
                            # Iniciar música do menu quando pular para o menu
                            if not self.music_started:
                                self.play_menu_music()
                                self.music_started = True
                    # Navegação do menu principal com joystick
                    elif self.state == GameState.MAIN_MENU:
                        if event.button == 0 or event.button in [6, 7, 8, 9]:  # A/X ou Start/Options
                            self.handle_menu_selection()
                    # Navegação das telas de créditos e recordes com joystick
                    elif self.state == GameState.CREDITS:
                        if event.button == 1 or event.button in [6, 7, 8, 9]:  # B/Círculo ou Start/Options
                            self.state = GameState.MAIN_MENU
                    elif self.state == GameState.RECORDS:
                        if event.button == 1 or event.button in [6, 7, 8, 9]:  # B/Círculo ou Start/Options
                            # Voltar ao estado anterior (MAIN_MENU ou GAME_OVER)
                            if self.previous_state_before_records:
                                self.state = self.previous_state_before_records
                                self.previous_state_before_records = None
                            else:
                                self.state = GameState.MAIN_MENU  # Fallback
                    # Navegação do menu de game over com joystick
                    elif self.state == GameState.GAME_OVER:
                        if event.button == 0 or event.button in [6, 7, 8, 9]:  # A/X ou Start/Options
                            if self.game_over_selected == 0:  # Jogar novamente
                                # Configurar nível inicial baseado no ambiente
                                if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG:
                                    try:
                                        self.current_level = int(ENV_CONFIG['initial-stage'])
                                        # Validar se o nível está dentro do range válido
                                        if self.current_level < 1 or self.current_level > 20:
                                            self.current_level = 1
                                    except (ValueError, TypeError):
                                        self.current_level = 1
                                else:
                                    self.current_level = 1
                                self.score = 0
                                self.platforms_jumped.clear()
                                self.birds_dodged.clear()
                                self.lives = self.max_lives
                                self.player_name = ""
                                self.game_over_selected = 0
                                self.state = GameState.PLAYING
                                self.init_level()
                            elif self.game_over_selected == 1:  # Recordes
                                self.previous_state_before_records = GameState.GAME_OVER
                                self.state = GameState.RECORDS
                            elif self.game_over_selected == 2:  # Sair
                                return False
                    # Botão A (0) ou X (0) para pular
                    elif event.button == 0:  # Botão A/X
                        keys = pygame.key.get_pressed()
                        keys = list(keys)
                        keys[pygame.K_SPACE] = True
                        keys = tuple(keys)
                    # Botão B (1) ou Círculo (1) para atirar
                    elif event.button == 1:  # Botão B/Círculo
                        keys = pygame.key.get_pressed()
                        keys = list(keys)
                        keys[pygame.K_SPACE] = True  # Usar espaço para tiro também
                        keys = tuple(keys)
                    # Start/Options para confirmar nome ou reiniciar
                    elif event.button in [6, 7, 8, 9]:  # Start/Options (varia entre drivers)
                        if self.state == GameState.ENTER_NAME:
                            # Confirmar entrada de nome (equivalente ao ENTER)
                            if self.player_name.strip():
                                self.ranking_manager.add_score(self.player_name.strip(), self.score)
                                # Salvar o estado anterior antes de ir para SHOW_RANKING
                                self.previous_state_before_ranking = GameState.GAME_OVER
                                self.state = GameState.SHOW_RANKING
                        elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY or self.state == GameState.SHOW_RANKING:
                            # Reiniciar jogo (equivalente ao R)
                            # Configurar nível inicial baseado no ambiente
                            if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG:
                                try:
                                    self.current_level = int(ENV_CONFIG['initial-stage'])
                                    # Validar se o nível está dentro do range válido
                                    if self.current_level < 1 or self.current_level > 20:
                                        self.current_level = 1
                                except (ValueError, TypeError):
                                    self.current_level = 1
                            else:
                                self.current_level = 1
                            self.score = 0
                            self.platforms_jumped.clear()
                            self.birds_dodged.clear()
                            self.lives = self.max_lives
                            self.player_name = ""
                            self.state = GameState.PLAYING
                            self.init_level()
                    # Botão B para voltar do ranking
                    elif event.button == 1 and self.state == GameState.SHOW_RANKING:  # Botão B
                        # Voltar ao estado anterior (GAME_OVER ou VICTORY)
                        if self.previous_state_before_ranking:
                            self.state = self.previous_state_before_ranking
                            self.previous_state_before_ranking = None
                        else:
                            self.state = GameState.GAME_OVER  # Fallback
        
        # Verificar movimento do joystick (analógico e D-pad) para navegação dos menus
        if self.joystick_connected:
            # Capturar eixos analógicos (mesma lógica do gameplay)
            analog_vertical = 0
            analog_horizontal = 0
            
            if self.joystick.get_numaxes() >= 2:
                analog_vertical = self.joystick.get_axis(1)  # Eixo Y do analógico esquerdo
                # Aplicar zona morta para evitar drift
                if abs(analog_vertical) < 0.1:
                    analog_vertical = 0
            
            if self.joystick.get_numaxes() >= 1:
                analog_horizontal = self.joystick.get_axis(0)  # Eixo X do analógico esquerdo
                # Aplicar zona morta para evitar drift
                if abs(analog_horizontal) < 0.1:
                    analog_horizontal = 0
            
            # Capturar D-pad
            dpad_vertical = 0
            dpad_horizontal = 0
            
            if self.joystick.get_numaxes() > 7:
                dpad_vertical = self.joystick.get_axis(7)
            if self.joystick.get_numaxes() > 6:
                dpad_horizontal = self.joystick.get_axis(6)
            
            # Detectar mudança no eixo vertical (analógico ou D-pad)
            analog_up = analog_vertical < -0.5 and self.prev_analog_vertical >= -0.5
            analog_down = analog_vertical > 0.5 and self.prev_analog_vertical <= 0.5
            dpad_up = dpad_vertical < -0.5 and self.prev_dpad_vertical >= -0.5
            dpad_down = dpad_vertical > 0.5 and self.prev_dpad_vertical <= 0.5
            
            # Navegação para cima (analógico ou D-pad)
            if analog_up or dpad_up:
                if self.state == GameState.MAIN_MENU:
                    self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
                elif self.state == GameState.GAME_OVER:
                    self.game_over_selected = (self.game_over_selected - 1) % len(self.game_over_options)
            
            # Navegação para baixo (analógico ou D-pad)
            elif analog_down or dpad_down:
                if self.state == GameState.MAIN_MENU:
                    self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
                elif self.state == GameState.GAME_OVER:
                    self.game_over_selected = (self.game_over_selected + 1) % len(self.game_over_options)
            
            # Atualizar valores anteriores
            self.prev_analog_vertical = analog_vertical
            self.prev_analog_horizontal = analog_horizontal
            self.prev_dpad_vertical = dpad_vertical
            self.prev_dpad_horizontal = dpad_horizontal
        
        return True
    
    def handle_menu_selection(self):
        """Processar seleção do menu principal"""
        selected_option = self.menu_options[self.menu_selected]
        
        if selected_option == 'Iniciar':
            # Iniciar novo jogo
            # Configurar nível inicial baseado no ambiente
            if ENV_CONFIG.get('environment') == 'development' and 'initial-stage' in ENV_CONFIG:
                try:
                    self.current_level = int(ENV_CONFIG['initial-stage'])
                    # Validar se o nível está dentro do range válido
                    if self.current_level < 1 or self.current_level > 20:
                        print(f"Aviso: initial-stage {self.current_level} inválido. Usando nível 1.")
                        self.current_level = 1
                except (ValueError, TypeError):
                    print("Aviso: initial-stage deve ser um número. Usando nível 1.")
                    self.current_level = 1
            else:
                self.current_level = 1
            self.score = 0
            self.platforms_jumped.clear()
            self.birds_dodged.clear()
            self.lives = self.max_lives
            self.player_name = ""
            self.state = GameState.PLAYING
            self.init_level()
            # Tocar música do nível atual
            self.play_level_music(self.current_level)
        elif selected_option == 'Recordes':
            self.state = GameState.RECORDS
        elif selected_option == 'Créditos':
            self.state = GameState.CREDITS
        elif selected_option == 'Sair':
            pygame.quit()
            sys.exit()
        
    def update(self):
        if self.state == GameState.SPLASH:
            # Atualizar timer do splash screen
            self.splash_timer += 1
            
            # Calcular qual logo mostrar baseado no tempo com fade
            if self.logos:
                self.current_logo_index = (self.splash_timer // self.logo_display_time) % len(self.logos)
            
            # Após o tempo total, ir para o menu
            if self.splash_timer >= self.splash_duration:
                self.state = GameState.MAIN_MENU
                # Iniciar música do menu quando aparecer o menu
                if not self.music_started:
                    self.play_menu_music()
                    self.music_started = True
        
        elif self.state == GameState.PLAYING:
            # Atualizar jogador
            if not self.player.update(self.platforms, self.bullet_image, self.camera_x, self.joystick if self.joystick_connected else None):
                # Jogador morreu (caiu da tela) - decrementar vida
                self.lives -= 1
                if self.lives <= 0:
                    # Sem vidas, game over - verificar se entra no ranking
                    if self.ranking_manager.is_high_score(self.score):
                        self.state = GameState.ENTER_NAME
                    else:
                        self.state = GameState.GAME_OVER
                else:
                    # Ainda tem vidas, reiniciar nível atual
                    self.init_level()
                
            # Atualizar câmera para seguir o jogador
            target_camera_x = self.player.x - CAMERA_OFFSET_X
            if target_camera_x > self.camera_x:
                self.camera_x = target_camera_x
                
            # Sistema de pontuação - verificar se jogador pousou em nova plataforma
            if self.player.just_landed and hasattr(self.player, 'landed_platform_id'):
                if self.player.landed_platform_id not in self.platforms_jumped:
                    self.platforms_jumped.add(self.player.landed_platform_id)
                    self.score += 10
                # Reset da flag após verificar pontuação
                self.player.just_landed = False
                delattr(self.player, 'landed_platform_id')
                
            # Sistema de pássaros
            # Spawn de novos pássaros
            self.bird_spawn_timer += 1
            if self.bird_spawn_timer >= self.bird_spawn_interval:
                # Spawnar múltiplos pássaros baseado no nível
                import random
                for i in range(self.birds_per_spawn):
                    bird_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                    bird_x = WIDTH + self.camera_x + 50 + (i * 100)  # Espaçar pássaros
                    bird_images = (self.bird_img1, self.bird_img2) if hasattr(self, 'bird_img1') else None
                    self.birds.append(Bird(bird_x, bird_y, bird_images))
                self.bird_spawn_timer = 0
            
            # Atualizar pássaros
            self.birds = [bird for bird in self.birds if bird.update()]
            
            # Atualizar tartarugas
            for turtle in self.turtles:
                turtle.update()
            
            # Atualizar explosões
            self.explosions = [explosion for explosion in self.explosions if explosion.update()]
            
            # Verificar colisão entre tiros e pássaros
            for bullet in self.player.bullets[:]:
                for bird in self.birds[:]:
                    if bullet.rect.colliderect(bird.rect):
                        # Tiro acertou pássaro
                        self.player.bullets.remove(bullet)
                        self.birds.remove(bird)
                        # Criar explosão na posição do pássaro
                        self.explosions.append(Explosion(bird.x, bird.y, self.explosion_image))
                        # Adicionar pontos
                        self.score += 50
                        break
            
            # Verificar colisão entre tiros e tartarugas
            for bullet in self.player.bullets[:]:
                for turtle in self.turtles[:]:
                    if bullet.rect.colliderect(turtle.rect):
                        # Tiro acertou tartaruga
                        self.player.bullets.remove(bullet)
                        self.turtles.remove(turtle)
                        # Criar explosão na posição da tartaruga
                        self.explosions.append(Explosion(turtle.x, turtle.y, self.explosion_image))
                        # Adicionar pontos
                        self.score += 60
                        break
            
            # Verificar colisão e esquiva com pássaros
            for bird in self.birds[:]:
                # Verificar se pássaro passou perto do jogador (esquiva)
                distance_x = abs(bird.x - self.player.x)
                distance_y = abs(bird.y - self.player.y)
                
                # Se pássaro passou perto (dentro de 40 pixels) e já passou do jogador
                if (distance_x < 40 and distance_y < 50 and 
                    bird.x < self.player.x and bird.id not in self.birds_dodged):
                    self.birds_dodged.add(bird.id)
                    self.score += 10  # Pontos por esquivar
                
                # Verificar colisão direta
                if self.player.rect.colliderect(bird.rect):
                    # Colidiu com pássaro, ativar animação de hit
                    if not self.player.is_hit:  # Só aplicar hit se não estiver já em estado de hit
                        self.player.take_hit()
                        # Criar explosão na posição do pássaro
                        self.explosions.append(Explosion(bird.x, bird.y, self.explosion_image))
                        self.birds.remove(bird)
                        self.lives -= 1
                        if self.lives <= 0:
                            # Sem vidas, game over - verificar se entra no ranking
                            if self.ranking_manager.is_high_score(self.score):
                                self.state = GameState.ENTER_NAME
                            else:
                                self.state = GameState.GAME_OVER
                        # Não reiniciar o nível imediatamente, deixar o jogador continuar
                    break
            
            # Verificar colisão com tartarugas
            for turtle in self.turtles[:]:
                # Verificar colisão direta
                if self.player.rect.colliderect(turtle.rect):
                    # Colidiu com tartaruga, ativar animação de hit
                    if not self.player.is_hit:  # Só aplicar hit se não estiver já em estado de hit
                        self.player.take_hit()
                        # Criar explosão na posição da tartaruga
                        self.explosions.append(Explosion(turtle.x, turtle.y, self.explosion_image))
                        self.turtles.remove(turtle)
                        self.lives -= 1
                        if self.lives <= 0:
                            # Sem vidas, game over - verificar se entra no ranking
                            if self.ranking_manager.is_high_score(self.score):
                                self.state = GameState.ENTER_NAME
                            else:
                                self.state = GameState.GAME_OVER
                        # Não reiniciar o nível imediatamente, deixar o jogador continuar
                    break
            
            # Verificar se tocou a bandeira
            if self.player.rect.colliderect(self.flag.rect):
                if self.current_level < self.max_levels:
                    self.current_level += 1
                    self.init_level()
                else:
                    # Vitória - verificar se entra no ranking
                    if self.ranking_manager.is_high_score(self.score):
                        self.state = GameState.ENTER_NAME
                    else:
                        self.state = GameState.VICTORY
                    
    def draw(self):
        if self.state == GameState.SPLASH:
            # Tela de splash com fundo preto
            self.screen.fill(BLACK)
            
            # Mostrar logo atual com efeito de fade
            if self.logos and self.current_logo_index < len(self.logos):
                logo = self.logos[self.current_logo_index]
                
                # Calcular posição no ciclo do logo atual
                logo_cycle_time = self.splash_timer % self.logo_display_time
                alpha = 255  # Opacidade padrão
                
                # Fade in (primeiros frames)
                if logo_cycle_time < self.fade_in_duration:
                    alpha = int((logo_cycle_time / self.fade_in_duration) * 255)
                # Fade out (últimos frames)
                elif logo_cycle_time > (self.logo_display_time - self.fade_out_duration):
                    fade_progress = (logo_cycle_time - (self.logo_display_time - self.fade_out_duration)) / self.fade_out_duration
                    alpha = int((1 - fade_progress) * 255)
                
                # Aplicar alpha ao logo
                if alpha < 255:
                    logo_with_alpha = logo.copy()
                    logo_with_alpha.set_alpha(alpha)
                    logo_rect = logo_with_alpha.get_rect(center=(WIDTH//2, HEIGHT//2))
                    self.screen.blit(logo_with_alpha, logo_rect)
                else:
                    logo_rect = logo.get_rect(center=(WIDTH//2, HEIGHT//2))
                    self.screen.blit(logo, logo_rect)
            
            # Texto de instrução com fade suave (só em modo development)
            if ENV_CONFIG.get('environment', 'production') == 'development':
                instruction_alpha = min(255, self.splash_timer * 3)  # Fade in gradual
                instruction_text = self.font.render("Pressione qualquer tecla para continuar", True, WHITE)
                if instruction_alpha < 255:
                    instruction_text.set_alpha(instruction_alpha)
                instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
                self.screen.blit(instruction_text, instruction_rect)
        
        elif self.state == GameState.MAIN_MENU:
            # Tela de menu com fundo do jogo
            self.draw_ocean_background()
            
            # Logo do jogo (aumentado)
            if self.game_logo:
                # Aumentar o tamanho do logo em 50%
                logo_scaled = pygame.transform.scale(self.game_logo, 
                    (int(self.game_logo.get_width() * 1.5), int(self.game_logo.get_height() * 1.5)))
                logo_rect = logo_scaled.get_rect(center=(WIDTH//2, 120))
                self.screen.blit(logo_scaled, logo_rect)
            
            # Título do jogo se não houver logo
            else:
                title_text = self.big_font.render("Jogo de Plataforma - Mar", True, WHITE)
                title_rect = title_text.get_rect(center=(WIDTH//2, 150))
                self.screen.blit(title_text, title_rect)
            
            # Opções do menu
            menu_start_y = 300
            for i, option in enumerate(self.menu_options):
                color = YELLOW if i == self.menu_selected else WHITE
                option_text = self.font.render(option, True, color)
                option_rect = option_text.get_rect(center=(WIDTH//2, menu_start_y + i * 60))
                
                # Destacar opção selecionada com retângulo
                if i == self.menu_selected:
                    pygame.draw.rect(self.screen, DARK_BLUE, option_rect.inflate(20, 10))
                
                self.screen.blit(option_text, option_rect)
            
            # Rodapé com direitos autorais
            footer_text = "Desenvolvido por CirrasTec, Cirras RetroGames e Canal do Dudu. Todos os direitos reservados."
            footer_surface = pygame.font.Font(None, 24).render(footer_text, True, LIGHT_GRAY)
            footer_rect = footer_surface.get_rect(center=(WIDTH//2, HEIGHT - 30))
            self.screen.blit(footer_surface, footer_rect)
        
        elif self.state == GameState.PLAYING:
            self.draw_ocean_background()
            # Criar surface temporária para aplicar offset da câmera
            temp_surface = pygame.Surface((WIDTH, HEIGHT))
            temp_surface.fill((0, 0, 0, 0))  # Transparente
            
            # Desenhar plataformas com offset da câmera
            for platform in self.platforms:
                adjusted_rect = pygame.Rect(
                    platform.rect.x - self.camera_x,
                    platform.rect.y,
                    platform.rect.width,
                    platform.rect.height
                )
                if adjusted_rect.right > 0 and adjusted_rect.left < WIDTH:  # Só desenhar se visível
                    # Salvar posição original da plataforma
                    original_x = platform.x
                    # Ajustar posição para câmera
                    platform.x = adjusted_rect.x
                    # Usar o método draw da plataforma que faz ladrilhamento correto
                    platform.draw(self.screen)
                    # Restaurar posição original
                    platform.x = original_x
                
            # Desenhar bandeira com offset da câmera
            flag_x = self.flag.x - self.camera_x
            if flag_x > -50 and flag_x < WIDTH:  # Só desenhar se visível
                # Salvar posição original da bandeira
                original_x = self.flag.x
                # Ajustar posição temporariamente para o offset da câmera
                self.flag.x = flag_x
                # Desenhar usando o método da classe Flag
                self.flag.draw(self.screen)
                # Restaurar posição original
                self.flag.x = original_x
            
            # Desenhar pássaros com offset da câmera
            for bird in self.birds:
                bird_x = bird.x - self.camera_x
                if bird_x > -50 and bird_x < WIDTH:  # Só desenhar se visível
                    # Salvar posição original do pássaro
                    original_bird_x = bird.x
                    # Ajustar posição para câmera
                    bird.x = bird_x
                    # Chamar método draw do pássaro
                    bird.draw(self.screen)
                    # Restaurar posição original
                    bird.x = original_bird_x
            
            # Desenhar tartarugas com offset da câmera
            for turtle in self.turtles:
                turtle_x = turtle.x - self.camera_x
                if turtle_x > -50 and turtle_x < WIDTH:  # Só desenhar se visível
                    # Salvar posição original da tartaruga
                    original_turtle_x = turtle.x
                    # Ajustar posição para câmera
                    turtle.x = turtle_x
                    # Chamar método draw da tartaruga
                    turtle.draw(self.screen)
                    # Restaurar posição original
                    turtle.x = original_turtle_x
            
            # Desenhar explosões com offset da câmera
            for explosion in self.explosions:
                explosion_x = explosion.x - self.camera_x
                if explosion_x > -50 and explosion_x < WIDTH:  # Só desenhar se visível
                    # Salvar posição original da explosão
                    original_explosion_x = explosion.x
                    # Ajustar posição para câmera
                    explosion.x = explosion_x
                    # Chamar método draw da explosão
                    explosion.draw(self.screen)
                    # Restaurar posição original
                    explosion.x = original_explosion_x
            
            # Desenhar tiros do jogador com offset da câmera
            for bullet in self.player.bullets:
                bullet_x = bullet.x - self.camera_x
                if bullet_x > -20 and bullet_x < WIDTH + 20:  # Só desenhar se visível
                    # Salvar posição original do tiro
                    original_bullet_x = bullet.x
                    # Ajustar posição para câmera
                    bullet.x = bullet_x
                    # Chamar método draw do tiro
                    bullet.draw(self.screen)
                    # Restaurar posição original
                    bullet.x = original_bullet_x
            
            # Desenhar jogador com offset da câmera
            # Salvar posição original do jogador
            original_x = self.player.x
            # Ajustar posição para câmera
            self.player.x = self.player.x - self.camera_x
            # Chamar método draw do jogador
            self.player.draw(self.screen)
            # Restaurar posição original
            self.player.x = original_x
            
            # Desenhar UI (sem offset da câmera)
            level_text = self.font.render(f"Nível: {self.current_level}", True, WHITE)
            score_text = self.font.render(f"Pontuação: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Vidas: {self.lives}", True, WHITE)
            self.screen.blit(level_text, (10, 10))
            self.screen.blit(score_text, (10, 50))
            self.screen.blit(lives_text, (10, 90))
            
        elif self.state == GameState.GAME_OVER:
            # Usar fundo do cenário
            self.draw_ocean_background()
            
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Pontuação Final: {self.score}", True, WHITE)
            
            # Centralizar textos principais
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            
            # Menu de opções
            for i, option in enumerate(self.game_over_options):
                color = YELLOW if i == self.game_over_selected else WHITE
                option_text = self.font.render(option, True, color)
                option_rect = option_text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 40))
                
                # Destacar opção selecionada com retângulo
                if i == self.game_over_selected:
                    pygame.draw.rect(self.screen, DARK_BLUE, option_rect.inflate(20, 10))
                
                self.screen.blit(option_text, option_rect)
            
            # Instruções de controle
            control_text = self.font.render("Use ↑↓ ou D-pad para navegar, Enter ou A para selecionar", True, LIGHT_GRAY)
            control_rect = control_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
            self.screen.blit(control_text, control_rect)
            
        elif self.state == GameState.VICTORY:
            # Desenhar troféu (usando formas geométricas)
            trophy_x = WIDTH//2
            trophy_y = HEIGHT//2 - 100
            
            # Base do troféu
            pygame.draw.rect(self.screen, BROWN, (trophy_x - 40, trophy_y + 80, 80, 20))
            pygame.draw.rect(self.screen, BROWN, (trophy_x - 10, trophy_y + 60, 20, 40))
            
            # Taça do troféu
            pygame.draw.ellipse(self.screen, YELLOW, (trophy_x - 30, trophy_y, 60, 80))
            pygame.draw.ellipse(self.screen, (255, 215, 0), (trophy_x - 25, trophy_y + 5, 50, 70))
            
            # Alças do troféu
            pygame.draw.arc(self.screen, YELLOW, (trophy_x - 50, trophy_y + 20, 20, 40), 0, math.pi, 5)
            pygame.draw.arc(self.screen, YELLOW, (trophy_x + 30, trophy_y + 20, 20, 40), 0, math.pi, 5)
            
            # Textos
            victory_text = self.big_font.render("PARABÉNS!", True, GREEN)
            complete_text = self.font.render("Você completou todos os níveis!", True, WHITE)
            final_score_text = self.font.render(f"Pontuação Final: {self.score}", True, WHITE)
            restart_text = self.font.render("Pressione R para jogar novamente", True, WHITE)
            
            self.screen.blit(victory_text, (WIDTH//2 - 150, HEIGHT//2 + 120))
            self.screen.blit(complete_text, (WIDTH//2 - 200, HEIGHT//2 + 170))
            self.screen.blit(final_score_text, (WIDTH//2 - 120, HEIGHT//2 + 200))
            self.screen.blit(restart_text, (WIDTH//2 - 180, HEIGHT//2 + 240))
            
        elif self.state == GameState.ENTER_NAME:
            # Tela para inserir nome no ranking
            title_text = self.big_font.render("NOVO RECORDE!", True, YELLOW)
            score_text = self.font.render(f"Pontuação: {self.score}", True, WHITE)
            prompt_text = self.font.render("Digite seu nome (máximo 25 caracteres):", True, WHITE)
            
            # Campo de entrada de nome com cursor
            name_display = self.player_name + "_" if len(self.player_name) < 25 else self.player_name
            name_text = self.font.render(name_display, True, WHITE)
            
            instruction_text = self.font.render("Pressione ENTER para confirmar", True, LIGHT_GRAY)
            
            # Centralizar textos
            title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 150))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
            prompt_rect = prompt_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            name_rect = name_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            
            # Desenhar caixa de entrada
            input_box = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 15, 400, 30)
            pygame.draw.rect(self.screen, DARK_GRAY, input_box)
            pygame.draw.rect(self.screen, WHITE, input_box, 2)
            
            self.screen.blit(title_text, title_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(prompt_text, prompt_rect)
            self.screen.blit(name_text, name_rect)
            self.screen.blit(instruction_text, instruction_rect)
            
        elif self.state == GameState.SHOW_RANKING:
            # Usar fundo do cenário em vez de fundo sólido
            self.draw_ocean_background()
            
            # Tela do ranking
            title_text = self.big_font.render("TOP 10 RANKING", True, YELLOW)
            rankings = self.ranking_manager.get_rankings()
            
            # Título
            title_rect = title_text.get_rect(center=(WIDTH//2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Cabeçalho com posições fixas
            pos_x = WIDTH//2 - 200  # Posição inicial da tabela
            header_pos = self.font.render("POS", True, WHITE)
            header_name = self.font.render("NOME", True, WHITE)
            header_score = self.font.render("PONTUAÇÃO", True, WHITE)
            
            self.screen.blit(header_pos, (pos_x, 180))
            self.screen.blit(header_name, (pos_x + 60, 180))
            self.screen.blit(header_score, (pos_x + 300, 180))
            
            # Linha separadora
            pygame.draw.line(self.screen, WHITE, (pos_x - 10, 200), (pos_x + 390, 200), 2)
            
            # Rankings com colunas alinhadas
            y_offset = 230
            for i, ranking in enumerate(rankings, 1):
                # Destacar o jogador atual se estiver no ranking
                color = YELLOW if ranking['name'] == self.player_name.strip() else WHITE
                
                # Coluna posição
                pos_text = self.font.render(f"{i:2d}.", True, color)
                self.screen.blit(pos_text, (pos_x, y_offset))
                
                # Coluna nome (limitado a 18 chars para caber na coluna)
                name_display = ranking['name'][:18]
                name_text = self.font.render(name_display, True, color)
                self.screen.blit(name_text, (pos_x + 60, y_offset))
                
                # Coluna pontuação (alinhada à direita)
                score_display = f"{int(ranking['score']):,}".replace(',', '.')
                score_text = self.font.render(score_display, True, color)
                score_rect = score_text.get_rect()
                score_rect.right = pos_x + 390
                score_rect.y = y_offset
                self.screen.blit(score_text, score_rect)
                
                y_offset += 35
            
            # Instruções
            restart_text = self.font.render("Pressione R para jogar novamente", True, LIGHT_GRAY)
            restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT - 80))
            self.screen.blit(restart_text, restart_rect)
            
            back_text = self.font.render("Pressione ESC ou Botão B para voltar", True, LIGHT_GRAY)
            back_rect = back_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
            self.screen.blit(back_text, back_rect)
        
        elif self.state == GameState.CREDITS:
            # Tela de créditos com fundo do jogo
            self.draw_ocean_background()
            
            # Título
            title_text = self.big_font.render("CRÉDITOS", True, YELLOW)
            title_rect = title_text.get_rect(center=(WIDTH//2, 80))
            self.screen.blit(title_text, title_rect)
            
            # Conteúdo dos créditos
            credits_content = [
                "Jogo de Plataforma - Mar",
                "",
                "Desenvolvido por:",
                "CirrasTec",
                "",
                "Em parceria com:",
                "Cirras RetroGames",
                "https://www.youtube.com/@cirrasretrogames",
                "",
                "Canal do Dudu",
                "https://www.youtube.com/@canaldodudu8789",
                "",
                "Este jogo foi criado com paixão e dedicação,",
                "combinando a nostalgia dos jogos clássicos",
                "com elementos modernos de gameplay.",
                "",
                "Agradecemos por jogar!",
            ]
            
            y_offset = 150
            for line in credits_content:
                if line.startswith("https://"):
                    # Links em cor diferente
                    text_surface = self.font.render(line, True, LIGHT_BLUE)
                elif line in ["CirrasTec", "Cirras RetroGames", "Canal do Dudu"]:
                    # Nomes em destaque
                    text_surface = self.font.render(line, True, YELLOW)
                else:
                    # Texto normal
                    text_surface = self.font.render(line, True, WHITE)
                
                text_rect = text_surface.get_rect(center=(WIDTH//2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 30
            
            # Instruções
            instruction_text = self.font.render("Pressione ESC ou ENTER para voltar", True, LIGHT_GRAY)
            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
            self.screen.blit(instruction_text, instruction_rect)
        
        elif self.state == GameState.RECORDS:
            # Tela de recordes (reutilizar a lógica do ranking)
            self.draw_ocean_background()
            
            # Título
            title_text = self.big_font.render("RECORDES", True, YELLOW)
            rankings = self.ranking_manager.get_rankings()
            
            # Título
            title_rect = title_text.get_rect(center=(WIDTH//2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Cabeçalho com posições fixas
            pos_x = WIDTH//2 - 200  # Posição inicial da tabela
            header_pos = self.font.render("POS", True, WHITE)
            header_name = self.font.render("NOME", True, WHITE)
            header_score = self.font.render("PONTUAÇÃO", True, WHITE)
            
            self.screen.blit(header_pos, (pos_x, 180))
            self.screen.blit(header_name, (pos_x + 60, 180))
            self.screen.blit(header_score, (pos_x + 300, 180))
            
            # Linha separadora
            pygame.draw.line(self.screen, WHITE, (pos_x - 10, 200), (pos_x + 390, 200), 2)
            
            # Rankings com colunas alinhadas
            y_offset = 230
            for i, ranking in enumerate(rankings, 1):
                color = WHITE
                
                # Coluna posição
                pos_text = self.font.render(f"{i:2d}.", True, color)
                self.screen.blit(pos_text, (pos_x, y_offset))
                
                # Coluna nome (limitado a 18 chars para caber na coluna)
                name_display = ranking['name'][:18]
                name_text = self.font.render(name_display, True, color)
                self.screen.blit(name_text, (pos_x + 60, y_offset))
                
                # Coluna pontuação (alinhada à direita)
                score_display = f"{int(ranking['score']):,}".replace(',', '.')
                score_text = self.font.render(score_display, True, color)
                score_rect = score_text.get_rect()
                score_rect.right = pos_x + 390
                score_rect.y = y_offset
                self.screen.blit(score_text, score_rect)
                
                y_offset += 35
            
            # Instruções
            instruction_text = self.font.render("Pressione ESC ou ENTER para voltar", True, LIGHT_GRAY)
            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
            self.screen.blit(instruction_text, instruction_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()