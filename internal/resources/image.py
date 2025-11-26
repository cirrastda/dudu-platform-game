import pygame
from internal.resources.cache import ResourceCache
from internal.utils.constants import WIDTH, HEIGHT
from internal.engine.level.level import Level


class Image:
    def __init__(self, image_path=None):
        if image_path:
            self.image_path = image_path
            self.image = pygame.image.load(image_path)
        else:
            self.image_path = None
            self.image = None

    def load_images(self, game=None):
        """Carregar todas as imagens do jogo usando sistema de cache"""
        try:
            # Inicializar cache de recursos
            cache = ResourceCache()

            # Carregar fundo baseado no nível atual (apenas para gameplay)
            if game:
                background_file = Level.get_background_for_level(
                    game, game.current_level
                )
                self.background_img = cache.get_image(
                    background_file,
                    (WIDTH, HEIGHT),
                )
            else:
                self.background_img = None

            # Carregar fundo fixo para menus, recordes, etc.
            self.menu_background_img = cache.get_image(
                "imagens/fundo6.png", (WIDTH, HEIGHT)
            )

            # Carregar textura de plataforma usando cache
            self.platform_texture = cache.get_image(
                "imagens/texturas/platform2.png", (20, 20)
            )
            self.platform_texture_city = cache.get_image(
                "imagens/texturas/metal.jpg", (20, 20)
            )
            # Textura espacial para níveis 41-50
            self.platform_texture_space = cache.get_image(
                "imagens/texturas/platform-space.png", (20, 20)
            )
            # Textura da nave para nível 51
            self.platform_texture_ship = cache.get_image(
                "imagens/texturas/platform-ship.png", (20, 20)
            )
            # Textura padrão para a plataforma da bandeira
            # Usa a mesma textura das plataformas comuns por padrão
            self.platform_texture_flag = self.platform_texture

            # Carregar imagens dos pássaros usando cache
            self.bird_img1 = cache.get_image(
                "imagens/inimigos/bird1.png",
                (40, 30),
            )
            self.bird_img2 = cache.get_image(
                "imagens/inimigos/bird2.png",
                (40, 30),
            )

            # Carregar imagens dos morcegos usando cache
            self.bat_img1 = cache.get_image(
                "imagens/inimigos/bat1.png",
                (40, 30),
            )
            self.bat_img2 = cache.get_image(
                "imagens/inimigos/bat2.png",
                (40, 30),
            )
            self.bat_img3 = cache.get_image(
                "imagens/inimigos/bat3.png",
                (40, 30),
            )

            # Carregar imagens dos aviões usando cache
            self.airplane_img1 = cache.get_image(
                "imagens/inimigos/airplane1.png", (50, 30)
            )
            self.airplane_img2 = cache.get_image(
                "imagens/inimigos/airplane2.png", (50, 30)
            )
            self.airplane_img3 = cache.get_image(
                "imagens/inimigos/airplane3.png", (50, 30)
            )

            # Carregar imagens do flying-disk usando cache
            try:
                self.disk_img1 = cache.get_image(
                    "imagens/inimigos/disk1.png",
                    (40, 40),
                )
                self.disk_img2 = cache.get_image(
                    "imagens/inimigos/disk2.png",
                    (40, 40),
                )
                self.disk_img3 = cache.get_image(
                    "imagens/inimigos/disk3.png",
                    (40, 40),
                )
                self.flying_disk_images = [
                    self.disk_img1,
                    self.disk_img2,
                    self.disk_img3,
                ]
            except pygame.error as e:
                print(f"Erro ao carregar imagens do flying-disk: {e}")
                self.flying_disk_images = None

            # Carregar imagem da estrela cadente (shooting star) com fallback
            try:
                self.shooting_star_img = None
                # Caminho correto informado pelo projeto
                path = "imagens/elementos/estrelaCadente.png"
                try:
                    img = cache.get_image(path, (26, 26))
                except Exception:
                    img = None
                if img:
                    self.shooting_star_img = img
                # Fallback: desenhar um pequeno círculo branco se não houver imagem
                if self.shooting_star_img is None:
                    surf = pygame.Surface((26, 26), pygame.SRCALPHA)
                    pygame.draw.circle(surf, (255, 255, 255), (13, 13), 6)
                    self.shooting_star_img = surf
            except Exception as e:
                print(f"Erro ao carregar imagem da estrela cadente: {e}")
                self.shooting_star_img = None

            try:
                self.meteor_img = None
                path = "imagens/elementos/meteoro.png"
                try:
                    img = cache.get_image(path, (30, 30))
                except Exception:
                    img = None
                if img:
                    self.meteor_img = img
                if self.meteor_img is None:
                    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
                    pygame.draw.circle(surf, (160, 160, 160), (15, 15), 12)
                    self.meteor_img = surf
            except Exception:
                self.meteor_img = None

            # Carregar imagens das tartarugas usando cache
            try:
                self.turtle_left1 = cache.get_image(
                    "imagens/inimigos/turtle-left1.png", (40, 30)
                )
                self.turtle_left2 = cache.get_image(
                    "imagens/inimigos/turtle-left2.png", (40, 30)
                )
                self.turtle_left3 = cache.get_image(
                    "imagens/inimigos/turtle-left3.png", (40, 30)
                )
                self.turtle_right1 = cache.get_image(
                    "imagens/inimigos/turtle-right1.png", (40, 30)
                )
                self.turtle_right2 = cache.get_image(
                    "imagens/inimigos/turtle-right2.png", (40, 30)
                )
                self.turtle_right3 = cache.get_image(
                    "imagens/inimigos/turtle-right3.png", (40, 30)
                )

                # Organizar imagens em dicionário para facilitar o uso
                self.turtle_images = {
                    "left": [self.turtle_left1, self.turtle_left2, self.turtle_left3],
                    "right": [
                        self.turtle_right1,
                        self.turtle_right2,
                        self.turtle_right3,
                    ],
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens das tartarugas: {e}")
                self.turtle_images = None

            # Carregar imagens das aranhas usando cache
            try:
                self.spider_img1 = cache.get_image(
                    "imagens/inimigos/spider1.png", (40, 30)
                )
                self.spider_img2 = cache.get_image(
                    "imagens/inimigos/spider2.png", (40, 30)
                )
                self.spider_img3 = cache.get_image(
                    "imagens/inimigos/spider3.png", (40, 30)
                )

                # Organizar imagens em lista para facilitar o uso
                self.spider_images = [
                    self.spider_img1,
                    self.spider_img2,
                    self.spider_img3,
                ]
            except pygame.error as e:
                print(f"Erro ao carregar imagens das aranhas: {e}")
                self.spider_images = None

            # Carregar imagens dos robôs usando cache
            try:
                # Imagens de movimento
                self.robot_right1 = cache.get_image(
                    "imagens/inimigos/robot-right1.png", (57, 57)
                )
                self.robot_right2 = cache.get_image(
                    "imagens/inimigos/robot-right2.png", (57, 57)
                )
                self.robot_right3 = cache.get_image(
                    "imagens/inimigos/robot-right3.png", (57, 57)
                )
                self.robot_left1 = cache.get_image(
                    "imagens/inimigos/robot-left1.png", (57, 57)
                )
                self.robot_left2 = cache.get_image(
                    "imagens/inimigos/robot-left2.png", (57, 57)
                )
                self.robot_left3 = cache.get_image(
                    "imagens/inimigos/robot-left3.png", (57, 57)
                )

                # Imagens de tiro
                self.robot_shot_right1 = cache.get_image(
                    "imagens/inimigos/robot-shot-right1.png", (57, 57)
                )
                self.robot_shot_right2 = cache.get_image(
                    "imagens/inimigos/robot-shot-right2.png", (57, 57)
                )
                self.robot_shot_right3 = cache.get_image(
                    "imagens/inimigos/robot-shot-right3.png", (57, 57)
                )
                self.robot_shot_left1 = cache.get_image(
                    "imagens/inimigos/robot-shot-left1.png", (57, 57)
                )
                self.robot_shot_left2 = cache.get_image(
                    "imagens/inimigos/robot-shot-left2.png", (57, 57)
                )
                self.robot_shot_left3 = cache.get_image(
                    "imagens/inimigos/robot-shot-left3.png", (57, 57)
                )

                # Organizar imagens em dicionário para facilitar o uso
                self.robot_images = {
                    "left": [self.robot_left1, self.robot_left2, self.robot_left3],
                    "right": [self.robot_right1, self.robot_right2, self.robot_right3],
                    "shot_left": [
                        self.robot_shot_left1,
                        self.robot_shot_left2,
                        self.robot_shot_left3,
                    ],
                    "shot_right": [
                        self.robot_shot_right1,
                        self.robot_shot_right2,
                        self.robot_shot_right3,
                    ],
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens dos robôs: {e}")
                self.robot_images = None

            # Carregar imagens dos aliens usando cache
            try:
                # Imagens de movimento (esquerda e direita)
                self.alien_left1 = cache.get_image(
                    "imagens/inimigos/alien-left1.png", (57, 57)
                )
                self.alien_left2 = cache.get_image(
                    "imagens/inimigos/alien-left2.png", (57, 57)
                )
                self.alien_left3 = cache.get_image(
                    "imagens/inimigos/alien-left3.png", (57, 57)
                )
                self.alien_left4 = cache.get_image(
                    "imagens/inimigos/alien-left4.png", (57, 57)
                )
                self.alien_left5 = cache.get_image(
                    "imagens/inimigos/alien-left5.png", (57, 57)
                )

                self.alien_right1 = cache.get_image(
                    "imagens/inimigos/alien-right1.png", (57, 57)
                )
                self.alien_right2 = cache.get_image(
                    "imagens/inimigos/alien-right2.png", (57, 57)
                )
                self.alien_right3 = cache.get_image(
                    "imagens/inimigos/alien-right3.png", (57, 57)
                )
                self.alien_right4 = cache.get_image(
                    "imagens/inimigos/alien-right4.png", (57, 57)
                )
                self.alien_right5 = cache.get_image(
                    "imagens/inimigos/alien-right5.png", (57, 57)
                )

                # Imagens de tiro (apenas virado para a esquerda)
                self.alien_shot_left1 = cache.get_image(
                    "imagens/inimigos/alien-shot-left1.png", (57, 57)
                )
                self.alien_shot_left2 = cache.get_image(
                    "imagens/inimigos/alien-shot-left2.png", (57, 57)
                )
                self.alien_shot_left3 = cache.get_image(
                    "imagens/inimigos/alien-shot-left3.png", (57, 57)
                )

                # Organizar imagens em dicionário para facilitar o uso
                self.alien_images = {
                    "left": [
                        self.alien_left1,
                        self.alien_left2,
                        self.alien_left3,
                        self.alien_left4,
                        self.alien_left5,
                    ],
                    "right": [
                        self.alien_right1,
                        self.alien_right2,
                        self.alien_right3,
                        self.alien_right4,
                        self.alien_right5,
                    ],
                    "shot_left": [
                        self.alien_shot_left1,
                        self.alien_shot_left2,
                        self.alien_shot_left3,
                    ],
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens dos aliens: {e}")
                self.alien_images = None

            # Carregar imagens do boss alien usando cache
            try:
                # Imagens de corrida
                self.boss_alien_run1 = cache.get_image(
                    "imagens/boss/alien1.png", (57, 57)
                )
                self.boss_alien_run2 = cache.get_image(
                    "imagens/boss/alien2.png", (57, 57)
                )
                self.boss_alien_run3 = cache.get_image(
                    "imagens/boss/alien3.png", (57, 57)
                )
                self.boss_alien_run4 = cache.get_image(
                    "imagens/boss/alien4.png", (57, 57)
                )

                # Imagens de salto
                self.boss_alien_jump1 = cache.get_image(
                    "imagens/boss/alienJ1.png", (57, 57)
                )
                self.boss_alien_jump2 = cache.get_image(
                    "imagens/boss/alienJ2.png", (57, 57)
                )
                self.boss_alien_jump3 = cache.get_image(
                    "imagens/boss/alienJ3.png", (57, 57)
                )
                self.boss_alien_jump4 = cache.get_image(
                    "imagens/boss/alienJ4.png", (57, 57)
                )

                # Imagem de parado
                self.boss_alien_stop = cache.get_image(
                    "imagens/boss/alienStop.png", (57, 57)
                )

                # Organizar imagens em dicionário para facilitar o uso
                self.boss_alien_images = {
                    "running": [
                        self.boss_alien_run1,
                        self.boss_alien_run2,
                        self.boss_alien_run3,
                        self.boss_alien_run4,
                    ],
                    "jumping": [
                        self.boss_alien_jump1,
                        self.boss_alien_jump2,
                        self.boss_alien_jump3,
                        self.boss_alien_jump4,
                    ],
                    "stopped": self.boss_alien_stop,
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens do boss alien: {e}")
                self.boss_alien_images = None

            # Carregar imagem do foguinho mantendo proporção
            try:
                base_fire = cache.get_image("imagens/inimigos/fogo.png")
                if base_fire:
                    orig_w, orig_h = base_fire.get_size()
                    target_h = 30
                    new_w = max(1, int(orig_w * target_h / orig_h))
                    self.fire_image = pygame.transform.scale(
                        base_fire, (new_w, target_h)
                    )
                else:
                    self.fire_image = None
            except pygame.error as e:
                print(f"Erro ao carregar imagem do foguinho: {e}")
                self.fire_image = None

            # Carregar imagens dos mísseis usando cache
            try:
                self.missile_right = cache.get_image(
                    "imagens/elementos/missil-right.png", (20, 8)
                )
                self.missile_left = cache.get_image(
                    "imagens/elementos/missil-left.png", (20, 8)
                )

                # Organizar imagens em dicionário para facilitar o uso
                self.missile_images = {
                    "right": self.missile_right,
                    "left": self.missile_left,
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens dos mísseis: {e}")
                self.missile_images = None

            # Carregar imagem do tiro usando cache (seta)
            self.bullet_img = cache.get_image("imagens/elementos/arrow.png", (15, 8))
            self.bullet_image = self.bullet_img  # Alias para compatibilidade

            # Carregar imagem da explosão usando cache
            self.explosion_img = cache.get_image(
                "imagens/elementos/explosao.png", (40, 40)
            )
            self.explosion_image = self.explosion_img  # Alias para compatibilidade

            # Carregar imagem da gota de chuva (elemento das fases 7-10)
            try:
                self.raindrop_img = cache.get_image(
                    "imagens/elementos/chuva.png", (20, 20)
                )
            except pygame.error as e:
                print(f"Erro ao carregar imagem da gota de chuva: {e}")
                self.raindrop_img = None

            try:
                self.lava_drop_img = cache.get_image(
                    "imagens/elementos/lava.png", (20, 20)
                )
            except pygame.error as e:
                print(f"Erro ao carregar imagem da gota de lava: {e}")
                self.lava_drop_img = None

            # Geradores e raios (fases 37-40)
            try:
                self.generator_img = cache.get_image(
                    "imagens/elementos/gerador.png", (32, 32)
                )
            except pygame.error:
                self.generator_img = None
            try:
                base_h = cache.get_image("imagens/elementos/raioHorizontal.png")
                self.lightning_h_img = (
                    pygame.transform.scale(base_h, (12, 6)) if base_h else None
                )
            except pygame.error:
                self.lightning_h_img = None
            try:
                base_v = cache.get_image("imagens/elementos/raioVertical.png")
                self.lightning_v_img = (
                    pygame.transform.scale(base_v, (6, 12)) if base_v else None
                )
            except pygame.error:
                self.lightning_v_img = None

            # Carregar imagem de vida extra (item colecionável)
            self.extra_life_img = cache.get_image(
                "imagens/elementos/vida.png", (24, 24)
            )

            # Carregar imagens de power-ups (itens colecionáveis)
            # Tamanho igual ao da vida extra para consistência visual
            self.powerup_invincibility_img = cache.get_image(
                "imagens/elementos/invencibilidade.png", (24, 24)
            )
            self.powerup_double_jump_img = cache.get_image(
                "imagens/elementos/superpulo.png", (24, 24)
            )
            self.powerup_shield_img = cache.get_image(
                "imagens/elementos/protecao.png", (24, 24)
            )
            # Power-up Tempo (lentidão dos inimigos)
            self.powerup_tempo_img = cache.get_image(
                "imagens/elementos/tempo.png", (24, 24)
            )
            # Power-up SuperTiro (rajada + velocidade dos tiros do jogador)
            self.powerup_super_shot_img = cache.get_image(
                "imagens/elementos/supertiro.png", (24, 24)
            )

            # Bolha do escudo (overlay que envolve o personagem)
            # Carregada sem escala para permitir ajuste dinâmico conforme tamanho do player
            self.shield_bubble_img = cache.get_image(
                "imagens/elementos/bolha.png"
            )

            # Carregar logos para splash screen usando cache
            logo_files = ["cirrastec.png", "cirrasretrogames.png", "canaldodudu.png"]
            self.logos = []
            for logo_file in logo_files:
                try:
                    logo_path = f"imagens/logos/{logo_file}"
                    # Primeiro carregar sem escala para calcular dimensões
                    temp_logo = cache.get_image(logo_path)
                    if temp_logo:
                        logo_rect = temp_logo.get_rect()
                        if logo_rect.width > 400 or logo_rect.height > 300:
                            scale_factor = min(
                                400 / logo_rect.width, 300 / logo_rect.height
                            )
                            new_width = int(logo_rect.width * scale_factor)
                            new_height = int(logo_rect.height * scale_factor)
                            logo_img = cache.get_image(
                                logo_path, (new_width, new_height)
                            )
                        else:
                            logo_img = temp_logo
                        self.logos.append(logo_img)
                except pygame.error:
                    print(f"Erro ao carregar logo: {logo_file}")

            # Carregar logo principal do jogo usando cache
            try:
                # Primeiro carregar sem escala para calcular dimensões
                temp_game_logo = cache.get_image("imagens/logos/game.png")
                if temp_game_logo:
                    logo_rect = temp_game_logo.get_rect()
                    if logo_rect.width > 300 or logo_rect.height > 200:
                        scale_factor = min(
                            300 / logo_rect.width, 200 / logo_rect.height
                        )
                        new_width = int(logo_rect.width * scale_factor)
                        new_height = int(logo_rect.height * scale_factor)
                        self.game_logo = cache.get_image(
                            "imagens/logos/game.png", (new_width, new_height)
                        )
                    else:
                        self.game_logo = temp_game_logo
                else:
                    self.game_logo = None
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
