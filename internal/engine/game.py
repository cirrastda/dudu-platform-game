import pygame
from internal.utils.constants import *
from internal.utils.functions import *
from internal.resources.cache import ResourceCache
from internal.engine.screen import Screen
from internal.engine.ranking import RankingManager
from internal.engine.state import GameState
from internal.resources.player import Player
from internal.resources.platform import Platform
from internal.resources.flag import Flag
from internal.resources.enemies.bird import Bird
from internal.resources.enemies.bat import Bat
from internal.resources.enemies.airplane import Airplane
from internal.resources.enemies.flying_disk import FlyingDisk
from internal.resources.enemies.turtle import Turtle
from internal.resources.enemies.spider import Spider
from internal.resources.enemies.robot import Robot
from internal.resources.enemies.alien import Alien
from internal.resources.bullet import Bullet
from internal.resources.explosion import Explosion
from internal.engine.level.level import Level
from internal.engine.level.generator.static import StaticLevelGenerator
from internal.engine.sound.music import Music
from internal.engine.sound.mixer import Mixer
from internal.engine.sound.effects import SoundEffects
from internal.resources.image import Image
from internal.engine.joystick import Joystick
from internal.engine.info import Info

# Carregar configurações
ENV_CONFIG = load_env_config()


class Game:
    def __init__(self):
        Screen.init(self)
        pygame.display.set_caption("Jump and Hit")
        self.clock = pygame.time.Clock()
        self.state = GameState.SPLASH

        # Configurar nível inicial baseado no ambiente
        if (
            ENV_CONFIG.get("environment") == "development"
            and "initial-stage" in ENV_CONFIG
        ):
            try:
                self.current_level = int(ENV_CONFIG["initial-stage"])
                # Validar se o nível está dentro do range válido
                if self.current_level < 1 or self.current_level > 50:
                    print(
                        f"Aviso: initial-stage {self.current_level} inválido. Usando nível 1."
                    )
                    self.current_level = 1
                else:
                    print(
                        f"Modo desenvolvimento: Iniciando no nível {self.current_level}"
                    )
            except (ValueError, TypeError):
                print("Aviso: initial-stage deve ser um número. Usando nível 1.")
                self.current_level = 1
        else:
            self.current_level = 1

        # Sistema de ranking
        self.ranking_manager = RankingManager()
        self.player_name = ""
        self.name_input_active = False
        self.max_levels = 50

        Mixer.init(pygame)

        # Sistema de música
        self.music = Music()
        self.music.start(self)
        self.sound_effects = SoundEffects()
        self.sound_effects.load_sound_effects()

        # Sistema de câmera
        self.camera_x = 0

        # Sistema de pontuação
        self.score = 0
        self.platforms_jumped = (
            set()
        )  # Conjunto para rastrear IDs de plataformas já pontuadas
        self.birds_dodged = set()  # Para rastrear pássaros já esquivados

        # Sistema de vidas
        self.lives = self.get_initial_lives()
        self.max_lives = self.get_initial_lives()

        # Sistema de vidas extras por pontuação
        self.extra_life_milestones = [1000, 5000, 10000]  # Marcos iniciais
        self.next_extra_life_score = 1000  # Próxima pontuação para vida extra
        self.extra_lives_earned = 0  # Contador de vidas extras ganhas

        # Sistema de joystick
        Joystick.init(self)

        # Sistema de splash screen e menu
        self.splash_timer = 0
        self.splash_duration = 360  # 6 segundos (60 FPS * 6)
        self.current_logo_index = 0
        self.logo_display_time = 120  # Tempo para cada logo (2 segundos)
        self.logos = []  # Lista de logos para splash
        self.menu_selected = 0  # Opção selecionada no menu
        self.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
        self.game_logo = None  # Logo principal do jogo

        # Efeitos de fade para splash screen
        self.fade_in_duration = 30  # 0.5 segundos para fade in
        self.fade_out_duration = 30  # 0.5 segundos para fade out
        self.logo_hold_time = 60  # 1 segundo para mostrar o logo
        self.music_started = False  # Controla se a música já foi iniciada

        # Controle de eixos do joystick para D-pad e analógicos
        self.prev_dpad_vertical = 0
        self.prev_dpad_horizontal = 0
        self.prev_analog_vertical = 0
        self.prev_analog_horizontal = 0

        # Sistema de menu de game over
        self.game_over_selected = 0  # Opção selecionada no menu de game over
        self.game_over_options = ["Jogar novamente", "Recordes", "Sair"]

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

        # Inicializar variáveis de spawn de morcegos (níveis 21-30)
        self.bats = []
        self.bat_spawn_timer = 0
        self.bats_per_spawn = 1
        self.bat_spawn_interval = 180

        # Inicializar variáveis de spawn de aviões (níveis 31+)
        self.airplanes = []
        self.airplane_spawn_timer = 0
        self.airplanes_per_spawn = 1
        self.airplane_spawn_interval = 150

        # Inicializar variáveis de flying-disk (níveis 41-50)
        self.flying_disks = []
        self.flying_disk_spawn_timer = 0
        self.flying_disks_per_spawn = 1
        self.flying_disk_spawn_interval = 150

        # Inicializar variáveis de robôs (níveis 31-40)
        self.robots = []
        self.orphan_missiles = (
            []
        )  # Mísseis de robôs mortos que continuam visíveis mas sem hitbox

        # Inicializar variáveis de aliens (níveis 41-50)
        self.aliens = []
        self.orphan_lasers = []  # Lasers de aliens mortos que continuam visíveis mas sem hitbox

        # Ajustar dificuldade baseada no nível
        self.birds_per_spawn = Level.get_birds_per_spawn(self.current_level)
        self.bird_spawn_interval = Level.get_bird_spawn_interval(self.current_level)

        # Fonte para texto
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        # Carregar imagens
        Image.load_images(self)

        # Se estiver em modo desenvolvimento e iniciando em uma fase específica,
        # pular para o estado PLAYING e tocar música do nível
        if (
            ENV_CONFIG.get("environment") == "development"
            and "initial-stage" in ENV_CONFIG
            and self.current_level > 1
        ):
            self.state = GameState.PLAYING
            self.score = 0
            self.platforms_jumped = set()
            self.birds_dodged = set()
            self.lives = self.max_lives
            self.player_name = ""
            Level.init_level(self)
            self.music.play_level_music(self, self.current_level)
        else:
            Level.init_level(self)

    def get_initial_lives(self):
        """Obter o número inicial de vidas baseado na configuração"""
        if ENV_CONFIG.get("environment") == "development" and "lives" in ENV_CONFIG:
            if ENV_CONFIG.get("lives").isdigit() and int(ENV_CONFIG.get("lives")) > 0:
                return int(ENV_CONFIG["lives"])

        return DEFAULT_INITIAL_LIVES  # Valor padrão se não houver configuração válida

    def check_extra_life(self):
        """Verificar se o jogador merece uma vida extra baseada na pontuação"""
        if self.score >= self.next_extra_life_score:
            # Conceder vida extra
            self.lives += 1
            self.extra_lives_earned += 1

            # Tocar som de vida extra
            self.sound_effects.play_sound_effect(
                "new-life"
            )  # Som específico para vida extra

            # Calcular próxima pontuação para vida extra
            if self.extra_lives_earned <= 3:  # Primeiros 3 marcos: 1000, 5000, 10000
                if self.extra_lives_earned < len(self.extra_life_milestones):
                    self.next_extra_life_score = self.extra_life_milestones[
                        self.extra_lives_earned
                    ]
                else:
                    # Após 10000, a cada 10000 pontos
                    self.next_extra_life_score = 20000
            else:
                # A cada 10000 pontos após os marcos iniciais
                self.next_extra_life_score += 10000

            return True  # Indica que uma vida extra foi concedida
        return False

    def update_bird_difficulty(self):
        """Atualizar dificuldade dos pássaros baseada no nível atual
        Progressão gradual e jogável de 1-20 níveis
        """
        if self.current_level <= 20:
            self.birds_per_spawn = Level.get_birds_per_spawn(self.current_level)
            self.bird_spawn_interval = Level.get_bird_spawn_interval(self.current_level)
        elif self.current_level <= 30:
            self.bats_per_spawn = Level.get_birds_per_spawn(self.current_level)
            self.bat_spawn_interval = Level.get_bird_spawn_interval(self.current_level)
        else:
            self.birds_per_spawn = Level.get_birds_per_spawn(self.current_level)
            self.bird_spawn_interval = Level.get_bird_spawn_interval(self.current_level)

    def get_pooled_bullet(self, x, y, direction=1, image=None):
        """Obter bala do pool ou criar nova se necessário"""
        if self.bullet_pool:
            bullet = self.bullet_pool.pop()
            bullet.x = x
            bullet.y = y
            bullet.direction = direction
            bullet.image = image
            bullet.rect.x = x
            bullet.rect.y = y
            return bullet
        else:
            return Bullet(x, y, direction, image)

    def return_bullet_to_pool(self, bullet):
        """Retornar bala ao pool"""
        if len(self.bullet_pool) < 20:  # Limitar tamanho do pool
            self.bullet_pool.append(bullet)

    def get_pooled_explosion(self, x, y, image=None):
        """Obter explosão do pool ou criar nova se necessário"""
        if self.explosion_pool:
            explosion = self.explosion_pool.pop()
            explosion.x = x
            explosion.y = y
            explosion.image = image
            explosion.timer = 30  # Resetar timer para duração completa
            return explosion
        else:
            return Explosion(x, y, image)

    def return_explosion_to_pool(self, explosion):
        """Retornar explosão ao pool"""
        if len(self.explosion_pool) < 10:  # Limitar tamanho do pool
            self.explosion_pool.append(explosion)

    def draw_ocean_background(self):
        """Desenhar fundo do mar"""
        # Determinar qual fundo usar baseado no estado do jogo
        if self.state == GameState.PLAYING:
            # Durante o jogo, usar fundo baseado no nível
            background_to_use = self.background_img
        else:
            # Em menus, recordes, etc., usar fundo fixo
            background_to_use = getattr(
                self, "menu_background_img", self.background_img
            )

        if background_to_use:
            # Usar imagem de fundo
            self.screen.blit(background_to_use, (0, 0))
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
                    if ENV_CONFIG.get("environment", "production") == "development":
                        self.state = GameState.MAIN_MENU
                        # Iniciar música do menu quando pular para o menu
                        if not self.music_started:
                            self.music.play_menu_music(self)
                            self.music_started = True
                # Navegação do menu principal
                elif self.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(
                            self.menu_options
                        )
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
                        self.game_over_selected = (self.game_over_selected - 1) % len(
                            self.game_over_options
                        )
                    elif event.key == pygame.K_DOWN:
                        self.game_over_selected = (self.game_over_selected + 1) % len(
                            self.game_over_options
                        )
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.game_over_selected == 0:  # Jogar novamente
                            # Configurar nível inicial baseado no ambiente
                            if (
                                ENV_CONFIG.get("environment") == "development"
                                and "initial-stage" in ENV_CONFIG
                            ):
                                try:
                                    self.current_level = int(
                                        ENV_CONFIG["initial-stage"]
                                    )
                                    # Validar se o nível está dentro do range válido
                                    if (
                                        self.current_level < 1
                                        or self.current_level > 50
                                    ):
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
                            Level.init_level(self)
                            # Tocar música do nível atual
                            self.music.play_level_music(self, self.current_level)
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
                            self.ranking_manager.add_score(
                                self.player_name.strip(), self.score
                            )
                            # Salvar o estado anterior antes de ir para SHOW_RANKING
                            self.previous_state_before_ranking = GameState.GAME_OVER
                            self.state = GameState.SHOW_RANKING
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        # Adicionar caractere (limitado a 25)
                        if len(self.player_name) < 25 and event.unicode.isprintable():
                            self.player_name += event.unicode
                elif event.key == pygame.K_r and (
                    self.state == GameState.VICTORY
                    or self.state == GameState.SHOW_RANKING
                ):
                    # Configurar nível inicial baseado no ambiente
                    if (
                        ENV_CONFIG.get("environment") == "development"
                        and "initial-stage" in ENV_CONFIG
                    ):
                        try:
                            self.current_level = int(ENV_CONFIG["initial-stage"])
                            # Validar se o nível está dentro do range válido
                            if self.current_level < 1 or self.current_level > 50:
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
                    Level.init_level(
                        self
                    )  # Inicializar o nível para posicionar jogador corretamente
                    # Tocar música do nível atual
                    self.music.play_level_music(self, self.current_level)
                elif (
                    event.key == pygame.K_ESCAPE
                    and self.state == GameState.SHOW_RANKING
                ):
                    # Voltar ao estado anterior (GAME_OVER ou VICTORY)
                    if self.previous_state_before_ranking:
                        self.state = self.previous_state_before_ranking
                        self.previous_state_before_ranking = None
                    else:
                        self.state = GameState.GAME_OVER  # Fallback
                    Level.init_level(self)
                elif event.key == pygame.K_ESCAPE:
                    return False

            # Eventos do joystick
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.joystick_connected:
                    # Navegação do splash screen com joystick
                    if self.state == GameState.SPLASH:
                        # Só permite pular se estiver em modo development
                        if ENV_CONFIG.get("environment", "production") == "development":
                            self.state = GameState.MAIN_MENU
                            # Iniciar música do menu quando pular para o menu
                            if not self.music_started:
                                self.music.play_menu_music(self)
                                self.music_started = True
                    # Navegação do menu principal com joystick
                    elif self.state == GameState.MAIN_MENU:
                        if event.button == 0 or event.button in [
                            6,
                            7,
                            8,
                            9,
                        ]:  # A/X ou Start/Options
                            self.handle_menu_selection()
                    # Navegação das telas de créditos e recordes com joystick
                    elif self.state == GameState.CREDITS:
                        if event.button == 1 or event.button in [
                            6,
                            7,
                            8,
                            9,
                        ]:  # B/Círculo ou Start/Options
                            self.state = GameState.MAIN_MENU
                    elif self.state == GameState.RECORDS:
                        if event.button == 1 or event.button in [
                            6,
                            7,
                            8,
                            9,
                        ]:  # B/Círculo ou Start/Options
                            # Voltar ao estado anterior (MAIN_MENU ou GAME_OVER)
                            if self.previous_state_before_records:
                                self.state = self.previous_state_before_records
                                self.previous_state_before_records = None
                            else:
                                self.state = GameState.MAIN_MENU  # Fallback
                    # Navegação do menu de game over com joystick
                    elif self.state == GameState.GAME_OVER:
                        if event.button == 0 or event.button in [
                            6,
                            7,
                            8,
                            9,
                        ]:  # A/X ou Start/Options
                            if self.game_over_selected == 0:  # Jogar novamente
                                # Configurar nível inicial baseado no ambiente
                                if (
                                    ENV_CONFIG.get("environment") == "development"
                                    and "initial-stage" in ENV_CONFIG
                                ):
                                    try:
                                        self.current_level = int(
                                            ENV_CONFIG["initial-stage"]
                                        )
                                        # Validar se o nível está dentro do range válido
                                        if (
                                            self.current_level < 1
                                            or self.current_level > 50
                                        ):
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
                                Level.init_level(self)
                                # Tocar música do nível atual
                                self.music.play_level_music(self, self.current_level)
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
                    elif event.button in [
                        6,
                        7,
                        8,
                        9,
                    ]:  # Start/Options (varia entre drivers)
                        if self.state == GameState.ENTER_NAME:
                            # Confirmar entrada de nome (equivalente ao ENTER)
                            if self.player_name.strip():
                                self.ranking_manager.add_score(
                                    self.player_name.strip(), self.score
                                )
                                # Salvar o estado anterior antes de ir para SHOW_RANKING
                                self.previous_state_before_ranking = GameState.GAME_OVER
                                self.state = GameState.SHOW_RANKING
                        elif (
                            self.state == GameState.GAME_OVER
                            or self.state == GameState.VICTORY
                            or self.state == GameState.SHOW_RANKING
                        ):
                            # Reiniciar jogo (equivalente ao R)
                            # Configurar nível inicial baseado no ambiente
                            if (
                                ENV_CONFIG.get("environment") == "development"
                                and "initial-stage" in ENV_CONFIG
                            ):
                                try:
                                    self.current_level = int(
                                        ENV_CONFIG["initial-stage"]
                                    )
                                    # Validar se o nível está dentro do range válido
                                    if (
                                        self.current_level < 1
                                        or self.current_level > 50
                                    ):
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
                            Level.init_level(self)
                    # Botão B para voltar do ranking
                    elif (
                        event.button == 1 and self.state == GameState.SHOW_RANKING
                    ):  # Botão B
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
                analog_vertical = self.joystick.get_axis(
                    1
                )  # Eixo Y do analógico esquerdo
                # Aplicar zona morta para evitar drift
                if abs(analog_vertical) < 0.1:
                    analog_vertical = 0

            if self.joystick.get_numaxes() >= 1:
                analog_horizontal = self.joystick.get_axis(
                    0
                )  # Eixo X do analógico esquerdo
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
                    self.menu_selected = (self.menu_selected - 1) % len(
                        self.menu_options
                    )
                elif self.state == GameState.GAME_OVER:
                    self.game_over_selected = (self.game_over_selected - 1) % len(
                        self.game_over_options
                    )

            # Navegação para baixo (analógico ou D-pad)
            elif analog_down or dpad_down:
                if self.state == GameState.MAIN_MENU:
                    self.menu_selected = (self.menu_selected + 1) % len(
                        self.menu_options
                    )
                elif self.state == GameState.GAME_OVER:
                    self.game_over_selected = (self.game_over_selected + 1) % len(
                        self.game_over_options
                    )

            # Atualizar valores anteriores
            self.prev_analog_vertical = analog_vertical
            self.prev_analog_horizontal = analog_horizontal
            self.prev_dpad_vertical = dpad_vertical
            self.prev_dpad_horizontal = dpad_horizontal

        return True

    def handle_menu_selection(self):
        """Processar seleção do menu principal"""
        selected_option = self.menu_options[self.menu_selected]

        if selected_option == "Iniciar":
            # Iniciar novo jogo
            # Configurar nível inicial baseado no ambiente
            if (
                ENV_CONFIG.get("environment") == "development"
                and "initial-stage" in ENV_CONFIG
            ):
                try:
                    self.current_level = int(ENV_CONFIG["initial-stage"])
                    # Validar se o nível está dentro do range válido
                    if self.current_level < 1 or self.current_level > 50:
                        print(
                            f"Aviso: initial-stage {self.current_level} inválido. Usando nível 1."
                        )
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
            Level.init_level(self)
            # Tocar música do nível atual
            self.music.play_level_music(self, self.current_level)
        elif selected_option == "Recordes":
            self.state = GameState.RECORDS
        elif selected_option == "Créditos":
            self.state = GameState.CREDITS
        elif selected_option == "Sair":
            pygame.quit()
            sys.exit()

    def update(self):
        if self.state == GameState.SPLASH:
            # Atualizar timer do splash screen
            self.splash_timer += 1

            # Calcular qual logo mostrar baseado no tempo com fade
            if self.logos:
                self.current_logo_index = (
                    self.splash_timer // self.logo_display_time
                ) % len(self.logos)

            # Após o tempo total, ir para o menu
            if self.splash_timer >= self.splash_duration:
                self.state = GameState.MAIN_MENU
                # Iniciar música do menu quando aparecer o menu
                if not self.music_started:
                    self.music.play_menu_music(self)
                    self.music_started = True

        elif self.state == GameState.PLAYING:
            # Atualizar jogador
            player_action = self.player.update(
                self.platforms,
                self.bullet_image,
                self.camera_x,
                self.joystick if self.joystick_connected else None,
                self,
            )

            # Verificar ações do jogador e tocar sons
            if player_action == "jump":
                self.sound_effects.play_sound_effect("jump")
            elif player_action == "shot":
                self.sound_effects.play_sound_effect("shot")

            # Verificar se jogador morreu (retorno False)
            if player_action is False:
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
                    Level.init_level(self)
                    # Tocar música do nível atual
                    self.music.play_level_music(self, self.current_level)

            # Atualizar câmera para seguir o jogador
            target_camera_x = self.player.x - CAMERA_OFFSET_X
            if target_camera_x > self.camera_x:
                self.camera_x = target_camera_x

            # Sistema de pontuação - verificar se jogador pousou em nova plataforma
            if self.player.just_landed and hasattr(self.player, "landed_platform_id"):
                if self.player.landed_platform_id not in self.platforms_jumped:
                    self.platforms_jumped.add(self.player.landed_platform_id)
                    self.score += 10
                    # Verificar se merece vida extra
                    self.check_extra_life()
                # Reset da flag após verificar pontuação
                self.player.just_landed = False
                delattr(self.player, "landed_platform_id")

            # Sistema de pássaros e morcegos
            if self.current_level <= 20:
                # Spawn de novos pássaros (níveis 1-20)
                self.bird_spawn_timer += 1
                if self.bird_spawn_timer >= self.bird_spawn_interval:
                    # Spawnar múltiplos pássaros baseado no nível
                    import random

                    for i in range(self.birds_per_spawn):
                        bird_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        # Spawn sempre à direita da tela visível, independente da posição da câmera
                        bird_x = (
                            self.camera_x + WIDTH + 50 + (i * 100)
                        )  # Espaçar pássaros
                        bird_images = (
                            (self.bird_img1, self.bird_img2)
                            if hasattr(self, "bird_img1")
                            else None
                        )
                        self.birds.append(Bird(bird_x, bird_y, bird_images))
                    self.bird_spawn_timer = 0
            elif self.current_level <= 30:
                # Spawn de novos morcegos (níveis 21-30)
                self.bat_spawn_timer += 1
                if self.bat_spawn_timer >= self.bat_spawn_interval:
                    # Spawnar múltiplos morcegos baseado no nível
                    import random

                    for i in range(self.bats_per_spawn):
                        bat_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        # Spawn sempre à direita da tela visível, independente da posição da câmera
                        bat_x = (
                            self.camera_x + WIDTH + 50 + (i * 100)
                        )  # Espaçar morcegos
                        bat_images = (
                            (self.bat_img1, self.bat_img2, self.bat_img3)
                            if hasattr(self, "bat_img1")
                            else None
                        )
                        self.bats.append(Bat(bat_x, bat_y, bat_images))
                    self.bat_spawn_timer = 0
            elif self.current_level <= 40:
                # Spawn de novos aviões (níveis 31-40)
                self.airplane_spawn_timer += 1
                if self.airplane_spawn_timer >= self.airplane_spawn_interval:
                    # Spawnar múltiplos aviões baseado no nível
                    import random

                    for i in range(self.airplanes_per_spawn):
                        airplane_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        # Spawn sempre à direita da tela visível, independente da posição da câmera
                        airplane_x = (
                            self.camera_x + WIDTH + 50 + (i * 120)
                        )  # Espaçar aviões um pouco mais
                        airplane_images = (
                            (self.airplane_img1, self.airplane_img2, self.airplane_img3)
                            if hasattr(self, "airplane_img1")
                            else None
                        )
                        self.airplanes.append(
                            Airplane(airplane_x, airplane_y, airplane_images)
                        )
                    self.airplane_spawn_timer = 0
            else:
                # Spawn de novos flying-disks (níveis 41-50)
                self.flying_disk_spawn_timer += 1
                if self.flying_disk_spawn_timer >= self.flying_disk_spawn_interval:
                    # Spawnar múltiplos flying-disks baseado no nível
                    import random

                    for i in range(self.flying_disks_per_spawn):
                        disk_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        # Spawn à direita da tela visível
                        disk_x = self.camera_x + WIDTH + 50 + (i * 120)
                        disk_images = (
                            self.flying_disk_images if hasattr(self, "flying_disk_images") else None
                        )
                        self.flying_disks.append(FlyingDisk(disk_x, disk_y, disk_images))
                    self.flying_disk_spawn_timer = 0

            # Atualizar pássaros, morcegos e aviões com culling (remover objetos muito distantes da câmera)
            if self.current_level <= 20:
                visible_birds = []
                for bird in self.birds:
                    if bird.update():
                        # Culling: manter apenas pássaros próximos à área visível
                        if (
                            bird.x > self.camera_x - 200
                            and bird.x < self.camera_x + WIDTH + 200
                        ):
                            visible_birds.append(bird)
                self.birds = visible_birds
            elif self.current_level <= 30:
                visible_bats = []
                for bat in self.bats:
                    if bat.update(self.camera_x):
                        # Culling: manter apenas morcegos próximos à área visível
                        if (
                            bat.x > self.camera_x - 200
                            and bat.x < self.camera_x + WIDTH + 200
                        ):
                            visible_bats.append(bat)
                self.bats = visible_bats
            elif self.current_level <= 40:
                visible_airplanes = []
                for airplane in self.airplanes:
                    if airplane.update(self.camera_x):
                        # Culling: manter apenas aviões próximos à área visível
                        if (
                            airplane.x > self.camera_x - 200
                            and airplane.x < self.camera_x + WIDTH + 200
                        ):
                            visible_airplanes.append(airplane)
                self.airplanes = visible_airplanes
            else:
                visible_disks = []
                for disk in self.flying_disks:
                    if disk.update(self.camera_x):
                        # Culling: manter apenas discos próximos à área visível
                        if (
                            disk.x > self.camera_x - 200
                            and disk.x < self.camera_x + WIDTH + 200
                        ):
                            visible_disks.append(disk)
                self.flying_disks = visible_disks

            # Atualizar tartarugas e aranhas com culling
            if self.current_level <= 20:
                for turtle in self.turtles:
                    # Culling: só atualizar tartarugas próximas à área visível
                    if (
                        turtle.x > self.camera_x - 100
                        and turtle.x < self.camera_x + WIDTH + 100
                    ):
                        turtle.update()
            else:
                for spider in self.spiders:
                    # Culling: só atualizar aranhas próximas à área visível
                    if (
                        spider.x > self.camera_x - 100
                        and spider.x < self.camera_x + WIDTH + 100
                    ):
                        spider.update()

            # Atualizar robôs (níveis 31-40)
            if 31 <= self.current_level <= 40:
                for robot in self.robots:
                    # Atualizar todos os robôs para manter o sistema de tiro ativo
                    # passando a posição da câmera para remoção correta dos mísseis
                    robot.update(self.camera_x)

            # Atualizar aliens (níveis 41-50)
            if 41 <= self.current_level <= 50:
                for alien in self.aliens:
                    # Atualizar todos os aliens para manter o sistema de tiro ativo
                    alien.update(self.camera_x)

            # Atualizar explosões com pool
            active_explosions = []
            for explosion in self.explosions:
                if explosion.update():
                    active_explosions.append(explosion)
                else:
                    # Retornar explosão ao pool
                    self.return_explosion_to_pool(explosion)
            self.explosions = active_explosions

            # Verificar colisão entre tiros e pássaros/morcegos/aviões/discos
            if self.current_level <= 20:
                for bullet in self.player.bullets[:]:
                    for bird in self.birds[:]:
                        if bullet.rect.colliderect(bird.rect):
                            # Tiro acertou pássaro
                            self.player.bullets.remove(bullet)
                            self.birds.remove(bird)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                bird.x, bird.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += (
                                100  # Aviões valem mais pontos por serem maiores
                            )
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break
            elif self.current_level <= 30:
                for bullet in self.player.bullets[:]:
                    for bat in self.bats[:]:
                        if bullet.rect.colliderect(bat.rect):
                            # Tiro acertou morcego
                            self.player.bullets.remove(bullet)
                            self.bats.remove(bat)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                bat.x, bat.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += 75  # Morcegos valem mais pontos
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break
            elif self.current_level <= 40:
                for bullet in self.player.bullets[:]:
                    for airplane in self.airplanes[:]:
                        if bullet.rect.colliderect(airplane.rect):
                            # Tiro acertou avião
                            self.player.bullets.remove(bullet)
                            self.airplanes.remove(airplane)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                airplane.x, airplane.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += 50
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break
            else:
                for bullet in self.player.bullets[:]:
                    for disk in self.flying_disks[:]:
                        if bullet.rect.colliderect(disk.rect):
                            # Tiro acertou flying-disk
                            self.player.bullets.remove(bullet)
                            self.flying_disks.remove(disk)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                disk.x, disk.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += 90
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break

            # Verificar colisão entre tiros e tartarugas/aranhas
            if self.current_level <= 20:
                for bullet in self.player.bullets[:]:
                    for turtle in self.turtles[:]:
                        if bullet.rect.colliderect(turtle.rect):
                            # Tiro acertou tartaruga
                            self.player.bullets.remove(bullet)
                            self.turtles.remove(turtle)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                turtle.x, turtle.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += 60
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break
            else:
                for bullet in self.player.bullets[:]:
                    for spider in self.spiders[:]:
                        if bullet.rect.colliderect(spider.rect):
                            # Tiro acertou aranha
                            self.player.bullets.remove(bullet)
                            self.spiders.remove(spider)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                spider.x, spider.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += 60
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break

            # Verificar colisão entre tiros do jogador e robôs (níveis 31-40)
            if 31 <= self.current_level <= 40:
                for bullet in self.player.bullets[:]:
                    for robot in self.robots[:]:
                        if bullet.rect.colliderect(robot.rect):
                            # Tiro acertou robô
                            self.player.bullets.remove(bullet)
                            # Transferir mísseis ativos do robô para a lista de órfãos
                            for missile in robot.missiles:
                                self.orphan_missiles.append(missile)
                            self.robots.remove(robot)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                robot.x, robot.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += (
                                80  # Robôs valem mais pontos por serem mais difíceis
                            )
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break

            # Verificar colisão entre mísseis dos robôs e jogador (níveis 31-40)
            if 31 <= self.current_level <= 40:
                for robot in self.robots[:]:
                    for missile in robot.missiles[:]:
                        if self.player.rect.colliderect(missile.rect):
                            if self.player.is_invulnerable:
                                # Jogador invulnerável: explodir míssil sem causar dano
                                explosion = self.get_pooled_explosion(
                                    missile.x, missile.y, self.explosion_image
                                )
                                self.explosions.append(explosion)
                                robot.missiles.remove(missile)
                                self.score += 15  # Pontos bônus por destruir míssil durante invulnerabilidade
                                # Verificar se merece vida extra
                                self.check_extra_life()
                            else:
                                # Colidiu com míssil, ativar animação de hit
                                if (
                                    not self.player.is_hit
                                ):  # Só aplicar hit se não estiver já em estado de hit
                                    self.player.take_hit()
                                    # Criar explosão na posição do míssil
                                    explosion = self.get_pooled_explosion(
                                        missile.x, missile.y, self.explosion_image
                                    )
                                    self.explosions.append(explosion)
                                    robot.missiles.remove(missile)
                                    self.lives -= 1
                                    if self.lives <= 0:
                                        # Sem vidas, game over - verificar se entra no ranking
                                        if self.ranking_manager.is_high_score(
                                            self.score
                                        ):
                                            self.state = GameState.ENTER_NAME
                                        else:
                                            self.state = GameState.GAME_OVER
                                    # Não reiniciar o nível imediatamente, deixar o jogador continuar
                            break

            # Verificar colisão entre lasers dos aliens e jogador (níveis 41-50)
            if 41 <= self.current_level <= 50:
                for alien in self.aliens[:]:
                    for laser in alien.lasers[:]:
                        if self.player.rect.colliderect(laser.rect):
                            if self.player.is_invulnerable:
                                # Jogador invulnerável: explodir laser sem causar dano
                                explosion = self.get_pooled_explosion(
                                    laser.x, laser.y, self.explosion_image
                                )
                                self.explosions.append(explosion)
                                alien.lasers.remove(laser)
                                self.score += 15  # Pontos bônus por destruir laser durante invulnerabilidade
                                # Verificar se merece vida extra
                                self.check_extra_life()
                            else:
                                # Colidiu com laser, ativar animação de hit
                                if not self.player.is_hit:
                                    self.player.take_hit()
                                    # Criar explosão na posição do laser
                                    explosion = self.get_pooled_explosion(
                                        laser.x, laser.y, self.explosion_image
                                    )
                                    self.explosions.append(explosion)
                                    alien.lasers.remove(laser)
                                    self.lives -= 1
                                    if self.lives <= 0:
                                        # Sem vidas, game over - verificar se entra no ranking
                                        if self.ranking_manager.is_high_score(
                                            self.score
                                        ):
                                            self.state = GameState.ENTER_NAME
                                        else:
                                            self.state = GameState.GAME_OVER
                                    # Não reiniciar o nível imediatamente, deixar o jogador continuar
                            break

            # Verificar colisão entre tiros e aliens (níveis 41-50)
            if 41 <= self.current_level <= 50:
                for bullet in self.player.bullets[:]:
                    for alien in self.aliens[:]:
                        if bullet.rect.colliderect(alien.rect):
                            # Tiro acertou alien
                            self.player.bullets.remove(bullet)
                            # Transferir lasers ativos do alien para a lista de órfãos
                            for laser in alien.lasers:
                                self.orphan_lasers.append(laser)
                            self.aliens.remove(alien)
                            # Criar explosão usando pool
                            explosion = self.get_pooled_explosion(
                                alien.x, alien.y, self.explosion_image
                            )
                            self.explosions.append(explosion)
                            # Retornar bala ao pool
                            self.return_bullet_to_pool(bullet)
                            # Tocar som de explosão
                            self.sound_effects.play_sound_effect("explosion")
                            # Adicionar pontos
                            self.score += 80
                            # Verificar se merece vida extra
                            self.check_extra_life()
                            break

            # Atualizar mísseis órfãos (de robôs mortos) - apenas visual, sem colisão
            if 31 <= self.current_level <= 40:
                active_orphan_missiles = []
                for missile in self.orphan_missiles:
                    if missile.update(self.camera_x):
                        active_orphan_missiles.append(missile)
                self.orphan_missiles = active_orphan_missiles

            # Atualizar lasers órfãos (de aliens mortos) - apenas visual, sem colisão
            if 41 <= self.current_level <= 50:
                active_orphan_lasers = []
                for laser in self.orphan_lasers:
                    if laser.update(self.camera_x):
                        active_orphan_lasers.append(laser)
                self.orphan_lasers = active_orphan_lasers

            # Verificar colisão e esquiva com pássaros, morcegos, aviões e discos
            if self.current_level <= 20:
                for bird in self.birds[:]:
                    # Verificar se pássaro passou perto do jogador (esquiva)
                    distance_x = abs(bird.x - self.player.x)
                    distance_y = abs(bird.y - self.player.y)

                    # Se pássaro passou perto (dentro de 40 pixels) e já passou do jogador
                    if (
                        distance_x < 40
                        and distance_y < 50
                        and bird.x < self.player.x
                        and bird.id not in self.birds_dodged
                    ):
                        self.birds_dodged.add(bird.id)
                        self.score += 10  # Pontos por esquivar
                        # Verificar se merece vida extra
                        self.check_extra_life()

                    # Verificar colisão direta
                    if self.player.rect.colliderect(bird.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(bird.x, bird.y, self.explosion_image)
                            )
                            self.birds.remove(bird)
                            self.score += 20  # Pontos bônus por destruir inimigo durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com pássaro, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição do pássaro
                                self.explosions.append(
                                    Explosion(bird.x, bird.y, self.explosion_image)
                                )
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
            elif self.current_level <= 30:
                for bat in self.bats[:]:
                    # Verificar se morcego passou perto do jogador (esquiva)
                    distance_x = abs(bat.x - self.player.x)
                    distance_y = abs(bat.y - self.player.y)

                    # Se morcego passou perto (dentro de 40 pixels) e já passou do jogador
                    if (
                        distance_x < 40
                        and distance_y < 50
                        and bat.x < self.player.x
                        and bat.id not in self.birds_dodged
                    ):
                        self.birds_dodged.add(bat.id)
                        self.score += 15  # Pontos por esquivar morcego (mais difícil)
                        # Verificar se merece vida extra
                        self.check_extra_life()

                    # Verificar colisão direta
                    if self.player.rect.colliderect(bat.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(bat.x, bat.y, self.explosion_image)
                            )
                            self.bats.remove(bat)
                            self.score += 25  # Pontos bônus por destruir morcego durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com morcego, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição do morcego
                                self.explosions.append(
                                    Explosion(bat.x, bat.y, self.explosion_image)
                                )
                                self.bats.remove(bat)
                                self.lives -= 1
                                if self.lives <= 0:
                                    # Sem vidas, game over - verificar se entra no ranking
                                    if self.ranking_manager.is_high_score(self.score):
                                        self.state = GameState.ENTER_NAME
                                    else:
                                        self.state = GameState.GAME_OVER
                                # Não reiniciar o nível imediatamente, deixar o jogador continuar
                        break
            elif self.current_level <= 40:
                for airplane in self.airplanes[:]:
                    # Verificar se avião passou perto do jogador (esquiva)
                    distance_x = abs(airplane.x - self.player.x)
                    distance_y = abs(airplane.y - self.player.y)

                    # Se avião passou perto (dentro de 50 pixels) e já passou do jogador
                    if (
                        distance_x < 50
                        and distance_y < 60
                        and airplane.x < self.player.x
                        and airplane.id not in self.birds_dodged
                    ):
                        self.birds_dodged.add(airplane.id)
                        self.score += 20  # Pontos por esquivar avião (mais difícil)
                        # Verificar se merece vida extra
                        self.check_extra_life()

                    # Verificar colisão direta
                    if self.player.rect.colliderect(airplane.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(airplane.x, airplane.y, self.explosion_image)
                            )
                            self.airplanes.remove(airplane)
                            self.score += 30  # Pontos bônus por destruir avião durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com avião, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição do avião
                                self.explosions.append(
                                    Explosion(
                                        airplane.x, airplane.y, self.explosion_image
                                    )
                                )
                                self.airplanes.remove(airplane)
                                self.lives -= 1
                                if self.lives <= 0:
                                    # Sem vidas, game over - verificar se entra no ranking
                                    if self.ranking_manager.is_high_score(self.score):
                                        self.state = GameState.ENTER_NAME
                                    else:
                                        self.state = GameState.GAME_OVER
                                # Não reiniciar o nível imediatamente, deixar o jogador continuar
                        break
            else:
                for disk in self.flying_disks[:]:
                    # Verificar se disco passou perto do jogador (esquiva)
                    distance_x = abs(disk.x - self.player.x)
                    distance_y = abs(disk.y - self.player.y)

                    # Se disco passou perto (dentro de 55 pixels) e já passou do jogador
                    if (
                        distance_x < 55
                        and distance_y < 65
                        and disk.x < self.player.x
                        and disk.id not in self.birds_dodged
                    ):
                        self.birds_dodged.add(disk.id)
                        self.score += 25  # Pontos por esquivar disco (ainda mais difícil)
                        # Verificar se merece vida extra
                        self.check_extra_life()

                    # Verificar colisão direta
                    if self.player.rect.colliderect(disk.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(disk.x, disk.y, self.explosion_image)
                            )
                            self.flying_disks.remove(disk)
                            self.score += 40  # Pontos bônus por destruir disco durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com disco, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição do disco
                                self.explosions.append(
                                    Explosion(disk.x, disk.y, self.explosion_image)
                                )
                                self.flying_disks.remove(disk)
                                self.lives -= 1
                                if self.lives <= 0:
                                    # Sem vidas, game over - verificar se entra no ranking
                                    if self.ranking_manager.is_high_score(self.score):
                                        self.state = GameState.ENTER_NAME
                                    else:
                                        self.state = GameState.GAME_OVER
                                # Não reiniciar o nível imediatamente, deixar o jogador continuar
                        break

            # Verificar colisão com tartarugas e aranhas
            if self.current_level <= 20:
                for turtle in self.turtles[:]:
                    # Verificar colisão direta
                    if self.player.rect.colliderect(turtle.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(turtle.x, turtle.y, self.explosion_image)
                            )
                            self.turtles.remove(turtle)
                            self.score += 20  # Pontos bônus por destruir inimigo durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com tartaruga, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição da tartaruga
                                self.explosions.append(
                                    Explosion(turtle.x, turtle.y, self.explosion_image)
                                )
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
            else:
                for spider in self.spiders[:]:
                    # Verificar colisão direta
                    if self.player.rect.colliderect(spider.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(spider.x, spider.y, self.explosion_image)
                            )
                            self.spiders.remove(spider)
                            self.score += 25  # Pontos bônus por destruir aranha durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com aranha, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição da aranha
                                self.explosions.append(
                                    Explosion(spider.x, spider.y, self.explosion_image)
                                )
                                self.spiders.remove(spider)
                                self.lives -= 1
                                if self.lives <= 0:
                                    # Sem vidas, game over - verificar se entra no ranking
                                    if self.ranking_manager.is_high_score(self.score):
                                        self.state = GameState.ENTER_NAME
                                    else:
                                        self.state = GameState.GAME_OVER
                                # Não reiniciar o nível imediatamente, deixar o jogador continuar
                        break

            # Verificar colisão com robôs (níveis 31-40)
            if 31 <= self.current_level <= 40:
                for robot in self.robots[:]:
                    # Verificar colisão direta
                    if self.player.rect.colliderect(robot.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(robot.x, robot.y, self.explosion_image)
                            )
                            # Transferir mísseis ativos do robô para a lista de órfãos
                            for missile in robot.missiles:
                                self.orphan_missiles.append(missile)
                            self.robots.remove(robot)
                            self.score += 35  # Pontos bônus por destruir robô durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com robô, ativar animação de hit
                            if (
                                not self.player.is_hit
                            ):  # Só aplicar hit se não estiver já em estado de hit
                                self.player.take_hit()
                                # Criar explosão na posição do robô
                                self.explosions.append(
                                    Explosion(robot.x, robot.y, self.explosion_image)
                                )
                                # Transferir mísseis ativos do robô para a lista de órfãos
                                for missile in robot.missiles:
                                    self.orphan_missiles.append(missile)
                                self.robots.remove(robot)
                                self.lives -= 1
                                if self.lives <= 0:
                                    # Sem vidas, game over - verificar se entra no ranking
                                    if self.ranking_manager.is_high_score(self.score):
                                        self.state = GameState.ENTER_NAME
                                    else:
                                        self.state = GameState.GAME_OVER
                                # Não reiniciar o nível imediatamente, deixar o jogador continuar
                        break

            # Verificar colisão com aliens (níveis 41-50)
            if 41 <= self.current_level <= 50:
                for alien in self.aliens[:]:
                    # Verificar colisão direta
                    if self.player.rect.colliderect(alien.rect):
                        if self.player.is_invulnerable:
                            # Jogador invulnerável: explodir inimigo sem causar dano
                            self.explosions.append(
                                Explosion(alien.x, alien.y, self.explosion_image)
                            )
                            # Transferir lasers ativos do alien para a lista de órfãos
                            for laser in alien.lasers:
                                self.orphan_lasers.append(laser)
                            self.aliens.remove(alien)
                            self.score += 35  # Pontos bônus por destruir alien durante invulnerabilidade
                            # Verificar se merece vida extra
                            self.check_extra_life()
                        else:
                            # Colidiu com alien, ativar animação de hit
                            if not self.player.is_hit:
                                self.player.take_hit()
                                # Criar explosão na posição do alien
                                self.explosions.append(
                                    Explosion(alien.x, alien.y, self.explosion_image)
                                )
                                # Transferir lasers ativos do alien para a lista de órfãos
                                for laser in alien.lasers:
                                    self.orphan_lasers.append(laser)
                                self.aliens.remove(alien)
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
            if self.flag and self.player.rect.colliderect(self.flag.rect):
                if self.current_level < self.max_levels:
                    self.current_level += 1
                    Level.init_level(self)
                    # Tocar música do novo nível
                    self.music.play_level_music(self, self.current_level)
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
                elif logo_cycle_time > (
                    self.logo_display_time - self.fade_out_duration
                ):
                    fade_progress = (
                        logo_cycle_time
                        - (self.logo_display_time - self.fade_out_duration)
                    ) / self.fade_out_duration
                    alpha = int((1 - fade_progress) * 255)

                # Aplicar alpha ao logo
                if alpha < 255:
                    logo_with_alpha = logo.copy()
                    logo_with_alpha.set_alpha(alpha)
                    logo_rect = logo_with_alpha.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    self.screen.blit(logo_with_alpha, logo_rect)
                else:
                    logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    self.screen.blit(logo, logo_rect)

            # Texto de instrução com fade suave (só em modo development)
            if ENV_CONFIG.get("environment", "production") == "development":
                instruction_alpha = min(255, self.splash_timer * 3)  # Fade in gradual
                instruction_text = self.font.render(
                    "Pressione qualquer tecla para continuar", True, WHITE
                )
                if instruction_alpha < 255:
                    instruction_text.set_alpha(instruction_alpha)
                instruction_rect = instruction_text.get_rect(
                    center=(WIDTH // 2, HEIGHT - 50)
                )
                self.screen.blit(instruction_text, instruction_rect)

        elif self.state == GameState.MAIN_MENU:
            # Tela de menu com fundo do jogo
            self.draw_ocean_background()

            # Logo do jogo (aumentado)
            if self.game_logo:
                # Aumentar o tamanho do logo em 50%
                logo_scaled = pygame.transform.scale(
                    self.game_logo,
                    (
                        int(self.game_logo.get_width() * 1.5),
                        int(self.game_logo.get_height() * 1.5),
                    ),
                )
                logo_rect = logo_scaled.get_rect(center=(WIDTH // 2, 120))
                self.screen.blit(logo_scaled, logo_rect)

            # Título do jogo se não houver logo
            else:
                title_text = self.big_font.render(
                    "Jogo de Plataforma - Mar", True, WHITE
                )
                title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
                self.screen.blit(title_text, title_rect)

            # Opções do menu
            menu_start_y = 300
            for i, option in enumerate(self.menu_options):
                color = YELLOW if i == self.menu_selected else WHITE
                option_text = self.font.render(option, True, color)
                option_rect = option_text.get_rect(
                    center=(WIDTH // 2, menu_start_y + i * 60)
                )

                # Destacar opção selecionada com retângulo
                if i == self.menu_selected:
                    pygame.draw.rect(
                        self.screen, DARK_BLUE, option_rect.inflate(20, 10)
                    )

                self.screen.blit(option_text, option_rect)

            # Rodapé com direitos autorais
            footer_text = "Desenvolvido por CirrasTec, Cirras RetroGames e Canal do Dudu. Todos os direitos reservados."
            footer_surface = pygame.font.Font(None, 24).render(
                footer_text, True, LIGHT_GRAY
            )
            footer_rect = footer_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
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
                    platform.rect.height,
                )
                if (
                    adjusted_rect.right > 0 and adjusted_rect.left < WIDTH
                ):  # Só desenhar se visível
                    # Salvar posição original da plataforma
                    original_x = platform.x
                    # Ajustar posição para câmera
                    platform.x = adjusted_rect.x
                    # Usar o método draw da plataforma que faz ladrilhamento correto
                    platform.draw(self.screen)
                    # Restaurar posição original
                    platform.x = original_x

            # Desenhar bandeira com offset da câmera
            if self.flag:  # Verificar se a bandeira existe
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

            # Desenhar pássaros, morcegos, aviões e discos com offset da câmera
            if self.current_level <= 20:
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
            elif self.current_level <= 30:
                for bat in self.bats:
                    bat_x = bat.x - self.camera_x
                    if bat_x > -50 and bat_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do morcego
                        original_bat_x = bat.x
                        # Ajustar posição para câmera
                        bat.x = bat_x
                        # Chamar método draw do morcego
                        bat.draw(self.screen)
                        # Restaurar posição original
                        bat.x = original_bat_x
            elif self.current_level <= 40:
                for airplane in self.airplanes:
                    airplane_x = airplane.x - self.camera_x
                    if (
                        airplane_x > -60 and airplane_x < WIDTH
                    ):  # Só desenhar se visível (aviões são maiores)
                        # Salvar posição original do avião
                        original_airplane_x = airplane.x
                        # Ajustar posição para câmera
                        airplane.x = airplane_x
                        # Chamar método draw do avião
                        airplane.draw(self.screen)
                        # Restaurar posição original
                        airplane.x = original_airplane_x
            else:
                for disk in self.flying_disks:
                    disk_x = disk.x - self.camera_x
                    if (
                        disk_x > -60 and disk_x < WIDTH
                    ):  # Só desenhar se visível (discos são grandes)
                        # Salvar posição original do disco
                        original_disk_x = disk.x
                        # Ajustar posição para câmera
                        disk.x = disk_x
                        # Chamar método draw do disco
                        disk.draw(self.screen)
                        # Restaurar posição original
                        disk.x = original_disk_x

            # Desenhar tartarugas e aranhas com offset da câmera
            if self.current_level <= 20:
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
            else:
                for spider in self.spiders:
                    spider_x = spider.x - self.camera_x
                    if spider_x > -50 and spider_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original da aranha
                        original_spider_x = spider.x
                        # Ajustar posição para câmera
                        spider.x = spider_x
                        # Chamar método draw da aranha
                        spider.draw(self.screen)
                        # Restaurar posição original
                        spider.x = original_spider_x

            # Desenhar robôs e seus mísseis com offset da câmera (níveis 31-40)
            if 31 <= self.current_level <= 40:
                for robot in self.robots:
                    robot_x = robot.x - self.camera_x
                    if robot_x > -50 and robot_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do robô
                        original_robot_x = robot.x
                        # Ajustar posição para câmera
                        robot.x = robot_x
                        # Chamar método draw do robô (que também desenha os mísseis)
                        robot.draw(self.screen)
                        # Restaurar posição original
                        robot.x = original_robot_x

                        # Desenhar mísseis do robô com offset da câmera
                        for missile in robot.missiles:
                            missile_x = missile.x - self.camera_x
                            if (
                                missile_x > -20 and missile_x < WIDTH + 20
                            ):  # Só desenhar se visível
                                # Salvar posição original do míssil
                                original_missile_x = missile.x
                                # Ajustar posição para câmera
                                missile.x = missile_x
                                # Chamar método draw do míssil
                                missile.draw(self.screen)
                                # Restaurar posição original
                        missile.x = original_missile_x

                # Desenhar mísseis órfãos (de robôs mortos) com offset da câmera
                for missile in self.orphan_missiles:
                    missile_x = missile.x - self.camera_x
                    if (
                        missile_x > -20 and missile_x < WIDTH + 20
                    ):  # Só desenhar se visível
                        # Salvar posição original do míssil
                        original_missile_x = missile.x
                        # Ajustar posição para câmera
                        missile.x = missile_x
                        # Chamar método draw do míssil
                        missile.draw(self.screen)
                        # Restaurar posição original
                        missile.x = original_missile_x

            # Desenhar aliens e seus lasers com offset da câmera (níveis 41-50)
            if 41 <= self.current_level <= 50:
                for alien in self.aliens:
                    alien_x = alien.x - self.camera_x
                    if alien_x > -50 and alien_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do alien
                        original_alien_x = alien.x
                        # Ajustar posição para câmera
                        alien.x = alien_x
                        # Chamar método draw do alien
                        alien.draw(self.screen)
                        # Restaurar posição original
                        alien.x = original_alien_x

                        # Desenhar lasers do alien com offset da câmera
                        for laser in alien.lasers:
                            laser_x = laser.x - self.camera_x
                            if (
                                laser_x > -20 and laser_x < WIDTH + 20
                            ):  # Só desenhar se visível
                                # Salvar posição original do laser
                                original_laser_x = laser.x
                                # Ajustar posição para câmera
                                laser.x = laser_x
                                # Chamar método draw do laser
                                laser.draw(self.screen)
                                # Restaurar posição original
                                laser.x = original_laser_x

                # Desenhar lasers órfãos (de aliens mortos) com offset da câmera
                for laser in self.orphan_lasers:
                    laser_x = laser.x - self.camera_x
                    if laser_x > -20 and laser_x < WIDTH + 20:  # Só desenhar se visível
                        # Salvar posição original do laser
                        original_laser_x = laser.x
                        # Ajustar posição para câmera
                        laser.x = laser_x
                        # Chamar método draw do laser
                        laser.draw(self.screen)
                        # Restaurar posição original
                        laser.x = original_laser_x

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
            Info.display(self, self.screen, self.font, YELLOW)

        elif self.state == GameState.GAME_OVER:
            # Usar fundo do cenário
            self.draw_ocean_background()

            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Pontuação Final: {self.score}", True, WHITE)

            # Centralizar textos principais
            game_over_rect = game_over_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 120)
            )
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)

            # Menu de opções
            for i, option in enumerate(self.game_over_options):
                color = YELLOW if i == self.game_over_selected else WHITE
                option_text = self.font.render(option, True, color)
                option_rect = option_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 + i * 40)
                )

                # Destacar opção selecionada com retângulo
                if i == self.game_over_selected:
                    pygame.draw.rect(
                        self.screen, DARK_BLUE, option_rect.inflate(20, 10)
                    )

                self.screen.blit(option_text, option_rect)

            # Instruções de controle
            control_text = self.font.render(
                "Use ↑↓ ou D-pad para navegar, Enter ou A para selecionar",
                True,
                LIGHT_GRAY,
            )
            control_rect = control_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            self.screen.blit(control_text, control_rect)

        elif self.state == GameState.VICTORY:
            # Desenhar troféu (usando formas geométricas)
            trophy_x = WIDTH // 2
            trophy_y = HEIGHT // 2 - 100

            # Base do troféu
            pygame.draw.rect(self.screen, BROWN, (trophy_x - 40, trophy_y + 80, 80, 20))
            pygame.draw.rect(self.screen, BROWN, (trophy_x - 10, trophy_y + 60, 20, 40))

            # Taça do troféu
            pygame.draw.ellipse(self.screen, YELLOW, (trophy_x - 30, trophy_y, 60, 80))
            pygame.draw.ellipse(
                self.screen, (255, 215, 0), (trophy_x - 25, trophy_y + 5, 50, 70)
            )

            # Alças do troféu
            pygame.draw.arc(
                self.screen,
                YELLOW,
                (trophy_x - 50, trophy_y + 20, 20, 40),
                0,
                math.pi,
                5,
            )
            pygame.draw.arc(
                self.screen,
                YELLOW,
                (trophy_x + 30, trophy_y + 20, 20, 40),
                0,
                math.pi,
                5,
            )

            # Textos
            victory_text = self.big_font.render("PARABÉNS!", True, GREEN)
            complete_text = self.font.render(
                "Você completou todos os níveis!", True, WHITE
            )
            final_score_text = self.font.render(
                f"Pontuação Final: {self.score}", True, WHITE
            )
            restart_text = self.font.render(
                "Pressione R para jogar novamente", True, WHITE
            )

            self.screen.blit(victory_text, (WIDTH // 2 - 150, HEIGHT // 2 + 120))
            self.screen.blit(complete_text, (WIDTH // 2 - 200, HEIGHT // 2 + 170))
            self.screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2 + 200))
            self.screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 240))

        elif self.state == GameState.ENTER_NAME:
            # Tela para inserir nome no ranking
            title_text = self.big_font.render("NOVO RECORDE!", True, YELLOW)
            score_text = self.font.render(f"Pontuação: {self.score}", True, WHITE)
            prompt_text = self.font.render(
                "Digite seu nome (máximo 25 caracteres):", True, WHITE
            )

            # Campo de entrada de nome com cursor
            name_display = (
                self.player_name + "_"
                if len(self.player_name) < 25
                else self.player_name
            )
            name_text = self.font.render(name_display, True, WHITE)

            instruction_text = self.font.render(
                "Pressione ENTER para confirmar", True, LIGHT_GRAY
            )

            # Centralizar textos
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            instruction_rect = instruction_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )

            # Desenhar caixa de entrada
            input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 15, 400, 30)
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
            title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)

            # Cabeçalho com posições fixas
            pos_x = WIDTH // 2 - 200  # Posição inicial da tabela
            header_pos = self.font.render("POS", True, WHITE)
            header_name = self.font.render("NOME", True, WHITE)
            header_score = self.font.render("PONTUAÇÃO", True, WHITE)

            self.screen.blit(header_pos, (pos_x, 180))
            self.screen.blit(header_name, (pos_x + 60, 180))
            self.screen.blit(header_score, (pos_x + 300, 180))

            # Linha separadora
            pygame.draw.line(
                self.screen, WHITE, (pos_x - 10, 200), (pos_x + 390, 200), 2
            )

            # Rankings com colunas alinhadas
            y_offset = 230
            for i, ranking in enumerate(rankings, 1):
                # Destacar o jogador atual se estiver no ranking
                color = YELLOW if ranking["name"] == self.player_name.strip() else WHITE

                # Coluna posição
                pos_text = self.font.render(f"{i:2d}.", True, color)
                self.screen.blit(pos_text, (pos_x, y_offset))

                # Coluna nome (limitado a 18 chars para caber na coluna)
                name_display = ranking["name"][:18]
                name_text = self.font.render(name_display, True, color)
                self.screen.blit(name_text, (pos_x + 60, y_offset))

                # Coluna pontuação (alinhada à direita)
                score_display = f"{int(ranking['score']):,}".replace(",", ".")
                score_text = self.font.render(score_display, True, color)
                score_rect = score_text.get_rect()
                score_rect.right = pos_x + 390
                score_rect.y = y_offset
                self.screen.blit(score_text, score_rect)

                y_offset += 35

            # Instruções
            restart_text = self.font.render(
                "Pressione R para jogar novamente", True, LIGHT_GRAY
            )
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
            self.screen.blit(restart_text, restart_rect)

            back_text = self.font.render(
                "Pressione ESC ou Botão B para voltar", True, LIGHT_GRAY
            )
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            self.screen.blit(back_text, back_rect)

        elif self.state == GameState.CREDITS:
            # Tela de créditos com fundo do jogo
            self.draw_ocean_background()

            # Título
            title_text = self.big_font.render("CRÉDITOS", True, YELLOW)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
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

                text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 30

            # Instruções
            instruction_text = self.font.render(
                "Pressione ESC ou ENTER para voltar", True, LIGHT_GRAY
            )
            instruction_rect = instruction_text.get_rect(
                center=(WIDTH // 2, HEIGHT - 50)
            )
            self.screen.blit(instruction_text, instruction_rect)

        elif self.state == GameState.RECORDS:
            # Tela de recordes (reutilizar a lógica do ranking)
            self.draw_ocean_background()

            # Título
            title_text = self.big_font.render("RECORDES", True, YELLOW)
            rankings = self.ranking_manager.get_rankings()

            # Título
            title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)

            # Cabeçalho com posições fixas
            pos_x = WIDTH // 2 - 200  # Posição inicial da tabela
            header_pos = self.font.render("POS", True, WHITE)
            header_name = self.font.render("NOME", True, WHITE)
            header_score = self.font.render("PONTUAÇÃO", True, WHITE)

            self.screen.blit(header_pos, (pos_x, 180))
            self.screen.blit(header_name, (pos_x + 60, 180))
            self.screen.blit(header_score, (pos_x + 300, 180))

            # Linha separadora
            pygame.draw.line(
                self.screen, WHITE, (pos_x - 10, 200), (pos_x + 390, 200), 2
            )

            # Rankings com colunas alinhadas
            y_offset = 230
            for i, ranking in enumerate(rankings, 1):
                color = WHITE

                # Coluna posição
                pos_text = self.font.render(f"{i:2d}.", True, color)
                self.screen.blit(pos_text, (pos_x, y_offset))

                # Coluna nome (limitado a 18 chars para caber na coluna)
                name_display = ranking["name"][:18]
                name_text = self.font.render(name_display, True, color)
                self.screen.blit(name_text, (pos_x + 60, y_offset))

                # Coluna pontuação (alinhada à direita)
                score_display = f"{int(ranking['score']):,}".replace(",", ".")
                score_text = self.font.render(score_display, True, color)
                score_rect = score_text.get_rect()
                score_rect.right = pos_x + 390
                score_rect.y = y_offset
                self.screen.blit(score_text, score_rect)

                y_offset += 35

            # Instruções
            instruction_text = self.font.render(
                "Pressione ESC ou ENTER para voltar", True, LIGHT_GRAY
            )
            instruction_rect = instruction_text.get_rect(
                center=(WIDTH // 2, HEIGHT - 50)
            )
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
