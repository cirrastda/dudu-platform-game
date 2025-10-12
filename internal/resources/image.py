import pygame
from internal.resources.cache import ResourceCache
from internal.utils.functions import resource_path
from internal.utils.constants import WIDTH, HEIGHT
from internal.engine.level.level import Level


class Image:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)

    def load_images(self):
        """Carregar todas as imagens do jogo usando sistema de cache"""
        try:
            # Inicializar cache de recursos
            cache = ResourceCache()

            # Carregar fundo baseado no nível atual (apenas para gameplay)
            background_file = Level.get_background_for_level(self, self.current_level)
            self.background_img = cache.get_image(background_file, (WIDTH, HEIGHT))

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

            # Carregar imagens dos pássaros usando cache
            self.bird_img1 = cache.get_image("imagens/inimigos/bird1.png", (40, 30))
            self.bird_img2 = cache.get_image("imagens/inimigos/bird2.png", (40, 30))

            # Carregar imagens dos morcegos usando cache
            self.bat_img1 = cache.get_image("imagens/inimigos/bat1.png", (40, 30))
            self.bat_img2 = cache.get_image("imagens/inimigos/bat2.png", (40, 30))
            self.bat_img3 = cache.get_image("imagens/inimigos/bat3.png", (40, 30))

            # Carregar imagens dos aviões usando cache
            self.airplane_img1 = cache.get_image("imagens/inimigos/airplane1.png", (50, 30))
            self.airplane_img2 = cache.get_image("imagens/inimigos/airplane2.png", (50, 30))
            self.airplane_img3 = cache.get_image("imagens/inimigos/airplane3.png", (50, 30))

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
                    "shot_left": [self.robot_shot_left1, self.robot_shot_left2, self.robot_shot_left3],
                    "shot_right": [self.robot_shot_right1, self.robot_shot_right2, self.robot_shot_right3],
                }
            except pygame.error as e:
                print(f"Erro ao carregar imagens dos robôs: {e}")
                self.robot_images = None

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

            # Carregar imagem do tiro usando cache
            self.bullet_img = cache.get_image("imagens/elementos/tiro.png", (15, 8))
            self.bullet_image = self.bullet_img  # Alias para compatibilidade

            # Carregar imagem da explosão usando cache
            self.explosion_img = cache.get_image(
                "imagens/elementos/explosao.png", (40, 40)
            )
            self.explosion_image = self.explosion_img  # Alias para compatibilidade

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
