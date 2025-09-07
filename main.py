import pygame
import sys
import math
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

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    VICTORY = 5  # Nova tela de vitória com troféu

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.original_height = 60
        self.crouched_height = 30
        self.height = self.original_height
        self.vel_x = 0
        self.vel_y = 0
        self.prev_vel_y = 0  # Velocidade anterior para detectar mudança
        self.on_ground = False
        self.just_landed = False  # Flag para detectar pouso
        self.is_crouching = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, platforms):
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
            
        # Pulo (não pode pular enquanto agachado)
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground and not self.is_crouching:
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
        self.just_landed = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Colisão por cima (jogador pousando na plataforma)
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    # Detectar se acabou de pousar (estava caindo e agora parou)
                    if self.prev_vel_y > 0:
                        self.just_landed = True
                    self.vel_y = 0
                    self.on_ground = True
                    self.rect.y = self.y
                    
        return True
    
    def draw(self, screen):
        # Desenhar jogador como um retângulo azul
        pygame.draw.rect(screen, BLUE, self.rect)
        # Adicionar detalhes simples
        if self.is_crouching:
            # Cabeça mais baixa quando agachado
            pygame.draw.circle(screen, WHITE, (int(self.x + self.width//2), int(self.y + 8)), 6)  # Cabeça menor
        else:
            # Cabeça normal
            pygame.draw.circle(screen, WHITE, (int(self.x + self.width//2), int(self.y + 15)), 8)  # Cabeça

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
            # Escalar a textura para o tamanho da plataforma
            scaled_texture = pygame.transform.scale(self.texture, (self.width, self.height))
            screen.blit(scaled_texture, (self.x, self.y))
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
        
    def draw(self, screen):
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
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.speed = 3
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # Atribuir ID único
        Bird._id_counter += 1
        self.id = Bird._id_counter
        
    def update(self):
        # Mover pássaro da direita para a esquerda
        self.x -= self.speed
        self.rect.x = self.x
        
        # Retornar True se ainda está na tela, False se saiu
        return self.x + self.width > 0
        
    def draw(self, screen):
        # Desenhar pássaro como um oval marrom
        pygame.draw.ellipse(screen, BROWN, self.rect)
        # Adicionar detalhes simples (asas)
        wing_y = self.y + 5
        pygame.draw.ellipse(screen, BLACK, (self.x + 5, wing_y, 8, 4))
        pygame.draw.ellipse(screen, BLACK, (self.x + 17, wing_y, 8, 4))
        # Bico
        pygame.draw.polygon(screen, YELLOW, [(self.x, self.y + 8), (self.x - 5, self.y + 10), (self.x, self.y + 12)])

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jogo de Plataforma - Mar")
        self.clock = pygame.time.Clock()
        self.state = GameState.PLAYING
        self.current_level = 1
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
        self.bird_spawn_timer = 0
        self.bird_spawn_interval = 180  # Spawn a cada 3 segundos (60 FPS * 3)
        
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
            self.background_img = pygame.image.load("imagens/fundo2.jpg")
            self.background_img = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))
            
            # Carregar imagem de objetos
            self.objects_img = pygame.image.load("imagens/objetos.jpg")
            
            # Extrair textura de plataforma (assumindo que está na parte superior esquerda)
            # Você pode ajustar estas coordenadas conforme necessário
            platform_rect = pygame.Rect(0, 0, 100, 30)  # Ajuste conforme a imagem
            self.platform_texture = self.objects_img.subsurface(platform_rect).copy()
            
        except pygame.error as e:
            print(f"Erro ao carregar imagens: {e}")
            # Fallback para cores sólidas se as imagens não carregarem
            self.background_img = None
            self.platform_texture = None
        
    def init_level(self):
        """Inicializar o nível atual"""
        self.player = Player(50, HEIGHT - 200)
        self.platforms = []
        self.flag = None
        self.camera_x = 0
        # Reinicializar sistema de pássaros
        self.birds = []
        self.bird_spawn_timer = 0
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
        """Nível 3 - Médio-Difícil (40 plataformas)"""
        platforms = [
            (100, HEIGHT - 200, 80, 20), (240, HEIGHT - 300, 80, 20), (380, HEIGHT - 180, 80, 20),
            (520, HEIGHT - 350, 80, 20), (660, HEIGHT - 220, 80, 20), (800, HEIGHT - 400, 80, 20),
            (940, HEIGHT - 150, 80, 20), (1080, HEIGHT - 320, 80, 20), (1220, HEIGHT - 180, 80, 20),
            (1360, HEIGHT - 380, 80, 20), (1500, HEIGHT - 240, 80, 20), (1640, HEIGHT - 140, 80, 20),
            (1780, HEIGHT - 360, 80, 20), (1920, HEIGHT - 200, 80, 20), (2060, HEIGHT - 420, 80, 20),
            (2200, HEIGHT - 160, 80, 20), (2340, HEIGHT - 340, 80, 20), (2480, HEIGHT - 220, 80, 20),
            (2620, HEIGHT - 120, 80, 20), (2760, HEIGHT - 380, 80, 20), (2900, HEIGHT - 180, 80, 20),
            (3040, HEIGHT - 400, 80, 20), (3180, HEIGHT - 240, 80, 20), (3320, HEIGHT - 140, 80, 20),
            (3460, HEIGHT - 360, 80, 20), (3600, HEIGHT - 200, 80, 20), (3740, HEIGHT - 440, 80, 20),
            (3880, HEIGHT - 160, 80, 20), (4020, HEIGHT - 320, 80, 20), (4160, HEIGHT - 220, 80, 20),
            (4300, HEIGHT - 120, 80, 20), (4440, HEIGHT - 380, 80, 20), (4580, HEIGHT - 180, 80, 20),
            (4720, HEIGHT - 420, 80, 20), (4860, HEIGHT - 240, 80, 20), (5000, HEIGHT - 140, 80, 20),
            (5140, HEIGHT - 360, 80, 20), (5280, HEIGHT - 200, 80, 20), (5420, HEIGHT - 460, 80, 20),
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
                if event.key == pygame.K_r and (self.state == GameState.GAME_OVER or self.state == GameState.VICTORY):
                    self.current_level = 1
                    self.score = 0  # Resetar pontuação
                    self.platforms_jumped.clear()  # Resetar plataformas pontuadas
                    self.birds_dodged.clear()  # Resetar pássaros esquivados
                    self.lives = self.max_lives  # Resetar vidas
                    self.state = GameState.PLAYING
                    self.init_level()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def update(self):
        if self.state == GameState.PLAYING:
            # Atualizar jogador
            if not self.player.update(self.platforms):
                self.lives -= 1
                if self.lives > 0:
                    # Ainda tem vidas, reiniciar fase atual
                    # Limpar plataformas pontuadas para permitir pontuação novamente
                    self.platforms_jumped.clear()
                    self.birds_dodged.clear()  # Limpar pássaros esquivados
                    self.init_level()
                else:
                    # Sem vidas, game over
                    self.state = GameState.GAME_OVER
                
            # Atualizar câmera para seguir o jogador
            target_camera_x = self.player.x - CAMERA_OFFSET_X
            if target_camera_x > self.camera_x:
                self.camera_x = target_camera_x
                
            # Sistema de pontuação - verificar se jogador pousou em nova plataforma
            if self.player.just_landed:
                for platform in self.platforms:
                    if (self.player.rect.colliderect(platform.rect) and 
                        platform.id not in self.platforms_jumped):
                        self.platforms_jumped.add(platform.id)
                        self.score += 10
                        break  # Só uma plataforma por pouso
                
            # Sistema de pássaros
            # Spawn de novos pássaros
            self.bird_spawn_timer += 1
            if self.bird_spawn_timer >= self.bird_spawn_interval:
                # Spawnar pássaro na altura aleatória
                import random
                bird_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                bird_x = WIDTH + self.camera_x + 50  # Spawnar fora da tela à direita
                self.birds.append(Bird(bird_x, bird_y))
                self.bird_spawn_timer = 0
            
            # Atualizar pássaros
            self.birds = [bird for bird in self.birds if bird.update()]
            
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
                    # Colidiu com pássaro, perder vida
                    self.birds.remove(bird)
                    self.lives -= 1
                    if self.lives > 0:
                        # Ainda tem vidas, reiniciar fase atual
                        # Limpar plataformas pontuadas para permitir pontuação novamente
                        self.platforms_jumped.clear()
                        self.birds_dodged.clear()  # Limpar pássaros esquivados
                        self.init_level()
                    else:
                        # Sem vidas, game over
                        self.state = GameState.GAME_OVER
                    break
            
            # Verificar se tocou a bandeira
            if self.player.rect.colliderect(self.flag.rect):
                if self.current_level < self.max_levels:
                    self.current_level += 1
                    self.init_level()
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
                    if platform.texture:
                        scaled_texture = pygame.transform.scale(platform.texture, (platform.width, platform.height))
                        self.screen.blit(scaled_texture, (adjusted_rect.x, adjusted_rect.y))
                    else:
                        pygame.draw.rect(self.screen, BROWN, adjusted_rect)
                
            # Desenhar bandeira com offset da câmera
            flag_x = self.flag.x - self.camera_x
            if flag_x > -50 and flag_x < WIDTH:  # Só desenhar se visível
                pygame.draw.rect(self.screen, YELLOW, (flag_x, self.flag.y, self.flag.width, self.flag.height))
                pygame.draw.polygon(self.screen, RED, [
                    (flag_x + 5, self.flag.y + 5),
                    (flag_x + 25, self.flag.y + 15),
                    (flag_x + 5, self.flag.y + 25)
                ])
            
            # Desenhar pássaros com offset da câmera
            for bird in self.birds:
                bird_x = bird.x - self.camera_x
                if bird_x > -50 and bird_x < WIDTH:  # Só desenhar se visível
                    bird_rect = pygame.Rect(bird_x, bird.y, bird.width, bird.height)
                    # Desenhar pássaro
                    pygame.draw.ellipse(self.screen, BROWN, bird_rect)
                    # Adicionar detalhes (asas)
                    wing_y = bird.y + 5
                    pygame.draw.ellipse(self.screen, BLACK, (bird_x + 5, wing_y, 8, 4))
                    pygame.draw.ellipse(self.screen, BLACK, (bird_x + 17, wing_y, 8, 4))
                    # Bico
                    pygame.draw.polygon(self.screen, YELLOW, [(bird_x, bird.y + 8), (bird_x - 5, bird.y + 10), (bird_x, bird.y + 12)])
            
            # Desenhar jogador com offset da câmera
            player_x = self.player.x - self.camera_x
            player_rect = pygame.Rect(player_x, self.player.y, self.player.width, self.player.height)
            pygame.draw.rect(self.screen, BLUE, player_rect)
            # Desenhar cabeça baseada no estado de agachamento
            if self.player.is_crouching:
                pygame.draw.circle(self.screen, WHITE, (int(player_x + self.player.width//2), int(self.player.y + 8)), 6)
            else:
                pygame.draw.circle(self.screen, WHITE, (int(player_x + self.player.width//2), int(self.player.y + 15)), 8)
            
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
            
            self.screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 100))
            self.screen.blit(score_text, (WIDTH//2 - 120, HEIGHT//2 - 30))
            self.screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 20))
            
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