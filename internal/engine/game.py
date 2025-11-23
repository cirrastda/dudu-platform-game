import pygame
import sys
import os
import math
from internal.utils.constants import *
from internal.utils.functions import *
from internal.resources.cache import ResourceCache
from internal.resources.image import Image
from internal.engine.joystick import Joystick
from internal.engine.video import VideoPlayer
from internal.resources.bullet import Bullet
from internal.resources.explosion import Explosion
from internal.engine.screen import Screen
from internal.engine.ranking import RankingManager
from internal.engine.state import GameState
from internal.engine.difficulty import Difficulty
from internal.engine.level.level import Level
from internal.engine.sound.music import Music
from internal.engine.sound.mixer import Mixer
from internal.engine.sound.effects import SoundEffects


# Carregar módulos auxiliares da pasta internal/engine/game/ sem conflito de nome
_GAME_SUBMODULE_DIR = os.path.join(os.path.dirname(__file__), "game")
Life = None
Score = None
Hold = None
Events = None
Draw = None
Update = None
DifficultyOps = None
Pool = None
Cheat = None
Menu = None
System = None
try:
    import importlib.util

    # Encaminhadores finos para manter compatibilidade dos testes e da API

    def _load_submodule(file_name: str, module_name: str):
        spec = importlib.util.spec_from_file_location(
            module_name, os.path.join(_GAME_SUBMODULE_DIR, file_name)
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    _life_mod = _load_submodule("life.py", "internal.engine._game_life")
    _score_mod = _load_submodule("score.py", "internal.engine._game_score")
    _hold_mod = _load_submodule("hold.py", "internal.engine._game_hold")
    _events_mod = _load_submodule("events.py", "internal.engine._game_events")
    _draw_mod = _load_submodule("draw.py", "internal.engine._game_draw")
    _update_mod = _load_submodule("update.py", "internal.engine._game_update")
    _difficulty_mod = _load_submodule(
        "difficulty.py", "internal.engine._game_difficulty"
    )
    _pool_mod = _load_submodule("pool.py", "internal.engine._game_pool")
    _cheat_mod = _load_submodule("cheat.py", "internal.engine._game_cheat")
    _menu_mod = _load_submodule("menu.py", "internal.engine._game_menu")
    _system_mod = _load_submodule("system.py", "internal.engine._game_system")
    Life = getattr(_life_mod, "Life", None)
    Score = getattr(_score_mod, "Score", None)
    Hold = getattr(_hold_mod, "Hold", None)
    Events = getattr(_events_mod, "Events", None)
    Draw = getattr(_draw_mod, "Draw", None)
    Update = getattr(_update_mod, "Update", None)
    DifficultyOps = getattr(_difficulty_mod, "DifficultyOps", None)
    Pool = getattr(_pool_mod, "Pool", None)
    Cheat = getattr(_cheat_mod, "Cheat", None)
    Menu = getattr(_menu_mod, "Menu", None)
    System = getattr(_system_mod, "System", None)
except Exception:
    # Em ambientes de teste, garantir que erros de import não interrompam coleta
    pass

# Carregar configurações
ENV_CONFIG = load_env_config()
# Em ambiente de teste (pytest), ignorar .env carregado para os testes
try:
    if "pytest" in sys.modules:
        ENV_CONFIG = {"environment": "production"}
except Exception:
    pass


class Game:
    def __init__(self):
        # Carregar configuração de ambiente antes de inicializar a tela

        self.env_config = ENV_CONFIG
        # Inicializar o módulo de sistema cedo, pois Screen.init usa is_development()
        try:
            self._system = System(self)
        except Exception:
            self._system = None
        # Inicializar outros módulos delegados que podem ser chamados cedo em testes
        try:
            self._difficulty = DifficultyOps(self)
            self._pool = Pool(self)
            self._cheat = Cheat(self)
            self._menu = Menu(self)
        except Exception:
            pass
        Screen.init(self)
        pygame.display.set_caption("Jump and Hit")
        # Definir ícone da janela (barra de título)
        try:
            # Prioriza o ícone de desktop novo (PNG/ICO) e aplica fallback
            candidates = [
                resource_path("imagens/icones/icon_minimal.png"),
                resource_path("imagens/icones/icon_desktop_new.png"),
                resource_path("imagens/icones/title_icon.png"),
            ]
            icon_path = next((p for p in candidates if os.path.exists(p)), None)
            if icon_path:
                icon_surface = pygame.image.load(icon_path)
                pygame.display.set_icon(icon_surface)
        except Exception:
            # Ignorar falhas ao definir ícone para não interromper o jogo
            pass
        self.clock = pygame.time.Clock()
        self.state = GameState.SPLASH
        # Rastrear vidas extras coletadas por nível para não reaparecerem
        self.collected_extra_life_levels = set()
        self.max_levels = 51
        # Configurar nível inicial baseado no ambiente
        if (
            ENV_CONFIG.get("environment") == "development"
            and "initial-stage" in ENV_CONFIG
        ):
            try:
                self.current_level = int(ENV_CONFIG["initial-stage"])
                # Validar se o nível está dentro do range válido
                if self.current_level < 1 or self.current_level > self.max_levels:
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

        Mixer.init(pygame)

        # Sistema de música
        self.music = Music()
        self.music.start(self)
        self.sound_effects = SoundEffects()
        self.sound_effects.load_sound_effects()

        # Sistema de câmera
        self.camera_x = 0

        # Dificuldade padrão e opções
        self.difficulty = Difficulty.NORMAL
        self.difficulty_options = ["Fácil", "Normal", "Difícil"]
        self.difficulty_selected = 1

        # Em modo development, aplicar dificuldade definida no .env, se presente
        try:
            if self.env_config.get("environment") == "development":
                raw_diff = self.env_config.get("difficulty")
                if isinstance(raw_diff, str) and raw_diff.strip():
                    key = raw_diff.strip().upper()
                    # Aceitar também nomes em PT-BR e índices 0/1/2
                    mapping = {
                        "EASY": Difficulty.EASY,
                        "FACIL": Difficulty.EASY,
                        "FÁCIL": Difficulty.EASY,
                        "NORMAL": Difficulty.NORMAL,
                        "HARD": Difficulty.HARD,
                        "DIFICIL": Difficulty.HARD,
                        "DIFÍCIL": Difficulty.HARD,
                        "0": Difficulty.EASY,
                        "1": Difficulty.NORMAL,
                        "2": Difficulty.HARD,
                    }
                    chosen = mapping.get(key)
                    if chosen is not None:
                        self.difficulty = chosen
                        # Alinhar seleção do menu de dificuldade à configuração
                        if self.difficulty == Difficulty.EASY:
                            self.difficulty_selected = 0
                        elif self.difficulty == Difficulty.HARD:
                            self.difficulty_selected = 2
                        else:
                            self.difficulty_selected = 1
                # Ativar escudo inicial quando flag shield=on estiver definida no .env
                raw_shield = str(self.env_config.get("shield", "")).strip().lower()
                if raw_shield in ("on", "1", "true", "yes"):
                    self.shield_active = True
        except Exception:
            # Não interromper inicialização do jogo caso .env esteja inválido
            pass

        # Ligar subsistemas extraídos e encaminhar métodos públicos
        self._life = Life(self)
        self.get_initial_lives = self._life.get_initial_lives
        self.get_extra_life_milestones_and_increment = (
            self._life.get_extra_life_milestones_and_increment
        )
        self.check_extra_life = self._life.check_extra_life

        self._score = Score(self)
        self.get_score_multiplier = self._score.get_score_multiplier
        self.add_score = self._score.add_score

        self._hold = Hold(self)
        self._events = Events(self)
        self._draw = Draw(self)
        self._update = Update(self)
        self._difficulty = DifficultyOps(self)
        self._pool = Pool(self)
        self._cheat = Cheat(self)
        self._menu = Menu(self)
        self._system = System(self)

        # Sistema de pontuação
        self.score = 0
        self.platforms_jumped = (
            set()
        )  # Conjunto para rastrear IDs de plataformas já pontuadas
        self.birds_dodged = set()  # Para rastrear pássaros já esquivados

        # Sistema de vidas
        self.lives = self.get_initial_lives()
        self.max_lives = self.get_initial_lives()

        # Sistema de vidas extras por pontuação (ajustado por dificuldade)
        (
            self.extra_life_milestones,
            self.extra_life_increment_after_milestones,
        ) = self.get_extra_life_milestones_and_increment()
        self.next_extra_life_score = self.extra_life_milestones[0]
        self.extra_lives_earned = 0  # Contador de vidas extras ganhas

        # Sistema de joystick
        Joystick.init(self)

        # Sistema de vídeo
        self.video_player = VideoPlayer()
        self.ending_video_player = VideoPlayer()

        # Código secreto: Konami Code para conceder 99 vidas iniciais
        self.cheat_99_lives_enabled = False
        self._cheat_buffer = []
        self._cheat_sequence = [
            "UP",
            "UP",
            "DOWN",
            "DOWN",
            "LEFT",
            "RIGHT",
            "LEFT",
            "RIGHT",
            "B",
            "A",
        ]

        # Sistema de splash screen e menu
        self.splash_timer = 0
        self.splash_duration = 360  # 6 segundos (60 FPS * 6)
        self.current_logo_index = 0
        self.logo_display_time = 120  # Tempo para cada logo (2 segundos)
        self.logos = []  # Lista de logos para splash
        self.menu_selected = 0  # Opção selecionada no menu
        self.menu_options = ["Iniciar", "Recordes", "Créditos", "Sair"]
        self.game_logo = None  # Logo principal do jogo
        self.credits_type = (
            None  # Inicializa tipo de créditos para evitar valores antigos
        )

        # Efeitos de fade para splash screen
        self.fade_in_duration = 30  # 0.5 segundos para fade in
        self.fade_out_duration = 30  # 0.5 segundos para fade out
        self.logo_hold_time = 60  # 1 segundo para mostrar o logo
        self.music_started = False  # Controla se a música já foi iniciada

        # Estado de hold para transições com esmaecimento e áudio
        self.hold_active = False
        self.hold_type = None  # "level_end" ou "game_over"
        self.hold_frames_left = 0
        self.hold_total_frames = 0
        # Controle de ducking de música durante holds com som
        self._music_duck_original_volume = None
        self._next_level_after_hold = False
        self._pending_state_after_hold = None

        # Controles do boss alien (nível 51) — inicialização segura
        # Alguns testes exercitam caminhos de desenho/atualização sem criar nível 51
        # pelo gerador estático; manter atributos definidos evita AttributeError.
        self.boss_alien = None
        self.boss_alien_captured = False
        self.capture_sequence_timer = 0
        self.capture_flash_timer = 0
        self.capture_flash_state = False

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

        # Sistema de gotas de chuva (fases 7-10)
        self.raindrops = []
        self.raindrop_spawn_timer = 0
        self.raindrops_per_spawn = 1
        self.raindrop_spawn_interval = 150

        # Sistema de gotas de lava (fases 27-30)
        self.lava_drops = []
        self.lavadrop_spawn_timer = 0
        self.lavadrops_per_spawn = 0
        self.lavadrop_spawn_interval = 999999

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

        # Shooting stars (níveis 21-30, junto com morcegos)
        self.shooting_stars = []
        self.shooting_star_spawn_timer = 0
        self.shooting_stars_per_spawn = 1
        self.shooting_star_spawn_interval = 220

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
        self.orphan_lasers = (
            []
        )  # Lasers de aliens mortos que continuam visíveis mas sem hitbox

        # Inicializar variáveis de foguinhos (nível 51)
        self.fires = []
        self.fire_spawn_timer = 0
        self.fires_per_spawn = 1
        self.fire_spawn_interval = 240  # Spawn menos frequente para reduzir quantidade

        # Ajustar dificuldade baseada no nível
        self.birds_per_spawn = Level.get_birds_per_spawn(self.current_level)
        self.bird_spawn_interval = Level.get_bird_spawn_interval(self.current_level)
        # Intervalo das gotas acompanha o dos pássaros por padrão
        self.raindrop_spawn_interval = self.bird_spawn_interval

        # Fonte para texto (HUD mais legível e em negrito)
        try:
            # Preferir fonte do sistema para melhor nitidez
            self.font = pygame.font.SysFont("Segoe UI", 48, bold=True)
        except Exception:
            try:
                self.font = pygame.font.SysFont("Arial", 48, bold=True)
            except Exception:
                # Fallback mantendo compatibilidade com ambientes de teste
                self.font = pygame.font.Font(None, 48)
                try:
                    if hasattr(self.font, "set_bold"):
                        self.font.set_bold(True)
                except Exception:
                    pass
        self.big_font = pygame.font.Font(None, 72)

        # Fontes dedicadas ao menu (estilo mais agradável e consistente)
        try:
            self.menu_font = pygame.font.SysFont("Bahnschrift", 32, bold=True)
        except Exception:
            try:
                self.menu_font = pygame.font.SysFont("Segoe UI", 32, bold=True)
            except Exception:
                self.menu_font = pygame.font.Font(None, 32)
                try:
                    if hasattr(self.menu_font, "set_bold"):
                        self.menu_font.set_bold(True)
                except Exception:
                    pass
        try:
            self.menu_big_font = pygame.font.SysFont("Bahnschrift", 56, bold=True)
        except Exception:
            try:
                self.menu_big_font = pygame.font.SysFont("Segoe UI", 56, bold=True)
            except Exception:
                self.menu_big_font = pygame.font.Font(None, 56)
                try:
                    if hasattr(self.menu_big_font, "set_bold"):
                        self.menu_big_font.set_bold(True)
                except Exception:
                    pass
        try:
            self.menu_small_font = pygame.font.SysFont("Segoe UI", 22)
        except Exception:
            try:
                self.menu_small_font = pygame.font.SysFont("Arial", 22)
            except Exception:
                self.menu_small_font = pygame.font.Font(None, 22)

        # Fonte de conteúdo do menu (um pouco mais bold e menor)
        try:
            self.menu_content_font = pygame.font.SysFont("Segoe UI", 22, bold=True)
        except Exception:
            try:
                self.menu_content_font = pygame.font.SysFont("Arial", 22, bold=True)
            except Exception:
                self.menu_content_font = pygame.font.Font(None, 22)
                try:
                    if hasattr(self.menu_content_font, "set_bold"):
                        self.menu_content_font.set_bold(True)
                except Exception:
                    pass

        # Carregar imagens
        self.image = Image()
        self.image.load_images(self)
        # Sincronizar logos da splash screen carregados pelo Image
        self.logos = getattr(self.image, "logos", [])
        # Disponibilizar texturas de plataforma diretamente no Game para geradores de níveis
        self.platform_texture = self.image.platform_texture
        self.platform_texture_city = self.image.platform_texture_city
        self.platform_texture_space = self.image.platform_texture_space
        self.platform_texture_ship = self.image.platform_texture_ship
        self.platform_texture_flag = self.image.platform_texture_flag
        # Compatibilidade com código que espera image_manager
        self.image_manager = self.image

        # Espelhar texturas e imagens necessárias como atributos diretos do jogo
        self.platform_texture = getattr(self.image, "platform_texture", None)
        self.platform_texture_city = getattr(self.image, "platform_texture_city", None)
        self.platform_texture_space = getattr(
            self.image, "platform_texture_space", None
        )
        self.platform_texture_ship = getattr(self.image, "platform_texture_ship", None)
        self.platform_texture_flag = getattr(self.image, "platform_texture_flag", None)

        self.turtle_images = getattr(self.image, "turtle_images", None)
        self.spider_images = getattr(self.image, "spider_images", None)
        self.robot_images = getattr(self.image, "robot_images", None)
        self.missile_images = getattr(self.image, "missile_images", None)
        self.alien_images = getattr(self.image, "alien_images", None)

        # Imagens de avião: manter também cópias individuais para uso existente
        self.airplane_img1 = getattr(self.image, "airplane_img1", None)
        self.airplane_img2 = getattr(self.image, "airplane_img2", None)
        self.airplane_img3 = getattr(self.image, "airplane_img3", None)
        self.airplane_images = (
            (self.airplane_img1, self.airplane_img2, self.airplane_img3)
            if self.airplane_img1 and self.airplane_img2 and self.airplane_img3
            else None
        )

        self.flying_disk_images = getattr(self.image, "flying_disk_images", None)
        self.fire_image = getattr(self.image, "fire_image", None)
        self.extra_life_img = getattr(self.image, "extra_life_img", None)
        self.explosion_image = getattr(self.image, "explosion_image", None)
        self.lava_drop_img = getattr(self.image, "lava_drop_img", None)
        # Imagens dos power-ups e bolha do escudo
        self.powerup_invincibility_img = getattr(
            self.image, "powerup_invincibility_img", None
        )
        self.powerup_double_jump_img = getattr(
            self.image, "powerup_double_jump_img", None
        )
        self.powerup_shield_img = getattr(self.image, "powerup_shield_img", None)
        self.shield_bubble_img = getattr(self.image, "shield_bubble_img", None)

        # Transferir logo do jogo
        self.game_logo = self.image.game_logo

        # Sistema de créditos com rolagem
        self.credits_scroll_y = 0
        self.credits_scroll_speed = 1
        self.credits_reset_timer = 0
        self.credits_type = "menu"  # "menu" ou "ending"

        # Itens colecionáveis
        self.extra_lives = []
        self.powerups = []

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

    # Encaminhadores finos para manter compatibilidade e delegar aos módulos extraídos
    def get_initial_lives(self):
        return Life(self).get_initial_lives()

    def get_extra_life_milestones_and_increment(self):
        return Life(self).get_extra_life_milestones_and_increment()

    def check_extra_life(self):
        return Life(self).check_extra_life()

    def get_score_multiplier(self):
        return Score(self).get_score_multiplier()

    def add_score(self, base_points):
        return Score(self).add_score(base_points)

    def _compute_sound_frames(self, sound_key, default_seconds=2.0):
        return self._hold._compute_sound_frames(sound_key, default_seconds)

    def _start_hold(self, hold_type, frames, pending_state=None, next_level=False):
        return self._hold._start_hold(hold_type, frames, pending_state, next_level)

    def start_game_over_hold(self):
        return self._hold.start_game_over_hold()

    def start_level_end_hold(self, is_last_level):
        return self._hold.start_level_end_hold(is_last_level)

    def _apply_hold_ducking(self):
        return self._hold._apply_hold_ducking()

    def _process_cheat_token(self, token):
        if not hasattr(self, "_cheat") or self._cheat is None:
            try:
                self._cheat = Cheat(self)
            except Exception:
                pass
        return self._cheat.process_cheat_token(token)

    def _map_key_to_cheat_token(self, key, unicode_val=""):
        if not hasattr(self, "_cheat") or self._cheat is None:
            try:
                self._cheat = Cheat(self)
            except Exception:
                pass
        return self._cheat.map_key_to_cheat_token(key, unicode_val)

    def update_bird_difficulty(self):
        if not hasattr(self, "_difficulty") or self._difficulty is None:
            try:
                self._difficulty = DifficultyOps(self)
            except Exception:
                pass
        return self._difficulty.update_bird_difficulty()

    def get_pooled_bullet(self, x, y, direction=1, image=None):
        if not hasattr(self, "_pool") or self._pool is None:
            try:
                self._pool = Pool(self)
            except Exception:
                pass
        return self._pool.get_pooled_bullet(x, y, direction, image)

    def return_bullet_to_pool(self, bullet):
        if not hasattr(self, "_pool") or self._pool is None:
            try:
                self._pool = Pool(self)
            except Exception:
                pass
        return self._pool.return_bullet_to_pool(bullet)

    def get_pooled_explosion(self, x, y, image=None):
        if not hasattr(self, "_pool") or self._pool is None:
            try:
                self._pool = Pool(self)
            except Exception:
                pass
        return self._pool.get_pooled_explosion(x, y, image)

    def return_explosion_to_pool(self, explosion):
        if not hasattr(self, "_pool") or self._pool is None:
            try:
                self._pool = Pool(self)
            except Exception:
                pass
        return self._pool.return_explosion_to_pool(explosion)

    def draw_ocean_background(self, draw_surface=None):
        """Delegar desenho do fundo para o submódulo Draw."""
        if not hasattr(self, "_draw") or self._draw is None:
            try:
                self._draw = Draw(self)
            except Exception:
                pass
        return self._draw.draw_ocean_background(draw_surface)

    def handle_events(self):
        if not hasattr(self, "_events") or self._events is None:
            try:
                self._events = Events(self)
            except Exception:
                pass
        return self._events.handle_events()

    def draw(self):
        if not hasattr(self, "_draw") or self._draw is None:
            try:
                self._draw = Draw(self)
            except Exception:
                pass
        return self._draw.draw()

    def update(self):
        if not hasattr(self, "_update") or self._update is None:
            try:
                self._update = Update(self)
            except Exception:
                pass
        return self._update.update()

    def handle_menu_selection(self):
        if not hasattr(self, "_menu") or self._menu is None:
            try:
                self._menu = Menu(self)
            except Exception:
                pass
        # Injetar sys e pygame do módulo atual para permitir monkeypatch nos testes
        try:
            self._menu.set_runtime_modules(sys, pygame)
        except Exception:
            pass
        return self._menu.handle_menu_selection()

    def is_development(self):
        if not hasattr(self, "_system") or self._system is None:
            try:
                self._system = System(self)
            except Exception:
                pass
        return self._system.is_development()

    def run(self):
        if not hasattr(self, "_system") or self._system is None:
            try:
                self._system = System(self)
            except Exception:
                pass
        return self._system.run()

    def shutdown(self):
        if not hasattr(self, "_system") or self._system is None:
            try:
                self._system = System(self)
            except Exception:
                pass
        return self._system.shutdown()
