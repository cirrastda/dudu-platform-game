import pygame
from internal.utils.constants import *
from internal.resources.platform import Platform
from internal.resources.flag import Flag
from internal.resources.cache import ResourceCache
from internal.engine.level.generator.static import StaticLevelGenerator
from internal.resources.player import Player
from internal.resources.enemies.turtle import Turtle


class Level:

    def get_birds_per_spawn(level):
        # Progressão equilibrada focando mais no intervalo que na quantidade
        # Pássaros por spawn: máximo 3 para manter jogabilidade
        # Intervalo de spawn: principal fator de dificuldade

        if level <= 20:
            # Cálculo gradual baseado no nível (1-20)
            level_progress = (level - 1) / 19.0  # 0.0 a 1.0

            # Pássaros por spawn: progressão gradual até o máximo
            if level <= 4:
                return 1
            elif level <= 15:
                return 2
            elif level <= 17:
                return 3
            else:  # Níveis 18-20: reduzir para 2 pássaros
                return 2
        elif level <= 30:
            # Níveis 21-30: usar morcegos seguindo EXATAMENTE o mesmo padrão dos pássaros das fases 11-20
            equivalent_bird_level = level - 10  # 21->11, 22->12, etc.
            level_progress = (
                equivalent_bird_level - 1
            ) / 19.0  # 0.0 a 1.0 (mesmo cálculo das fases 11-20)

            # Morcegos por spawn: seguir EXATAMENTE o mesmo padrão dos pássaros das fases 11-20
            if equivalent_bird_level <= 4:  # Fases 21-24 (equivalente a 11-14)
                return 1
            elif (
                equivalent_bird_level <= 15
            ):  # Fases 25-32 (equivalente a 15-22, mas limitado a 30)
                return 2
            elif equivalent_bird_level <= 17:  # Fase 30 (equivalente a 20)
                return 3
            else:  # Níveis além de 30
                return 2
        else:
            return 2

    def get_bird_spawn_interval(level):
        # Progressão equilibrada focando mais no intervalo que na quantidade
        # Pássaros por spawn: máximo 3 para manter jogabilidade
        # Intervalo de spawn: principal fator de dificuldade

        if level <= 20:
            # Cálculo gradual baseado no nível (1-20)
            level_progress = (level - 1) / 19.0  # 0.0 a 1.0
            # Intervalo de spawn: 180 no nível 1, até 70 no nível 20 (menos agressivo)
            if level <= 16:
                return max(60, int(180 - (level_progress * 120)))
            else:  # Níveis 17-20: intervalo maior para compensar
                return max(70, int(90 - (level - 17) * 5))
        elif level <= 30:
            # Níveis 21-30: usar morcegos seguindo EXATAMENTE o mesmo padrão dos pássaros das fases 11-20
            equivalent_bird_level = level - 10  # 21->11, 22->12, etc.
            level_progress = (
                equivalent_bird_level - 1
            ) / 19.0  # 0.0 a 1.0 (mesmo cálculo das fases 11-20)
            # Intervalo de spawn: seguir EXATAMENTE o mesmo padrão dos pássaros das fases 11-20
            if equivalent_bird_level <= 16:  # Fases 21-26 (equivalente a 11-16)
                return max(60, int(180 - (level_progress * 120)))
            else:  # Fases 27-30 (equivalente a 17-20): intervalo maior para compensar
                return max(70, int(90 - (equivalent_bird_level - 17) * 5))
        else:
            # Níveis além de 30 (futuras expansões)
            # Mantém dificuldade máxima jogável
            return max(60, 70 - min(10, (level - 20)))  # Mínimo 60

    def get_background_for_level(self, level):
        """Retorna o arquivo de fundo apropriado para o nível"""
        if 1 <= level <= 10:
            return "imagens/fundo3.png"
        elif 11 <= level <= 20:
            return "imagens/fundo5.png"
        elif 21 <= level <= 30:
            return "imagens/fundo7.png"
        elif 31 <= level <= 40:
            return "imagens/fundoMundo4.2.jpg"
        elif 41 <= level <= 50:
            # Mundo espacial: usar fundo do espaço
            return "imagens/fundoEspaco.png"
        else:
            # Fallback para níveis fora do range esperado
            return "imagens/fundo6.png"

    def draw_level_bg(self, level):
        # Atualizar fundo baseado no nível atual
        cache = ResourceCache()
        background_file = Level.get_background_for_level(self, level)
        return cache.get_image(background_file, (WIDTH, HEIGHT))

    def create_level_platforms(self, level):
        if level == 1:
            StaticLevelGenerator.create_level_1(self)
        elif level == 2:
            StaticLevelGenerator.create_level_2(self)
        elif level == 3:
            StaticLevelGenerator.create_level_3(self)
        elif level == 4:
            StaticLevelGenerator.create_level_4(self)
        elif level == 5:
            StaticLevelGenerator.create_level_5(self)
        elif level == 6:
            StaticLevelGenerator.create_level_6(self)
        elif level == 7:
            StaticLevelGenerator.create_level_7(self)
        elif level == 8:
            StaticLevelGenerator.create_level_8(self)
        elif level == 9:
            StaticLevelGenerator.create_level_9(self)
        elif level == 10:
            StaticLevelGenerator.create_level_10(self)
        elif level == 11:
            StaticLevelGenerator.create_level_11(self)
        elif level == 12:
            StaticLevelGenerator.create_level_12(self)
        elif level == 13:
            StaticLevelGenerator.create_level_13(self)
        elif level == 14:
            StaticLevelGenerator.create_level_14(self)
        elif level == 15:
            StaticLevelGenerator.create_level_15(self)
        elif level == 16:
            StaticLevelGenerator.create_level_16(self)
        elif level == 17:
            StaticLevelGenerator.create_level_17(self)
        elif level == 18:
            StaticLevelGenerator.create_level_18(self)
        elif level == 19:
            StaticLevelGenerator.create_level_19(self)
        elif level == 20:
            StaticLevelGenerator.create_level_20(self)
        elif level == 21:
            StaticLevelGenerator.create_level_21(self)
        elif level == 22:
            StaticLevelGenerator.create_level_22(self)
        elif level == 23:
            StaticLevelGenerator.create_level_23(self)
        elif level == 24:
            StaticLevelGenerator.create_level_24(self)
        elif level == 25:
            StaticLevelGenerator.create_level_25(self)
        elif level == 26:
            StaticLevelGenerator.create_level_26(self)
        elif level == 27:
            StaticLevelGenerator.create_level_27(self)
        elif level == 28:
            StaticLevelGenerator.create_level_28(self)
        elif level == 29:
            StaticLevelGenerator.create_level_29(self)
        elif level == 30:
            StaticLevelGenerator.create_level_30(self)
        elif level == 31:
            StaticLevelGenerator.create_level_31(self)
        elif level == 32:
            StaticLevelGenerator.create_level_32(self)
        elif level == 33:
            StaticLevelGenerator.create_level_33(self)
        elif level == 34:
            StaticLevelGenerator.create_level_34(self)
        elif level == 35:
            StaticLevelGenerator.create_level_35(self)
        elif level == 36:
            StaticLevelGenerator.create_level_36(self)
        elif level == 37:
            StaticLevelGenerator.create_level_37(self)
        elif level == 38:
            StaticLevelGenerator.create_level_38(self)
        elif level == 39:
            StaticLevelGenerator.create_level_39(self)
        elif level == 40:
            StaticLevelGenerator.create_level_40(self)
        elif level == 41:
            StaticLevelGenerator.create_level_41(self)
        elif level == 42:
            StaticLevelGenerator.create_level_42(self)
        elif level == 43:
            StaticLevelGenerator.create_level_43(self)
        elif level == 44:
            StaticLevelGenerator.create_level_44(self)
        elif level == 45:
            StaticLevelGenerator.create_level_45(self)
        elif level == 46:
            StaticLevelGenerator.create_level_46(self)
        elif level == 47:
            StaticLevelGenerator.create_level_47(self)
        elif level == 48:
            StaticLevelGenerator.create_level_48(self)
        elif level == 49:
            StaticLevelGenerator.create_level_49(self)
        elif level == 50:
            StaticLevelGenerator.create_level_50(self)

    def init_level(game):
        """Inicializar o nível atual"""
        game.player = Player(50, HEIGHT - 200)
        game.platforms = []
        game.flag = None
        game.camera_x = 0
        # Reinicializar sistema de pássaros
        game.birds = []
        game.bird_spawn_timer = 0
        # Reinicializar sistema de morcegos
        game.bats = []
        game.bat_spawn_timer = 0
        # Reinicializar sistema de tartarugas
        game.turtles = []
        # Reinicializar sistema de aranhas
        game.spiders = []
        # Reinicializar sistema de robôs
        game.robots = []
        # Reinicializar sistema de aliens (níveis 41-50)
        game.aliens = []
        game.orphan_lasers = []
        # Reinicializar explosões
        game.explosions = []
        # Reinicializar sistema de flying-disk (níveis 41-50)
        game.flying_disks = []
        game.flying_disk_spawn_timer = 0

        # Atualizar dificuldade dos pássaros para o nível atual
        game.update_bird_difficulty()
        game.background_img = Level.draw_level_bg(game, game.current_level)

        # Garantir que o fundo do menu permanece inalterado
        if not hasattr(game, "menu_background_img") or game.menu_background_img is None:
            game.menu_background_img = cache.get_image(
                "imagens/fundo6.png", (WIDTH, HEIGHT)
            )

        # Pool de objetos para performance
        if not hasattr(game, "bullet_pool"):
            game.bullet_pool = []
        if not hasattr(game, "explosion_pool"):
            game.explosion_pool = []
        # Não resetar platforms_jumped aqui para manter pontuação entre níveis

        # Criar plataformas baseadas no nível
        Level.create_level_platforms(game, game.current_level)

    def drawTurtle(game, platform):
        turtle = Turtle(
            platform[0],
            platform[1] - 30,
            platform[0],
            platform[0] + platform[2],
            game.turtle_images,
        )
        game.turtles.append(turtle)
