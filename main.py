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
    MENU = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    VICTORY = 5  # Nova tela de vitória com troféu
    ENTER_NAME = 6  # Estado para inserir nome no ranking
    SHOW_RANKING = 7  # Estado para mostrar ranking

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
        
    def update(self, platforms, bullet_image=None, camera_x=0):
        # Aplicar gravidade
        self.vel_y += GRAVITY
        
        # Movimento horizontal
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0
            
        # Sistema de agachamento
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
            
        # Tiro com barra de espaço
        if keys[pygame.K_SPACE]:
            self.shoot(bullet_image)
            
        # Pulo (apenas com setas e WASD, não mais com espaço)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground and not self.is_crouching:
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
        self.state = GameState.PLAYING
        self.current_level = 1
        
        # Sistema de ranking
        self.ranking_manager = RankingManager()
        self.player_name = ""
        self.name_input_active = False
        self.max_levels = 5
        
        # Sistema de câmera
        self.camera_x = 0
        
        # Sistema de pontuação
        self.score = 0
        self.platforms_jumped = set()  # Conjunto para rastrear IDs de plataformas já pontuadas
        self.birds_dodged = set()  # Para rastrear pássaros já esquivados
        
        # Sistema de vidas
        self.lives = 3
        self.max_lives = 3
        
        # Sistema de pássaros
        self.birds = []
        
        # Sistema de explosões
        self.explosions = []
        self.bird_spawn_timer = 0
        
        # Ajustar dificuldade baseada no nível
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
        
        # Fonte para texto
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Carregar imagens
        self.load_images()
        
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
            
            # Carregar imagem do tiro
            self.bullet_img = pygame.image.load("imagens/elementos/tiro.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (15, 8))
            self.bullet_image = self.bullet_img  # Alias para compatibilidade
            
            # Carregar imagem da explosão
            self.explosion_img = pygame.image.load("imagens/elementos/explosao.png")
            self.explosion_img = pygame.transform.scale(self.explosion_img, (40, 40))
            self.explosion_image = self.explosion_img  # Alias para compatibilidade
            
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
        
    def init_level(self):
        """Inicializar o nível atual"""
        self.player = Player(50, HEIGHT - 200)
        self.platforms = []
        self.flag = None
        self.camera_x = 0
        # Reinicializar sistema de pássaros
        self.birds = []
        self.bird_spawn_timer = 0
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
                if self.state == GameState.ENTER_NAME:
                    # Capturar entrada de nome
                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            # Adicionar ao ranking e mostrar
                            self.ranking_manager.add_score(self.player_name.strip(), self.score)
                            self.state = GameState.SHOW_RANKING
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        # Adicionar caractere (limitado a 25)
                        if len(self.player_name) < 25 and event.unicode.isprintable():
                            self.player_name += event.unicode
                elif event.key == pygame.K_r and (self.state == GameState.GAME_OVER or self.state == GameState.VICTORY or self.state == GameState.SHOW_RANKING):
                    self.current_level = 1
                    self.score = 0  # Resetar pontuação
                    self.platforms_jumped.clear()  # Resetar plataformas pontuadas
                    self.birds_dodged.clear()  # Resetar pássaros esquivados
                    self.lives = self.max_lives  # Resetar vidas
                    self.player_name = ""  # Resetar nome
                    self.state = GameState.PLAYING
                    self.init_level()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def update(self):
        if self.state == GameState.PLAYING:
            # Atualizar jogador
            if not self.player.update(self.platforms, self.bullet_image, self.camera_x):
                self.lives -= 1
                if self.lives > 0:
                    # Ainda tem vidas, reiniciar fase atual
                    # Limpar plataformas pontuadas para permitir pontuação novamente
                    self.platforms_jumped.clear()
                    self.birds_dodged.clear()  # Limpar pássaros esquivados
                    self.init_level()
                else:
                    # Sem vidas, game over - verificar se entra no ranking
                    if self.ranking_manager.is_high_score(self.score):
                        self.state = GameState.ENTER_NAME
                    else:
                        self.state = GameState.GAME_OVER
                
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
        self.draw_ocean_background()
        
        if self.state == GameState.PLAYING:
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
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Pontuação Final: {self.score}", True, WHITE)
            restart_text = self.font.render("Pressione R para reiniciar", True, WHITE)
            
            # Centralizar textos corretamente
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
            restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
            
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
            restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
            self.screen.blit(restart_text, restart_rect)
            
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