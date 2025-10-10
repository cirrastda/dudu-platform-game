import pygame
from internal.engine.level.enemy import LevelEnemy
from internal.utils.constants import *
from internal.resources.platform import Platform
from internal.resources.flag import Flag
from internal.resources.cache import ResourceCache
from internal.resources.enemies.turtle import Turtle


class StaticLevelGenerator:
    limit_platform_y = HEIGHT - 50
    limit_platform_yTop = 100

    def create_level_1(game):
        """Nível 1 - Fácil (20 plataformas)"""
        platforms = [
            (100, HEIGHT - 150, 120, 20),
            (300, HEIGHT - 200, 120, 20),
            (500, HEIGHT - 120, 120, 20),
            (700, HEIGHT - 180, 120, 20),
            (900, HEIGHT - 100, 120, 20),
            (1100, HEIGHT - 160, 120, 20),
            (1300, HEIGHT - 220, 120, 20),
            (1500, HEIGHT - 140, 120, 20),
            (1700, HEIGHT - 190, 120, 20),
            (1900, HEIGHT - 110, 120, 20),
            (2100, HEIGHT - 170, 120, 20),
            (2300, HEIGHT - 230, 120, 20),
            (2500, HEIGHT - 130, 120, 20),
            (2700, HEIGHT - 200, 120, 20),
            (2900, HEIGHT - 150, 120, 20),
            (3100, HEIGHT - 180, 120, 20),
            (3300, HEIGHT - 120, 120, 20),
            (3500, HEIGHT - 210, 120, 20),
            (3700, HEIGHT - 160, 120, 20),
            (3900, HEIGHT - 140, 120, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)
        StaticLevelGenerator.putPlayerInFirstPlatform(game)
        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_2(game):
        """Nível 2 - Médio (30 plataformas)"""
        platforms = [
            (120, HEIGHT - 180, 100, 20),
            (280, HEIGHT - 250, 100, 20),
            (440, HEIGHT - 150, 100, 20),
            (600, HEIGHT - 300, 100, 20),
            (760, HEIGHT - 200, 100, 20),
            (920, HEIGHT - 120, 100, 20),
            (1080, HEIGHT - 280, 100, 20),
            (1240, HEIGHT - 160, 100, 20),
            (1400, HEIGHT - 320, 100, 20),
            (1560, HEIGHT - 180, 100, 20),
            (1720, HEIGHT - 240, 100, 20),
            (1880, HEIGHT - 140, 100, 20),
            (2040, HEIGHT - 300, 100, 20),
            (2200, HEIGHT - 200, 100, 20),
            (2360, HEIGHT - 120, 100, 20),
            (2520, HEIGHT - 280, 100, 20),
            (2680, HEIGHT - 160, 100, 20),
            (2840, HEIGHT - 340, 100, 20),
            (3000, HEIGHT - 220, 100, 20),
            (3160, HEIGHT - 140, 100, 20),
            (3320, HEIGHT - 300, 100, 20),
            (3480, HEIGHT - 180, 100, 20),
            (3640, HEIGHT - 260, 100, 20),
            (3800, HEIGHT - 120, 100, 20),
            (3960, HEIGHT - 320, 100, 20),
            (4120, HEIGHT - 200, 100, 20),
            (4280, HEIGHT - 140, 100, 20),
            (4440, HEIGHT - 280, 100, 20),
            (4600, HEIGHT - 160, 100, 20),
            (4760, HEIGHT - 240, 100, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_3(game):
        """Nível 3 - Médio-Difícil (40 plataformas) - Corrigido para pulos possíveis"""
        platforms = [
            (100, HEIGHT - 200, 80, 20),
            (240, HEIGHT - 300, 80, 20),
            (380, HEIGHT - 180, 80, 20),
            (520, HEIGHT - 310, 80, 20),
            (660, HEIGHT - 220, 80, 20),
            (800, HEIGHT - 350, 80, 20),
            (940, HEIGHT - 150, 80, 20),
            (1080, HEIGHT - 280, 80, 20),
            (1220, HEIGHT - 180, 80, 20),
            (1360, HEIGHT - 310, 80, 20),
            (1500, HEIGHT - 240, 80, 20),
            (1640, HEIGHT - 140, 80, 20),
            (1780, HEIGHT - 270, 80, 20),
            (1920, HEIGHT - 200, 80, 20),
            (2060, HEIGHT - 330, 80, 20),
            (2200, HEIGHT - 160, 80, 20),
            (2340, HEIGHT - 290, 80, 20),
            (2480, HEIGHT - 220, 80, 20),
            (2620, HEIGHT - 120, 80, 20),
            (2760, HEIGHT - 250, 80, 20),
            (2900, HEIGHT - 180, 80, 20),
            (3040, HEIGHT - 310, 80, 20),
            (3180, HEIGHT - 240, 80, 20),
            (3320, HEIGHT - 140, 80, 20),
            (3460, HEIGHT - 270, 80, 20),
            (3600, HEIGHT - 200, 80, 20),
            (3740, HEIGHT - 330, 80, 20),
            (3880, HEIGHT - 160, 80, 20),
            (4020, HEIGHT - 290, 80, 20),
            (4160, HEIGHT - 220, 80, 20),
            (4300, HEIGHT - 120, 80, 20),
            (4440, HEIGHT - 250, 80, 20),
            (4580, HEIGHT - 180, 80, 20),
            (4720, HEIGHT - 310, 80, 20),
            (4860, HEIGHT - 240, 80, 20),
            (5000, HEIGHT - 140, 80, 20),
            (5140, HEIGHT - 270, 80, 20),
            (5280, HEIGHT - 200, 80, 20),
            (5420, HEIGHT - 330, 80, 20),
            (5560, HEIGHT - 280, 80, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_4(game):
        """Nível 4 - Difícil (50 plataformas) - Versão corrigida sem plataformas extras"""
        # Limpar plataformas existentes para garantir que não há duplicatas
        game.platforms.clear()

        platforms = [
            (80, HEIGHT - 220, 70, 20),
            (200, HEIGHT - 350, 70, 20),
            (320, HEIGHT - 180, 70, 20),
            (440, HEIGHT - 400, 70, 20),
            (560, HEIGHT - 250, 70, 20),
            (680, HEIGHT - 450, 70, 20),
            (800, HEIGHT - 160, 70, 20),
            (920, HEIGHT - 380, 70, 20),
            (1040, HEIGHT - 200, 70, 20),
            (1160, HEIGHT - 420, 70, 20),
            (1280, HEIGHT - 280, 70, 20),
            (1400, HEIGHT - 140, 70, 20),
            (1520, HEIGHT - 360, 70, 20),
            (1640, HEIGHT - 220, 70, 20),
            (1760, HEIGHT - 480, 70, 20),
            (1880, HEIGHT - 160, 70, 20),
            (2000, HEIGHT - 340, 70, 20),
            (2120, HEIGHT - 240, 70, 20),
            (2240, HEIGHT - 120, 70, 20),
            (2360, HEIGHT - 400, 70, 20),
            (2480, HEIGHT - 180, 70, 20),
            (2600, HEIGHT - 460, 70, 20),
            (2720, HEIGHT - 260, 70, 20),
            (2840, HEIGHT - 140, 70, 20),
            (2960, HEIGHT - 380, 70, 20),
            (3080, HEIGHT - 200, 70, 20),
            (3200, HEIGHT - 500, 70, 20),
            (3320, HEIGHT - 160, 70, 20),
            (3440, HEIGHT - 320, 70, 20),
            (3560, HEIGHT - 240, 70, 20),
            (3680, HEIGHT - 120, 70, 20),
            (3800, HEIGHT - 420, 70, 20),
            (3920, HEIGHT - 180, 70, 20),
            (4040, HEIGHT - 480, 70, 20),
            (4160, HEIGHT - 280, 70, 20),
            (4280, HEIGHT - 140, 70, 20),
            (4400, HEIGHT - 360, 70, 20),
            (4520, HEIGHT - 220, 70, 20),
            (4640, HEIGHT - 520, 70, 20),
            (4760, HEIGHT - 160, 70, 20),
            (4880, HEIGHT - 340, 70, 20),
            (5000, HEIGHT - 260, 70, 20),
            (5120, HEIGHT - 120, 70, 20),
            (5240, HEIGHT - 400, 70, 20),
            (5360, HEIGHT - 200, 70, 20),
            # Removidas as 5 plataformas extras que estavam após a bandeira
        ]

        # Adicionar apenas as 50 plataformas definidas
        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_5(game):
        """Nível 5 - Muito Difícil (60 plataformas)"""
        platforms = [
            (60, HEIGHT - 250, 60, 20),
            (170, HEIGHT - 400, 60, 20),
            (280, HEIGHT - 180, 60, 20),
            (390, HEIGHT - 450, 60, 20),
            (500, HEIGHT - 280, 60, 20),
            (610, HEIGHT - 500, 60, 20),
            (720, HEIGHT - 160, 60, 20),
            (830, HEIGHT - 420, 60, 20),
            (940, HEIGHT - 240, 60, 20),
            (1050, HEIGHT - 480, 60, 20),
            (1160, HEIGHT - 200, 60, 20),
            (1270, HEIGHT - 380, 60, 20),
            (1380, HEIGHT - 140, 60, 20),
            (1490, HEIGHT - 460, 60, 20),
            (1600, HEIGHT - 260, 60, 20),
            (1710, HEIGHT - 520, 60, 20),
            (1820, HEIGHT - 180, 60, 20),
            (1930, HEIGHT - 340, 60, 20),
            (2040, HEIGHT - 220, 60, 20),
            (2150, HEIGHT - 500, 60, 20),
            (2260, HEIGHT - 160, 60, 20),
            (2370, HEIGHT - 400, 60, 20),
            (2480, HEIGHT - 280, 60, 20),
            (2590, HEIGHT - 540, 60, 20),
            (2700, HEIGHT - 200, 60, 20),
            (2810, HEIGHT - 360, 60, 20),
            (2920, HEIGHT - 240, 60, 20),
            (3030, HEIGHT - 480, 60, 20),
            (3140, HEIGHT - 140, 60, 20),
            (3250, HEIGHT - 420, 60, 20),
            (3360, HEIGHT - 300, 60, 20),
            (3470, HEIGHT - 560, 60, 20),
            (3580, HEIGHT - 180, 60, 20),
            (3690, HEIGHT - 340, 60, 20),
            (3800, HEIGHT - 260, 60, 20),
            (3910, HEIGHT - 500, 60, 20),
            (4020, HEIGHT - 160, 60, 20),
            (4130, HEIGHT - 380, 60, 20),
            (4240, HEIGHT - 220, 60, 20),
            (4350, HEIGHT - 520, 60, 20),
            (4460, HEIGHT - 280, 60, 20),
            (4570, HEIGHT - 140, 60, 20),
            (4680, HEIGHT - 400, 60, 20),
            (4790, HEIGHT - 240, 60, 20),
            (4900, HEIGHT - 540, 60, 20),
            (5010, HEIGHT - 180, 60, 20),
            (5120, HEIGHT - 360, 60, 20),
            (5230, HEIGHT - 300, 60, 20),
            (5340, HEIGHT - 480, 60, 20),
            (5450, HEIGHT - 160, 60, 20),
            (5560, HEIGHT - 420, 60, 20),
            (5670, HEIGHT - 260, 60, 20),
            (5780, HEIGHT - 520, 60, 20),
            (5890, HEIGHT - 200, 60, 20),
            (6000, HEIGHT - 380, 60, 20),
            (6110, HEIGHT - 240, 60, 20),
            (6220, HEIGHT - 500, 60, 20),
            (6330, HEIGHT - 180, 60, 20),
            (6440, HEIGHT - 340, 60, 20),
            (6550, HEIGHT - 280, 60, 20),
            (6660, HEIGHT - 460, 60, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_6(game):
        """Nível 6 - Progressão (65 plataformas)"""
        platforms = [
            (80, HEIGHT - 240, 60, 20),
            (200, HEIGHT - 380, 60, 20),
            (320, HEIGHT - 160, 60, 20),
            (440, HEIGHT - 420, 60, 20),
            (560, HEIGHT - 260, 60, 20),
            (680, HEIGHT - 480, 60, 20),
            (800, HEIGHT - 140, 60, 20),
            (920, HEIGHT - 400, 60, 20),
            (1040, HEIGHT - 220, 60, 20),
            (1160, HEIGHT - 460, 60, 20),
            (1280, HEIGHT - 180, 60, 20),
            (1400, HEIGHT - 360, 60, 20),
            (1520, HEIGHT - 120, 60, 20),
            (1640, HEIGHT - 440, 60, 20),
            (1760, HEIGHT - 280, 60, 20),
            (1880, HEIGHT - 500, 60, 20),
            (2000, HEIGHT - 160, 60, 20),
            (2120, HEIGHT - 320, 60, 20),
            (2240, HEIGHT - 200, 60, 20),
            (2360, HEIGHT - 480, 60, 20),
            (2480, HEIGHT - 140, 60, 20),
            (2600, HEIGHT - 380, 60, 20),
            (2720, HEIGHT - 260, 60, 20),
            (2840, HEIGHT - 520, 60, 20),
            (2960, HEIGHT - 180, 60, 20),
            (3080, HEIGHT - 340, 60, 20),
            (3200, HEIGHT - 220, 60, 20),
            (3320, HEIGHT - 460, 60, 20),
            (3440, HEIGHT - 120, 60, 20),
            (3560, HEIGHT - 400, 60, 20),
            (3680, HEIGHT - 280, 60, 20),
            (3800, HEIGHT - 540, 60, 20),
            (3920, HEIGHT - 160, 60, 20),
            (4040, HEIGHT - 320, 60, 20),
            (4160, HEIGHT - 240, 60, 20),
            (4280, HEIGHT - 480, 60, 20),
            (4400, HEIGHT - 140, 60, 20),
            (4520, HEIGHT - 360, 60, 20),
            (4640, HEIGHT - 200, 60, 20),
            (4760, HEIGHT - 500, 60, 20),
            (4880, HEIGHT - 180, 60, 20),
            (5000, HEIGHT - 340, 60, 20),
            (5120, HEIGHT - 260, 60, 20),
            (5240, HEIGHT - 460, 60, 20),
            (5360, HEIGHT - 120, 60, 20),
            (5480, HEIGHT - 380, 60, 20),
            (5600, HEIGHT - 220, 60, 20),
            (5720, HEIGHT - 520, 60, 20),
            (5840, HEIGHT - 160, 60, 20),
            (5960, HEIGHT - 320, 60, 20),
            (6080, HEIGHT - 240, 60, 20),
            (6200, HEIGHT - 480, 60, 20),
            (6320, HEIGHT - 140, 60, 20),
            (6440, HEIGHT - 360, 60, 20),
            (6560, HEIGHT - 280, 60, 20),
            (6680, HEIGHT - 500, 60, 20),
            (6800, HEIGHT - 180, 60, 20),
            (6920, HEIGHT - 340, 60, 20),
            (7040, HEIGHT - 220, 60, 20),
            (7160, HEIGHT - 460, 60, 20),
            (7280, HEIGHT - 160, 60, 20),
            (7400, HEIGHT - 380, 60, 20),
            (7520, HEIGHT - 260, 60, 20),
            (7640, HEIGHT - 480, 60, 20),
            (7760, HEIGHT - 200, 60, 20),
            (7880, HEIGHT - 340, 60, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_7(game):
        """Nível 7 - Progressão (68 plataformas)"""
        platforms = [
            (140, HEIGHT - 220, 60, 20),
            (300, HEIGHT - 300, 60, 20),
            (470, HEIGHT - 160, 60, 20),
            (640, HEIGHT - 280, 60, 20),
            (810, HEIGHT - 200, 60, 20),
            (980, HEIGHT - 340, 60, 20),
            (1150, HEIGHT - 140, 60, 20),
            (1320, HEIGHT - 260, 60, 20),
            (1490, HEIGHT - 320, 60, 20),
            (1660, HEIGHT - 180, 60, 20),
            (1830, HEIGHT - 240, 60, 20),
            (2000, HEIGHT - 300, 60, 20),
            (2170, HEIGHT - 160, 60, 20),
            (2340, HEIGHT - 280, 60, 20),
            (2510, HEIGHT - 220, 60, 20),
            (2680, HEIGHT - 340, 60, 20),
            (2850, HEIGHT - 180, 60, 20),
            (3020, HEIGHT - 260, 60, 20),
            (3190, HEIGHT - 300, 60, 20),
            (3360, HEIGHT - 140, 60, 20),
            (3530, HEIGHT - 240, 60, 20),
            (3700, HEIGHT - 320, 60, 20),
            (3870, HEIGHT - 200, 60, 20),
            (4040, HEIGHT - 280, 60, 20),
            (4210, HEIGHT - 160, 60, 20),
            (4380, HEIGHT - 300, 60, 20),
            (4550, HEIGHT - 220, 60, 20),
            (4720, HEIGHT - 260, 60, 20),
            (4890, HEIGHT - 340, 60, 20),
            (5060, HEIGHT - 180, 60, 20),
            (5230, HEIGHT - 240, 60, 20),
            (5400, HEIGHT - 300, 60, 20),
            (5570, HEIGHT - 160, 60, 20),
            (5740, HEIGHT - 280, 60, 20),
            (5910, HEIGHT - 220, 60, 20),
            (6080, HEIGHT - 340, 60, 20),
            (6250, HEIGHT - 140, 60, 20),
            (6420, HEIGHT - 260, 60, 20),
            (6590, HEIGHT - 320, 60, 20),
            (6760, HEIGHT - 180, 60, 20),
            (6930, HEIGHT - 240, 60, 20),
            (7100, HEIGHT - 300, 60, 20),
            (7270, HEIGHT - 160, 60, 20),
            (7440, HEIGHT - 280, 60, 20),
            (7610, HEIGHT - 220, 60, 20),
            (7780, HEIGHT - 340, 60, 20),
            (7950, HEIGHT - 180, 60, 20),
            (8120, HEIGHT - 260, 60, 20),
            (8290, HEIGHT - 320, 60, 20),
            (8460, HEIGHT - 140, 60, 20),
            (8630, HEIGHT - 240, 60, 20),
            (8800, HEIGHT - 300, 60, 20),
            (8970, HEIGHT - 160, 60, 20),
            (9140, HEIGHT - 280, 60, 20),
            (9310, HEIGHT - 220, 60, 20),
            (9480, HEIGHT - 340, 60, 20),
            (9650, HEIGHT - 180, 60, 20),
            (9820, HEIGHT - 260, 60, 20),
            (9990, HEIGHT - 320, 60, 20),
            (10160, HEIGHT - 140, 60, 20),
            (10330, HEIGHT - 240, 60, 20),
            (10500, HEIGHT - 300, 60, 20),
            (10670, HEIGHT - 160, 60, 20),
            (10840, HEIGHT - 280, 60, 20),
            (11010, HEIGHT - 220, 60, 20),
            (11180, HEIGHT - 340, 60, 20),
            (11350, HEIGHT - 180, 60, 20),
            (11520, HEIGHT - 260, 60, 20),
            (11690, HEIGHT - 320, 60, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_8(game):
        """Nível 8 - Progressão (70 plataformas)"""
        platforms = [
            (160, HEIGHT - 240, 60, 20),
            (340, HEIGHT - 320, 60, 20),
            (530, HEIGHT - 160, 60, 20),
            (720, HEIGHT - 280, 60, 20),
            (910, HEIGHT - 200, 60, 20),
            (1100, HEIGHT - 340, 60, 20),
            (1290, HEIGHT - 140, 60, 20),
            (1480, HEIGHT - 260, 60, 20),
            (1670, HEIGHT - 320, 60, 20),
            (1860, HEIGHT - 180, 60, 20),
            (2050, HEIGHT - 300, 60, 20),
            (2240, HEIGHT - 220, 60, 20),
            (2430, HEIGHT - 340, 60, 20),
            (2620, HEIGHT - 160, 60, 20),
            (2810, HEIGHT - 280, 60, 20),
            (3000, HEIGHT - 240, 60, 20),
            (3190, HEIGHT - 320, 60, 20),
            (3380, HEIGHT - 180, 60, 20),
            (3570, HEIGHT - 300, 60, 20),
            (3760, HEIGHT - 140, 60, 20),
            (3950, HEIGHT - 260, 60, 20),
            (4140, HEIGHT - 320, 60, 20),
            (4330, HEIGHT - 200, 60, 20),
            (4520, HEIGHT - 280, 60, 20),
            (4710, HEIGHT - 160, 60, 20),
            (4900, HEIGHT - 300, 60, 20),
            (5090, HEIGHT - 240, 60, 20),
            (5280, HEIGHT - 320, 60, 20),
            (5470, HEIGHT - 180, 60, 20),
            (5660, HEIGHT - 260, 60, 20),
            (5850, HEIGHT - 340, 60, 20),
            (6040, HEIGHT - 160, 60, 20),
            (6230, HEIGHT - 280, 60, 20),
            (6420, HEIGHT - 220, 60, 20),
            (6610, HEIGHT - 300, 60, 20),
            (6800, HEIGHT - 140, 60, 20),
            (6990, HEIGHT - 260, 60, 20),
            (7180, HEIGHT - 320, 60, 20),
            (7370, HEIGHT - 180, 60, 20),
            (7560, HEIGHT - 240, 60, 20),
            (7750, HEIGHT - 340, 60, 20),
            (7940, HEIGHT - 160, 60, 20),
            (8130, HEIGHT - 280, 60, 20),
            (8320, HEIGHT - 200, 60, 20),
            (8510, HEIGHT - 320, 60, 20),
            (8700, HEIGHT - 140, 60, 20),
            (8890, HEIGHT - 260, 60, 20),
            (9080, HEIGHT - 300, 60, 20),
            (9270, HEIGHT - 180, 60, 20),
            (9460, HEIGHT - 240, 60, 20),
            (9650, HEIGHT - 340, 60, 20),
            (9840, HEIGHT - 160, 60, 20),
            (10030, HEIGHT - 280, 60, 20),
            (10220, HEIGHT - 220, 60, 20),
            (10410, HEIGHT - 300, 60, 20),
            (10600, HEIGHT - 140, 60, 20),
            (10790, HEIGHT - 260, 60, 20),
            (10980, HEIGHT - 320, 60, 20),
            (11170, HEIGHT - 180, 60, 20),
            (11360, HEIGHT - 240, 60, 20),
            (11550, HEIGHT - 340, 60, 20),
            (11740, HEIGHT - 160, 60, 20),
            (11930, HEIGHT - 280, 60, 20),
            (12120, HEIGHT - 200, 60, 20),
            (12310, HEIGHT - 320, 60, 20),
            (12500, HEIGHT - 140, 60, 20),
            (12690, HEIGHT - 260, 60, 20),
            (12880, HEIGHT - 300, 60, 20),
            (13070, HEIGHT - 180, 60, 20),
            (13260, HEIGHT - 240, 60, 20),
            (13450, HEIGHT - 340, 60, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_9(game):
        """Nível 9 - Progressão (70 plataformas) - Gaps desafiadores mas possíveis"""
        platforms = [
            (180, HEIGHT - 260, 60, 20),
            (380, HEIGHT - 340, 60, 20),
            (580, HEIGHT - 160, 60, 20),
            (780, HEIGHT - 300, 60, 20),
            (980, HEIGHT - 200, 60, 20),
            (1180, HEIGHT - 340, 60, 20),
            (1380, HEIGHT - 140, 60, 20),
            (1580, HEIGHT - 280, 60, 20),
            (1780, HEIGHT - 320, 60, 20),
            (1980, HEIGHT - 180, 60, 20),
            (2180, HEIGHT - 300, 60, 20),
            (2380, HEIGHT - 240, 60, 20),
            (2580, HEIGHT - 340, 60, 20),
            (2780, HEIGHT - 160, 60, 20),
            (2980, HEIGHT - 280, 60, 20),
            (3180, HEIGHT - 260, 60, 20),
            (3380, HEIGHT - 320, 60, 20),
            (3580, HEIGHT - 180, 60, 20),
            (3780, HEIGHT - 300, 60, 20),
            (3980, HEIGHT - 140, 60, 20),
            (4180, HEIGHT - 280, 60, 20),
            (4380, HEIGHT - 320, 60, 20),
            (4580, HEIGHT - 200, 60, 20),
            (4780, HEIGHT - 300, 60, 20),
            (4980, HEIGHT - 160, 60, 20),
            (5180, HEIGHT - 320, 60, 20),
            (5380, HEIGHT - 240, 60, 20),
            (5580, HEIGHT - 300, 60, 20),
            (5780, HEIGHT - 180, 60, 20),
            (5980, HEIGHT - 280, 60, 20),
            (6180, HEIGHT - 260, 60, 20),
            (6380, HEIGHT - 320, 60, 20),
            (6580, HEIGHT - 180, 60, 20),
            (6780, HEIGHT - 300, 60, 20),
            (6980, HEIGHT - 240, 60, 20),
            (7180, HEIGHT - 340, 60, 20),
            (7380, HEIGHT - 160, 60, 20),
            (7580, HEIGHT - 280, 60, 20),
            (7780, HEIGHT - 320, 60, 20),
            (7980, HEIGHT - 200, 60, 20),
            (8180, HEIGHT - 300, 60, 20),
            (8380, HEIGHT - 140, 60, 20),
            (8580, HEIGHT - 280, 60, 20),
            (8780, HEIGHT - 260, 60, 20),
            (8980, HEIGHT - 340, 60, 20),
            (9180, HEIGHT - 180, 60, 20),
            (9380, HEIGHT - 320, 60, 20),
            (9580, HEIGHT - 240, 60, 20),
            (9780, HEIGHT - 300, 60, 20),
            (9980, HEIGHT - 160, 60, 20),
            (10180, HEIGHT - 280, 60, 20),
            (10380, HEIGHT - 320, 60, 20),
            (10580, HEIGHT - 200, 60, 20),
            (10780, HEIGHT - 340, 60, 20),
            (10980, HEIGHT - 140, 60, 20),
            (11180, HEIGHT - 280, 60, 20),
            (11380, HEIGHT - 260, 60, 20),
            (11580, HEIGHT - 320, 60, 20),
            (11780, HEIGHT - 180, 60, 20),
            (11980, HEIGHT - 300, 60, 20),
            (12180, HEIGHT - 240, 60, 20),
            (12380, HEIGHT - 340, 60, 20),
            (12580, HEIGHT - 160, 60, 20),
            (12780, HEIGHT - 280, 60, 20),
            (12980, HEIGHT - 320, 60, 20),
            (13180, HEIGHT - 200, 60, 20),
            (13380, HEIGHT - 300, 60, 20),
            (13580, HEIGHT - 140, 60, 20),
            (13780, HEIGHT - 280, 60, 20),
            (13980, HEIGHT - 260, 60, 20),
            (14180, HEIGHT - 340, 60, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_10(game):
        """Nível 10 - Progressão (70 plataformas) - Máxima dificuldade com saltos no limite"""
        platforms = [
            (200, HEIGHT - 280, 60, 20),
            (410, HEIGHT - 360, 60, 20),
            (620, HEIGHT - 160, 60, 20),
            (830, HEIGHT - 320, 60, 20),
            (1040, HEIGHT - 200, 60, 20),
            (1250, HEIGHT - 340, 60, 20),
            (1460, HEIGHT - 140, 60, 20),
            (1670, HEIGHT - 300, 60, 20),
            (1880, HEIGHT - 260, 60, 20),
            (2090, HEIGHT - 340, 60, 20),
            (2300, HEIGHT - 180, 60, 20),
            (2510, HEIGHT - 320, 60, 20),
            (2720, HEIGHT - 240, 60, 20),
            (2930, HEIGHT - 360, 60, 20),
            (3140, HEIGHT - 160, 60, 20),
            (3350, HEIGHT - 300, 60, 20),
            (3560, HEIGHT - 280, 60, 20),
            (3770, HEIGHT - 340, 60, 20),
            (3980, HEIGHT - 180, 60, 20),
            (4190, HEIGHT - 320, 60, 20),
            (4400, HEIGHT - 140, 60, 20),
            (4610, HEIGHT - 300, 60, 20),
            (4820, HEIGHT - 260, 60, 20),
            (5030, HEIGHT - 340, 60, 20),
            (5240, HEIGHT - 200, 60, 20),
            (5450, HEIGHT - 320, 60, 20),
            (5660, HEIGHT - 160, 60, 20),
            (5870, HEIGHT - 300, 60, 20),
            (6080, HEIGHT - 240, 60, 20),
            (6290, HEIGHT - 340, 60, 20),
            (6500, HEIGHT - 180, 60, 20),
            (6710, HEIGHT - 300, 60, 20),
            (6920, HEIGHT - 260, 60, 20),
            (7130, HEIGHT - 320, 60, 20),
            (7340, HEIGHT - 180, 60, 20),
            (7550, HEIGHT - 340, 60, 20),
            (7760, HEIGHT - 240, 60, 20),
            (7970, HEIGHT - 360, 60, 20),
            (8180, HEIGHT - 160, 60, 20),
            (8390, HEIGHT - 300, 60, 20),
            (8600, HEIGHT - 280, 60, 20),
            (8810, HEIGHT - 340, 60, 20),
            (9020, HEIGHT - 200, 60, 20),
            (9230, HEIGHT - 320, 60, 20),
            (9440, HEIGHT - 140, 60, 20),
            (9650, HEIGHT - 300, 60, 20),
            (9860, HEIGHT - 260, 60, 20),
            (10070, HEIGHT - 340, 60, 20),
            (10280, HEIGHT - 180, 60, 20),
            (10490, HEIGHT - 320, 60, 20),
            (10700, HEIGHT - 240, 60, 20),
            (10910, HEIGHT - 360, 60, 20),
            (11120, HEIGHT - 160, 60, 20),
            (11330, HEIGHT - 300, 60, 20),
            (11540, HEIGHT - 280, 60, 20),
            (11750, HEIGHT - 340, 60, 20),
            (11960, HEIGHT - 200, 60, 20),
            (12170, HEIGHT - 320, 60, 20),
            (12380, HEIGHT - 140, 60, 20),
            (12590, HEIGHT - 300, 60, 20),
            (12800, HEIGHT - 260, 60, 20),
            (13010, HEIGHT - 340, 60, 20),
            (13220, HEIGHT - 180, 60, 20),
            (13430, HEIGHT - 320, 60, 20),
            (13640, HEIGHT - 240, 60, 20),
            (13850, HEIGHT - 360, 60, 20),
            (14060, HEIGHT - 160, 60, 20),
            (14270, HEIGHT - 300, 60, 20),
            (14480, HEIGHT - 280, 60, 20),
            (14690, HEIGHT - 340, 60, 20),
            (14900, HEIGHT - 200, 60, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_11(game):
        """Nível 11 - Reinício com tartarugas (30 plataformas)"""
        platforms = []
        x_pos = 100
        initial_y = HEIGHT - 150
        y_pos = initial_y
        for i in range(31):
            y_pos -= 100
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 80, 20))
            x_pos += 120 + (i % 2) * 40

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 10 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 10)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_12(game):
        """Nível 12 - Progressão com tartarugas (39 plataformas)"""
        platforms = []
        x_pos = 90
        initial_y = HEIGHT - 120
        y_pos = initial_y
        for i in range(39):
            y_pos -= 110
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 75, 20))
            x_pos += 115 + (i % 3) * 35

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 9 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 9)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_13(game):
        """Nível 13 - Progressão com tartarugas (48 plataformas)"""
        platforms = []
        x_pos = 80
        initial_y = HEIGHT - 110
        y_pos = initial_y
        for i in range(49):
            y_pos -= 115
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 70, 20))
            x_pos += 110 + (i % 4) * 30

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 8 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 8)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_14(game):
        """Nível 14 - Progressão com tartarugas (58 plataformas)"""
        platforms = []
        x_pos = 70
        initial_y = HEIGHT - 100
        y_pos = initial_y
        for i in range(58):
            y_pos -= 115
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 65, 20))
            x_pos += 105 + (i % 5) * 25

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 7 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 7)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_15(game):
        """Nível 15 - Progressão com tartarugas (66 plataformas)"""
        platforms = []
        x_pos = 60
        initial_y = HEIGHT - 90
        y_pos = initial_y
        for i in range(67):
            y_pos -= 119
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 60, 20))
            x_pos += 100 + (i % 6) * 20

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 6 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 6)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_16(game):
        """Nível 16 - Progressão com tartarugas (75 plataformas)"""
        platforms = []
        x_pos = 50
        initial_y = HEIGHT - 120
        y_pos = initial_y
        for i in range(76):
            y_pos -= 125
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 55, 20))
            x_pos += 95 + (i % 7) * 15

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 5 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 5)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_17(game):
        """Nível 17 - Progressão com tartarugas (84 plataformas)"""
        platforms = []
        x_pos = 40
        initial_y = HEIGHT - 120
        y_pos = initial_y
        for i in range(84):
            y_pos -= 125
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 50, 20))
            x_pos += 90 + (i % 8) * 10

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 4 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 4)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_18(game):
        """Nível 18 - Progressão com tartarugas (93 plataformas)"""
        platforms = []
        x_pos = 30
        initial_y = HEIGHT - 120
        y_pos = initial_y
        for i in range(93):
            y_pos -= 125
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 45, 20))
            x_pos += 85 + (i % 9) * 5

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 3 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 3)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_19(game):
        """Nível 19 - Progressão com tartarugas (102 plataformas)"""
        platforms = []
        x_pos = 20
        initial_y = HEIGHT - 120
        y_pos = initial_y
        for i in range(102):
            y_pos -= 125
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 40, 20))
            x_pos += 80 + (i % 10) * 0

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (1 a cada 3 plataformas)
        StaticLevelGenerator.drawTurtles(game, platforms, 3)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_20(game):
        """Nível 20 - Máxima dificuldade com tartarugas (110 plataformas)"""
        platforms = []
        x_pos = 10
        initial_y = HEIGHT - 120
        y_pos = initial_y
        for i in range(111):
            y_pos -= 125
            if y_pos < StaticLevelGenerator.limit_platform_yTop:
                y_pos = initial_y
            platforms.append((x_pos, y_pos, 35, 20))
            x_pos += 75

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar tartarugas (máxima quantidade - 1 por plataforma)
        StaticLevelGenerator.drawTurtles(game, platforms, 2)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_21(game):
        """Nível 21 - Início dos morcegos e aranhas (111 plataformas) - Padrão aleatório"""
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 7 plataformas - padrão da fase 11)
        StaticLevelGenerator.drawSpiders(game, platforms, 7)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_22(game):
        """Nível 22 - Progressão com morcegos e aranhas (112 plataformas) - Padrão manual como fase 21"""
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 6 plataformas - padrão da fase 12)
        StaticLevelGenerator.drawSpiders(game, platforms, 6)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_23(game):
        """Nível 23 - Mais aranhas (113 plataformas) - Padrão manual como fase 21"""
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 5 plataformas - seguindo padrão do nível 13)
        StaticLevelGenerator.drawSpiders(game, platforms, 5)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_24(game):
        """Nível 24 - Dificuldade crescente (114 plataformas) - Padrão manual como fase 21"""
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 5 plataformas - seguindo padrão da fase 14)
        StaticLevelGenerator.drawSpiders(game, platforms, 5)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_25(game):
        """Nível 25 - Máxima dificuldade (115 plataformas) - Padrão manual como fase 21"""
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
            (15120, HEIGHT - 180, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 4 plataformas - seguindo padrão da fase 15)
        StaticLevelGenerator.drawSpiders(game, platforms, 4)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_26(game):
        """Nível 26 - Introdução dos morcegos (116 plataformas) - Padrão manual como fase 21"""
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
            (15120, HEIGHT - 180, 30, 20),
            (15240, HEIGHT - 300, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 4 plataformas - seguindo padrão da fase 16)
        StaticLevelGenerator.drawSpiders(game, platforms, 4)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_27(game):
        """Nível 27 - Mais morcegos (117 plataformas) - Padrão escadinha como nível 21"""
        # Padrão manual de plataformas seguindo o mesmo layout da fase 21 com extensões
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
            # Plataformas extras para nível 27 (6 adicionais)
            (15120, HEIGHT - 180, 30, 20),
            (15240, HEIGHT - 300, 30, 20),
            (15360, HEIGHT - 160, 30, 20),
            (15480, HEIGHT - 320, 30, 20),
            (15600, HEIGHT - 200, 30, 20),
            (15720, HEIGHT - 340, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (1 a cada 3 plataformas - seguindo padrão do nível 17)
        StaticLevelGenerator.drawSpiders(game, platforms, 3)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_28(game):
        """Nível 28 - Combinação intensa (118 plataformas) - Padrão escadinha como nível 21"""
        # Padrão manual de plataformas seguindo o mesmo layout da fase 21 com extensões
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
            # Plataformas extras para nível 28 (7 adicionais)
            (15120, HEIGHT - 180, 30, 20),
            (15240, HEIGHT - 300, 30, 20),
            (15360, HEIGHT - 160, 30, 20),
            (15480, HEIGHT - 320, 30, 20),
            (15600, HEIGHT - 200, 30, 20),
            (15720, HEIGHT - 340, 30, 20),
            (15840, HEIGHT - 180, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        StaticLevelGenerator.drawSpiders(game, platforms, 3)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_29(game):
        """Nível 29 - Quase impossível (119 plataformas) - Padrão escadinha como nível 21"""
        # Padrão manual de plataformas seguindo o mesmo layout da fase 21 com extensões
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
            # Plataformas extras para nível 29 (8 adicionais)
            (15120, HEIGHT - 180, 30, 20),
            (15240, HEIGHT - 300, 30, 20),
            (15360, HEIGHT - 160, 30, 20),
            (15480, HEIGHT - 320, 30, 20),
            (15600, HEIGHT - 200, 30, 20),
            (15720, HEIGHT - 340, 30, 20),
            (15840, HEIGHT - 180, 30, 20),
            (15960, HEIGHT - 300, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)

        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (3 por plataforma - seguindo padrão do nível 19)
        StaticLevelGenerator.drawSpiders(game, platforms, 3)

        StaticLevelGenerator.drawFlag(game, platforms)

    def create_level_30(game):
        """Nível 30 - FINAL BOSS (120 plataformas) - Padrão escadinha como nível 21"""
        # Padrão manual de plataformas seguindo o mesmo layout da fase 21 com extensões
        platforms = [
            (10, HEIGHT - 100, 30, 20),
            (120, HEIGHT - 280, 30, 20),
            (240, HEIGHT - 160, 30, 20),
            (360, HEIGHT - 320, 30, 20),
            (480, HEIGHT - 200, 30, 20),
            (600, HEIGHT - 360, 30, 20),
            (720, HEIGHT - 140, 30, 20),
            (840, HEIGHT - 300, 30, 20),
            (960, HEIGHT - 180, 30, 20),
            (1080, HEIGHT - 340, 30, 20),
            (1200, HEIGHT - 120, 30, 20),
            (1320, HEIGHT - 280, 30, 20),
            (1440, HEIGHT - 220, 30, 20),
            (1560, HEIGHT - 360, 30, 20),
            (1680, HEIGHT - 160, 30, 20),
            (1800, HEIGHT - 300, 30, 20),
            (1920, HEIGHT - 140, 30, 20),
            (2040, HEIGHT - 320, 30, 20),
            (2160, HEIGHT - 200, 30, 20),
            (2280, HEIGHT - 340, 30, 20),
            (2400, HEIGHT - 180, 30, 20),
            (2520, HEIGHT - 300, 30, 20),
            (2640, HEIGHT - 120, 30, 20),
            (2760, HEIGHT - 280, 30, 20),
            (2880, HEIGHT - 240, 30, 20),
            (3000, HEIGHT - 360, 30, 20),
            (3120, HEIGHT - 160, 30, 20),
            (3240, HEIGHT - 320, 30, 20),
            (3360, HEIGHT - 200, 30, 20),
            (3480, HEIGHT - 340, 30, 20),
            (3600, HEIGHT - 140, 30, 20),
            (3720, HEIGHT - 300, 30, 20),
            (3840, HEIGHT - 180, 30, 20),
            (3960, HEIGHT - 320, 30, 20),
            (4080, HEIGHT - 220, 30, 20),
            (4200, HEIGHT - 360, 30, 20),
            (4320, HEIGHT - 160, 30, 20),
            (4440, HEIGHT - 300, 30, 20),
            (4560, HEIGHT - 140, 30, 20),
            (4680, HEIGHT - 280, 30, 20),
            (4800, HEIGHT - 200, 30, 20),
            (4920, HEIGHT - 340, 30, 20),
            (5040, HEIGHT - 180, 30, 20),
            (5160, HEIGHT - 320, 30, 20),
            (5280, HEIGHT - 120, 30, 20),
            (5400, HEIGHT - 280, 30, 20),
            (5520, HEIGHT - 240, 30, 20),
            (5640, HEIGHT - 360, 30, 20),
            (5760, HEIGHT - 160, 30, 20),
            (5880, HEIGHT - 300, 30, 20),
            (6000, HEIGHT - 200, 30, 20),
            (6120, HEIGHT - 340, 30, 20),
            (6240, HEIGHT - 140, 30, 20),
            (6360, HEIGHT - 320, 30, 20),
            (6480, HEIGHT - 180, 30, 20),
            (6600, HEIGHT - 300, 30, 20),
            (6720, HEIGHT - 220, 30, 20),
            (6840, HEIGHT - 360, 30, 20),
            (6960, HEIGHT - 160, 30, 20),
            (7080, HEIGHT - 280, 30, 20),
            (7200, HEIGHT - 200, 30, 20),
            (7320, HEIGHT - 340, 30, 20),
            (7440, HEIGHT - 140, 30, 20),
            (7560, HEIGHT - 300, 30, 20),
            (7680, HEIGHT - 180, 30, 20),
            (7800, HEIGHT - 320, 30, 20),
            (7920, HEIGHT - 240, 30, 20),
            (8040, HEIGHT - 360, 30, 20),
            (8160, HEIGHT - 160, 30, 20),
            (8280, HEIGHT - 300, 30, 20),
            (8400, HEIGHT - 120, 30, 20),
            (8520, HEIGHT - 280, 30, 20),
            (8640, HEIGHT - 200, 30, 20),
            (8760, HEIGHT - 340, 30, 20),
            (8880, HEIGHT - 180, 30, 20),
            (9000, HEIGHT - 320, 30, 20),
            (9120, HEIGHT - 140, 30, 20),
            (9240, HEIGHT - 300, 30, 20),
            (9360, HEIGHT - 220, 30, 20),
            (9480, HEIGHT - 360, 30, 20),
            (9600, HEIGHT - 160, 30, 20),
            (9720, HEIGHT - 280, 30, 20),
            (9840, HEIGHT - 200, 30, 20),
            (9960, HEIGHT - 340, 30, 20),
            (10080, HEIGHT - 140, 30, 20),
            (10200, HEIGHT - 300, 30, 20),
            (10320, HEIGHT - 180, 30, 20),
            (10440, HEIGHT - 320, 30, 20),
            (10560, HEIGHT - 240, 30, 20),
            (10680, HEIGHT - 360, 30, 20),
            (10800, HEIGHT - 160, 30, 20),
            (10920, HEIGHT - 300, 30, 20),
            (11040, HEIGHT - 120, 30, 20),
            (11160, HEIGHT - 280, 30, 20),
            (11280, HEIGHT - 200, 30, 20),
            (11400, HEIGHT - 340, 30, 20),
            (11520, HEIGHT - 180, 30, 20),
            (11640, HEIGHT - 320, 30, 20),
            (11760, HEIGHT - 140, 30, 20),
            (11880, HEIGHT - 300, 30, 20),
            (12000, HEIGHT - 220, 30, 20),
            (12120, HEIGHT - 360, 30, 20),
            (12240, HEIGHT - 160, 30, 20),
            (12360, HEIGHT - 280, 30, 20),
            (12480, HEIGHT - 200, 30, 20),
            (12600, HEIGHT - 340, 30, 20),
            (12720, HEIGHT - 140, 30, 20),
            (12840, HEIGHT - 300, 30, 20),
            (12960, HEIGHT - 180, 30, 20),
            (13080, HEIGHT - 320, 30, 20),
            (13200, HEIGHT - 240, 30, 20),
            (13320, HEIGHT - 360, 30, 20),
            (13440, HEIGHT - 160, 30, 20),
            (13560, HEIGHT - 280, 30, 20),
            (13680, HEIGHT - 200, 30, 20),
            (13800, HEIGHT - 340, 30, 20),
            (13920, HEIGHT - 140, 30, 20),
            (14040, HEIGHT - 300, 30, 20),
            (14160, HEIGHT - 180, 30, 20),
            (14280, HEIGHT - 320, 30, 20),
            (14400, HEIGHT - 240, 30, 20),
            (14520, HEIGHT - 360, 30, 20),
            (14640, HEIGHT - 160, 30, 20),
            (14760, HEIGHT - 280, 30, 20),
            (14880, HEIGHT - 200, 30, 20),
            (15000, HEIGHT - 340, 30, 20),
            # Plataformas extras para nível 30 (9 adicionais)
            (15120, HEIGHT - 180, 30, 20),
            (15240, HEIGHT - 300, 30, 20),
            (15360, HEIGHT - 160, 30, 20),
            (15480, HEIGHT - 320, 30, 20),
            (15600, HEIGHT - 200, 30, 20),
            (15720, HEIGHT - 340, 30, 20),
            (15840, HEIGHT - 180, 30, 20),
            (15960, HEIGHT - 300, 30, 20),
            (16080, HEIGHT - 160, 30, 20),
        ]

        StaticLevelGenerator.drawPlatforms(game, platforms)
        StaticLevelGenerator.putPlayerInFirstPlatform(game)

        # Adicionar aranhas (2 por plataforma - seguindo padrão do nível 20)
        StaticLevelGenerator.drawSpiders(game, platforms, 2)

        StaticLevelGenerator.drawFlag(game, platforms)

    @staticmethod
    def putPlayerInFirstPlatform(game):
        # Posicionar jogador na primeira plataforma
        first_platform = game.platforms[0]
        game.player.x = first_platform.x + 10
        game.player.y = first_platform.y - game.player.height
        game.player.rect.x = game.player.x
        game.player.rect.y = game.player.y
        game.player.vel_y = 0
        game.player.on_ground = True

    @staticmethod
    def drawPlatforms(game, platforms, texture=None):
        if not texture:
            texture = game.platform_texture

        for x, y, w, h in platforms:
            game.platforms.append(Platform(x, y, w, h, texture))

    @staticmethod
    def drawFlag(game, platforms):
        last_platform = platforms[-1]  # Última plataforma da lista
        previous_platform = platforms[-2]  # Penúltima plataforma da lista
        x_gap = last_platform[0] - previous_platform[0]
        y_gap = last_platform[1] - previous_platform[1]

        final_x = last_platform[0] + x_gap  # x + width + 100
        final_y = last_platform[1] + y_gap  # y + gap
        if final_y > StaticLevelGenerator.limit_platform_y:
            final_y = last_platform[1] - y_gap  # y - gap
        if y_gap < 0 and final_y < StaticLevelGenerator.limit_platform_yTop:
            final_y = last_platform[1] - y_gap

        platform_width = last_platform[2]
        game.platforms.append(
            Platform(final_x, final_y, platform_width, 20, game.platform_texture)
        )
        game.flag = Flag(final_x + (platform_width / 2) - 20, final_y - 100)

    @staticmethod
    def drawSpiders(game, platforms, factor):
        for i in range(factor, len(platforms), factor):
            if i < len(platforms):
                platform = platforms[i]
                LevelEnemy.drawSpider(game, platform)

    @staticmethod
    def drawTurtles(game, platforms, factor):
        for i in range(factor, len(platforms), factor):
            if i < len(platforms):
                platform = platforms[i]
                LevelEnemy.drawTurtle(game, platform)
