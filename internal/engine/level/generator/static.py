import pygame
from internal.utils.constants import *
from internal.resources.platform import Platform
from internal.resources.flag import Flag
from internal.resources.cache import ResourceCache


class StaticLevelGenerator:
    def create_level_1(self):
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
        last_platform = platforms[-1]  # Última plataforma da lista
        final_x = last_platform[0] + last_platform[2] + 100  # x + width + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 120, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 50, HEIGHT - 300)

    def create_level_2(self):
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
        self.platforms.append(
            Platform(4940, HEIGHT - 200, 100, 20, self.platform_texture)
        )
        self.flag = Flag(4960, HEIGHT - 300)

    def create_level_3(self):
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
        self.platforms.append(
            Platform(5740, HEIGHT - 240, 80, 20, self.platform_texture)
        )
        self.flag = Flag(5760, HEIGHT - 340)

    def create_level_4(self):
        """Nível 4 - Difícil (50 plataformas) - Versão corrigida sem plataformas extras"""
        # Limpar plataformas existentes para garantir que não há duplicatas
        self.platforms.clear()

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

        # Adicionar APENAS a plataforma da bandeira (não há outras plataformas após esta)
        self.platforms.append(
            Platform(5540, HEIGHT - 200, 80, 20, self.platform_texture)
        )
        self.flag = Flag(5560, HEIGHT - 300)

        # Debug: Imprimir número total de plataformas para verificação
        print(
            f"Nível 4 criado com {len(self.platforms)} plataformas (47 + 1 da bandeira = 48 total)"
        )

    def create_level_8(self):
        """Nível 8 - Progressão (55 plataformas)"""
        platforms = []
        x_pos = 90
        for i in range(55):
            y_pos = HEIGHT - (85 + (i % 11) * 48 + (i // 11) * 38)
            platforms.append((x_pos, y_pos, 38, 20))
            x_pos += 105

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
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 42, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_9(self):
        """Nível 9 - Insano (60 plataformas) - Layout manual"""
        platforms = [
            (40, HEIGHT - 280, 50, 20),
            (130, HEIGHT - 380, 50, 20),
            (220, HEIGHT - 120, 50, 20),
            (310, HEIGHT - 420, 50, 20),
            (400, HEIGHT - 180, 50, 20),
            (490, HEIGHT - 80, 50, 20),
            (580, HEIGHT - 360, 50, 20),
            (670, HEIGHT - 140, 50, 20),
            (760, HEIGHT - 440, 50, 20),
            (850, HEIGHT - 100, 50, 20),
            (940, HEIGHT - 340, 50, 20),
            (1030, HEIGHT - 160, 50, 20),
            (1120, HEIGHT - 400, 50, 20),
            (1210, HEIGHT - 80, 50, 20),
            (1300, HEIGHT - 320, 50, 20),
            (1390, HEIGHT - 140, 50, 20),
            (1480, HEIGHT - 380, 50, 20),
            (1570, HEIGHT - 120, 50, 20),
            (1660, HEIGHT - 360, 50, 20),
            (1750, HEIGHT - 200, 50, 20),
            (1840, HEIGHT - 100, 50, 20),
            (1930, HEIGHT - 420, 50, 20),
            (2020, HEIGHT - 160, 50, 20),
            (2110, HEIGHT - 340, 50, 20),
            (2200, HEIGHT - 80, 50, 20),
            (2290, HEIGHT - 400, 50, 20),
            (2380, HEIGHT - 140, 50, 20),
            (2470, HEIGHT - 380, 50, 20),
            (2560, HEIGHT - 180, 50, 20),
            (2650, HEIGHT - 100, 50, 20),
            (2740, HEIGHT - 360, 50, 20),
            (2830, HEIGHT - 220, 50, 20),
            (2920, HEIGHT - 120, 50, 20),
            (3010, HEIGHT - 420, 50, 20),
            (3100, HEIGHT - 160, 50, 20),
            (3190, HEIGHT - 340, 50, 20),
            (3280, HEIGHT - 80, 50, 20),
            (3370, HEIGHT - 400, 50, 20),
            (3460, HEIGHT - 140, 50, 20),
            (3550, HEIGHT - 380, 50, 20),
            (3640, HEIGHT - 180, 50, 20),
            (3730, HEIGHT - 100, 50, 20),
            (3820, HEIGHT - 360, 50, 20),
            (3910, HEIGHT - 220, 50, 20),
            (4000, HEIGHT - 120, 50, 20),
            (4090, HEIGHT - 420, 50, 20),
            (4180, HEIGHT - 160, 50, 20),
            (4270, HEIGHT - 340, 50, 20),
            (4360, HEIGHT - 140, 50, 20),
            (4450, HEIGHT - 400, 50, 20),
            (4540, HEIGHT - 180, 50, 20),
            (4630, HEIGHT - 320, 50, 20),
            (4720, HEIGHT - 140, 50, 20),
            (4810, HEIGHT - 380, 50, 20),
            (4900, HEIGHT - 180, 50, 20),
            (4990, HEIGHT - 300, 50, 20),
            (5080, HEIGHT - 120, 50, 20),
            (5170, HEIGHT - 380, 50, 20),
            (5260, HEIGHT - 200, 50, 20),
            (5350, HEIGHT - 340, 50, 20),
            (5440, HEIGHT - 160, 50, 20),
            (5530, HEIGHT - 280, 50, 20),
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
        self.platforms.append(
            Platform(5710, HEIGHT - 200, 50, 20, self.platform_texture)
        )
        self.flag = Flag(5730, HEIGHT - 300)

    def create_level_10(self):
        """Nível 10 - Impossível (65 plataformas) - Layout manual"""
        platforms = [
            (30, HEIGHT - 300, 45, 20),
            (115, HEIGHT - 400, 45, 20),
            (200, HEIGHT - 100, 45, 20),
            (285, HEIGHT - 440, 45, 20),
            (370, HEIGHT - 160, 45, 20),
            (455, HEIGHT - 60, 45, 20),
            (540, HEIGHT - 380, 45, 20),
            (625, HEIGHT - 120, 45, 20),
            (710, HEIGHT - 460, 45, 20),
            (795, HEIGHT - 80, 45, 20),
            (880, HEIGHT - 360, 45, 20),
            (965, HEIGHT - 140, 45, 20),
            (1050, HEIGHT - 420, 45, 20),
            (1135, HEIGHT - 60, 45, 20),
            (1220, HEIGHT - 340, 45, 20),
            (1305, HEIGHT - 120, 45, 20),
            (1390, HEIGHT - 400, 45, 20),
            (1475, HEIGHT - 100, 45, 20),
            (1560, HEIGHT - 380, 45, 20),
            (1645, HEIGHT - 180, 45, 20),
            (1730, HEIGHT - 80, 45, 20),
            (1815, HEIGHT - 440, 45, 20),
            (1900, HEIGHT - 140, 45, 20),
            (1985, HEIGHT - 360, 45, 20),
            (2070, HEIGHT - 60, 45, 20),
            (2155, HEIGHT - 420, 45, 20),
            (2240, HEIGHT - 120, 45, 20),
            (2325, HEIGHT - 400, 45, 20),
            (2410, HEIGHT - 160, 45, 20),
            (2495, HEIGHT - 80, 45, 20),
            (2580, HEIGHT - 380, 45, 20),
            (2665, HEIGHT - 200, 45, 20),
            (2750, HEIGHT - 100, 45, 20),
            (2835, HEIGHT - 440, 45, 20),
            (2920, HEIGHT - 140, 45, 20),
            (3005, HEIGHT - 360, 45, 20),
            (3090, HEIGHT - 60, 45, 20),
            (3175, HEIGHT - 420, 45, 20),
            (3260, HEIGHT - 120, 45, 20),
            (3345, HEIGHT - 400, 45, 20),
            (3430, HEIGHT - 160, 45, 20),
            (3515, HEIGHT - 80, 45, 20),
            (3600, HEIGHT - 380, 45, 20),
            (3685, HEIGHT - 200, 45, 20),
            (3770, HEIGHT - 100, 45, 20),
            (3855, HEIGHT - 440, 45, 20),
            (3940, HEIGHT - 140, 45, 20),
            (4025, HEIGHT - 360, 45, 20),
            (4110, HEIGHT - 120, 45, 20),
            (4195, HEIGHT - 420, 45, 20),
            (4280, HEIGHT - 160, 45, 20),
            (4365, HEIGHT - 340, 45, 20),
            (4450, HEIGHT - 120, 45, 20),
            (4535, HEIGHT - 400, 45, 20),
            (4620, HEIGHT - 160, 45, 20),
            (4705, HEIGHT - 320, 45, 20),
            (4790, HEIGHT - 120, 45, 20),
            (4875, HEIGHT - 400, 45, 20),
            (4960, HEIGHT - 160, 45, 20),
            (5045, HEIGHT - 320, 45, 20),
            (5130, HEIGHT - 100, 45, 20),
            (5215, HEIGHT - 400, 45, 20),
            (5300, HEIGHT - 180, 45, 20),
            (5385, HEIGHT - 360, 45, 20),
            (5470, HEIGHT - 140, 45, 20),
            (5555, HEIGHT - 300, 45, 20),
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
        self.platforms.append(
            Platform(5735, HEIGHT - 200, 45, 20, self.platform_texture)
        )
        self.flag = Flag(5755, HEIGHT - 300)

    def create_level_11(self):
        """Nível 11 - Progressão (70 plataformas)"""
        platforms = []
        x_pos = 70
        for i in range(70):
            y_pos = HEIGHT - (100 + (i % 14) * 35 + (i // 14) * 50)
            platforms.append((x_pos, y_pos, 40, 20))
            x_pos += 110

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 40, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_12(self):
        """Nível 12 - Progressão (75 plataformas)"""
        platforms = []
        x_pos = 60
        for i in range(75):
            y_pos = HEIGHT - (110 + (i % 15) * 32 + (i // 15) * 55)
            platforms.append((x_pos, y_pos, 38, 20))
            x_pos += 105

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 38, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_13(self):
        """Nível 13 - Progressão (80 plataformas)"""
        platforms = []
        x_pos = 50
        for i in range(80):
            y_pos = HEIGHT - (115 + (i % 16) * 30 + (i // 16) * 60)
            platforms.append((x_pos, y_pos, 36, 20))
            x_pos += 100

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 36, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_14(self):
        """Nível 14 - Progressão (85 plataformas)"""
        platforms = []
        x_pos = 40
        for i in range(85):
            y_pos = HEIGHT - (120 + (i % 17) * 28 + (i // 17) * 65)
            platforms.append((x_pos, y_pos, 34, 20))
            x_pos += 95

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 34, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_15(self):
        """Nível 15 - Progressão (90 plataformas)"""
        platforms = []
        x_pos = 30
        for i in range(90):
            y_pos = HEIGHT - (125 + (i % 18) * 26 + (i // 18) * 70)
            platforms.append((x_pos, y_pos, 32, 20))
            x_pos += 90

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 32, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_16(self):
        """Nível 16 - Progressão (95 plataformas)"""
        platforms = []
        x_pos = 20
        for i in range(95):
            y_pos = HEIGHT - (130 + (i % 19) * 24 + (i // 19) * 75)
            platforms.append((x_pos, y_pos, 30, 20))
            x_pos += 85

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_17(self):
        """Nível 17 - Progressão (100 plataformas)"""
        platforms = []
        x_pos = 10
        for i in range(100):
            y_pos = HEIGHT - (135 + (i % 20) * 22 + (i // 20) * 80)
            platforms.append((x_pos, y_pos, 28, 20))
            x_pos += 80

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
        for i in range(1, len(platforms), 2):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 28, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_18(self):
        """Nível 18 - Progressão (105 plataformas)"""
        platforms = []
        x_pos = 5
        for i in range(105):
            y_pos = HEIGHT - (140 + (i % 21) * 20 + (i // 21) * 85)
            platforms.append((x_pos, y_pos, 26, 20))
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

        # Adicionar tartarugas (1 a cada 2 plataformas)
        for i in range(1, len(platforms), 2):
            if i < len(platforms):
                platform = platforms[i]
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 26, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_19(self):
        """Nível 19 - Progressão (110 plataformas)"""
        platforms = []
        x_pos = 0
        for i in range(110):
            y_pos = HEIGHT - (145 + (i % 22) * 18 + (i // 22) * 90)
            platforms.append((x_pos, y_pos, 24, 20))
            x_pos += 70

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

        # Adicionar tartarugas (1 a cada plataforma)
        for i in range(len(platforms)):
            platform = platforms[i]
            turtle = Turtle(
                platform[0],
                platform[1] - 30,
                platform[0],
                platform[0] + platform[2],
                self.turtle_images,
            )
            self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 24, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_20(self):
        """Nível 20 - Progressão Final (120 plataformas)"""
        platforms = []
        x_pos = 0
        for i in range(120):
            y_pos = HEIGHT - (150 + (i % 24) * 16 + (i // 24) * 95)
            platforms.append((x_pos, y_pos, 22, 20))
            x_pos += 65

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

        # Adicionar tartarugas (1 a cada plataforma)
        for i in range(len(platforms)):
            platform = platforms[i]
            turtle = Turtle(
                platform[0],
                platform[1] - 30,
                platform[0],
                platform[0] + platform[2],
                self.turtle_images,
            )
            self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 22, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_5(self):
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
        self.platforms.append(
            Platform(6840, HEIGHT - 240, 60, 20, self.platform_texture)
        )
        self.flag = Flag(6860, HEIGHT - 340)

    def create_level_6(self):
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
        self.platforms.append(
            Platform(8060, HEIGHT - 200, 60, 20, self.platform_texture)
        )
        self.flag = Flag(8080, HEIGHT - 300)

    def create_level_7(self):
        """Nível 7 - Progressão (28 plataformas) - Gaps moderados com saltos factíveis"""
        platforms = [
            (140, HEIGHT - 220, 90, 20),
            (300, HEIGHT - 300, 90, 20),
            (470, HEIGHT - 160, 90, 20),
            (640, HEIGHT - 280, 90, 20),
            (810, HEIGHT - 200, 90, 20),
            (980, HEIGHT - 340, 90, 20),
            (1150, HEIGHT - 140, 90, 20),
            (1320, HEIGHT - 260, 90, 20),
            (1490, HEIGHT - 320, 90, 20),
            (1660, HEIGHT - 180, 90, 20),
            (1830, HEIGHT - 240, 90, 20),
            (2000, HEIGHT - 300, 90, 20),
            (2170, HEIGHT - 160, 90, 20),
            (2340, HEIGHT - 280, 90, 20),
            (2510, HEIGHT - 220, 90, 20),
            (2680, HEIGHT - 340, 90, 20),
            (2850, HEIGHT - 180, 90, 20),
            (3020, HEIGHT - 260, 90, 20),
            (3190, HEIGHT - 300, 90, 20),
            (3360, HEIGHT - 140, 90, 20),
            (3530, HEIGHT - 240, 90, 20),
            (3700, HEIGHT - 320, 90, 20),
            (3870, HEIGHT - 200, 90, 20),
            (4040, HEIGHT - 280, 90, 20),
            (4210, HEIGHT - 160, 90, 20),
            (4380, HEIGHT - 300, 90, 20),
            (4550, HEIGHT - 220, 90, 20),
            (4720, HEIGHT - 260, 90, 20),
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
        # Calcular posição final baseada na última plataforma
        last_platform = platforms[-1]
        final_x = last_platform[0] + 200  # 200 pixels após a última plataforma
        self.platforms.append(
            Platform(final_x, HEIGHT - 180, 90, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 280)

    def create_level_8(self):
        """Nível 8 - Progressão (30 plataformas) - Gaps maiores mas ainda factíveis"""
        platforms = [
            (160, HEIGHT - 240, 85, 20),
            (340, HEIGHT - 320, 85, 20),
            (530, HEIGHT - 160, 85, 20),
            (720, HEIGHT - 280, 85, 20),
            (910, HEIGHT - 200, 85, 20),
            (1100, HEIGHT - 340, 85, 20),
            (1290, HEIGHT - 140, 85, 20),
            (1480, HEIGHT - 260, 85, 20),
            (1670, HEIGHT - 320, 85, 20),
            (1860, HEIGHT - 180, 85, 20),
            (2050, HEIGHT - 300, 85, 20),
            (2240, HEIGHT - 220, 85, 20),
            (2430, HEIGHT - 340, 85, 20),
            (2620, HEIGHT - 160, 85, 20),
            (2810, HEIGHT - 280, 85, 20),
            (3000, HEIGHT - 240, 85, 20),
            (3190, HEIGHT - 320, 85, 20),
            (3380, HEIGHT - 180, 85, 20),
            (3570, HEIGHT - 300, 85, 20),
            (3760, HEIGHT - 140, 85, 20),
            (3950, HEIGHT - 260, 85, 20),
            (4140, HEIGHT - 320, 85, 20),
            (4330, HEIGHT - 200, 85, 20),
            (4520, HEIGHT - 280, 85, 20),
            (4710, HEIGHT - 160, 85, 20),
            (4900, HEIGHT - 300, 85, 20),
            (5090, HEIGHT - 240, 85, 20),
            (5280, HEIGHT - 320, 85, 20),
            (5470, HEIGHT - 180, 85, 20),
            (5660, HEIGHT - 260, 85, 20),
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
        final_x = 5850
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 85, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_9(self):
        """Nível 9 - Progressão (32 plataformas) - Gaps desafiadores mas possíveis"""
        platforms = [
            (180, HEIGHT - 260, 80, 20),
            (380, HEIGHT - 340, 80, 20),
            (580, HEIGHT - 160, 80, 20),
            (780, HEIGHT - 300, 80, 20),
            (980, HEIGHT - 200, 80, 20),
            (1180, HEIGHT - 340, 80, 20),
            (1380, HEIGHT - 140, 80, 20),
            (1580, HEIGHT - 280, 80, 20),
            (1780, HEIGHT - 320, 80, 20),
            (1980, HEIGHT - 180, 80, 20),
            (2180, HEIGHT - 300, 80, 20),
            (2380, HEIGHT - 240, 80, 20),
            (2580, HEIGHT - 340, 80, 20),
            (2780, HEIGHT - 160, 80, 20),
            (2980, HEIGHT - 280, 80, 20),
            (3180, HEIGHT - 260, 80, 20),
            (3380, HEIGHT - 320, 80, 20),
            (3580, HEIGHT - 180, 80, 20),
            (3780, HEIGHT - 300, 80, 20),
            (3980, HEIGHT - 140, 80, 20),
            (4180, HEIGHT - 280, 80, 20),
            (4380, HEIGHT - 320, 80, 20),
            (4580, HEIGHT - 200, 80, 20),
            (4780, HEIGHT - 300, 80, 20),
            (4980, HEIGHT - 160, 80, 20),
            (5180, HEIGHT - 320, 80, 20),
            (5380, HEIGHT - 240, 80, 20),
            (5580, HEIGHT - 300, 80, 20),
            (5780, HEIGHT - 180, 80, 20),
            (5980, HEIGHT - 280, 80, 20),
            (6180, HEIGHT - 260, 80, 20),
            (6380, HEIGHT - 320, 80, 20),
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
        final_x = 6570
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 80, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

    def create_level_10(self):
        """Nível 10 - Progressão (34 plataformas) - Máxima dificuldade com saltos no limite"""
        platforms = [
            (200, HEIGHT - 280, 75, 20),
            (410, HEIGHT - 360, 75, 20),
            (620, HEIGHT - 160, 75, 20),
            (830, HEIGHT - 320, 75, 20),
            (1040, HEIGHT - 200, 75, 20),
            (1250, HEIGHT - 340, 75, 20),
            (1460, HEIGHT - 140, 75, 20),
            (1670, HEIGHT - 300, 75, 20),
            (1880, HEIGHT - 260, 75, 20),
            (2090, HEIGHT - 340, 75, 20),
            (2300, HEIGHT - 180, 75, 20),
            (2510, HEIGHT - 320, 75, 20),
            (2720, HEIGHT - 240, 75, 20),
            (2930, HEIGHT - 360, 75, 20),
            (3140, HEIGHT - 160, 75, 20),
            (3350, HEIGHT - 300, 75, 20),
            (3560, HEIGHT - 280, 75, 20),
            (3770, HEIGHT - 340, 75, 20),
            (3980, HEIGHT - 180, 75, 20),
            (4190, HEIGHT - 320, 75, 20),
            (4400, HEIGHT - 140, 75, 20),
            (4610, HEIGHT - 300, 75, 20),
            (4820, HEIGHT - 260, 75, 20),
            (5030, HEIGHT - 340, 75, 20),
            (5240, HEIGHT - 200, 75, 20),
            (5450, HEIGHT - 320, 75, 20),
            (5660, HEIGHT - 160, 75, 20),
            (5870, HEIGHT - 300, 75, 20),
            (6080, HEIGHT - 240, 75, 20),
            (6290, HEIGHT - 340, 75, 20),
            (6500, HEIGHT - 180, 75, 20),
            (6710, HEIGHT - 300, 75, 20),
            (6920, HEIGHT - 260, 75, 20),
            (7130, HEIGHT - 320, 75, 20),
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
        final_x = 7320
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 75, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 300)

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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 200, 80, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 190, 75, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 180, 70, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 170, 65, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 160, 60, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 150, 55, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 140, 50, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 130, 45, 20, self.platform_texture)
        )
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
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    self.turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 120, 40, 20, self.platform_texture)
        )
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
        turtle_images = self.turtle_images if hasattr(self, "turtle_images") else None

        for i, platform in enumerate(platforms):
            if i % 1 == 0:  # Uma tartaruga por plataforma
                turtle = Turtle(
                    platform[0],
                    platform[1] - 30,
                    platform[0],
                    platform[0] + platform[2],
                    turtle_images,
                )
                self.turtles.append(turtle)

        # Adicionar plataforma embaixo da bandeira
        final_x = x_pos + 100
        self.platforms.append(
            Platform(final_x, HEIGHT - 110, 35, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 210)

    def create_level_21(self):
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

        # Adicionar aranhas (1 a cada 4 plataformas - padrão da fase 11)
        for i in range(4, len(platforms), 4):
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 100
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Adicionar plataforma embaixo da bandeira
        final_x = 13560
        self.platforms.append(
            Platform(final_x, HEIGHT - 100, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 200)

    def create_level_22(self):
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

        # Adicionar aranhas (1 a cada 3 plataformas - padrão da fase 12)
        for i in range(3, len(platforms), 3):
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 100
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Adicionar plataforma embaixo da bandeira
        final_x = 14760
        self.platforms.append(
            Platform(final_x, HEIGHT - 100, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 200)

    def create_level_23(self):
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

        # Adicionar aranhas (1 a cada 4 plataformas - seguindo padrão do nível 13)
        for i in range(4, len(platforms), 4):  # Começar do índice 4 (5ª plataforma)
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 100
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Adicionar plataforma embaixo da bandeira
        final_x = 15000
        self.platforms.append(
            Platform(final_x, HEIGHT - 100, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 200)

    def create_level_24(self):
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

        # Adicionar aranhas (1 a cada 2 plataformas - seguindo padrão da fase 14)
        for i in range(2, len(platforms), 2):  # Começar do índice 2 (3ª plataforma)
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 100
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Adicionar plataforma embaixo da bandeira
        final_x = 15120
        self.platforms.append(
            Platform(final_x, HEIGHT - 100, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 200)

    def create_level_25(self):
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

        # Adicionar aranhas (1 a cada 2 plataformas - seguindo padrão da fase 15)
        for i in range(2, len(platforms), 2):  # Começar do índice 2 (3ª plataforma)
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 100
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Adicionar plataforma embaixo da bandeira
        final_x = 15240
        self.platforms.append(
            Platform(final_x, HEIGHT - 100, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 200)

    def create_level_26(self):
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

        # Adicionar aranhas (1 a cada 3 plataformas - seguindo padrão da fase 16)
        for i in range(3, len(platforms), 3):
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 100
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Nível 26 corresponde ao nível 16 - morcegos são gerados dinamicamente pelo sistema

        # Adicionar plataforma embaixo da bandeira
        final_x = 15360
        self.platforms.append(
            Platform(final_x, HEIGHT - 100, 30, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 200)

    def create_level_27(self):
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

        # Adicionar aranhas (1 a cada 2 plataformas - seguindo padrão do nível 17)
        for i in range(2, len(platforms), 2):  # Começar do índice 2 (3ª plataforma)
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 70
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Nível 27 corresponde ao nível 17 - morcegos são gerados dinamicamente pelo sistema
        # Não adicionar morcegos estáticos aqui

        # Adicionar plataforma embaixo da bandeira
        final_x = 15840
        self.platforms.append(
            Platform(final_x, HEIGHT - 70, 18, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 170)

    def create_level_28(self):
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

        # Adicionar aranhas (1 a cada 2 plataformas - seguindo padrão do nível 18)
        for i in range(2, len(platforms), 2):  # Começar do índice 2 (3ª plataforma)
            if i < len(platforms):
                platform = platforms[i]
                top_limit = platform[1] - 65
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Nível 28 corresponde ao nível 18 - morcegos são gerados dinamicamente pelo sistema
        # Não adicionar morcegos estáticos aqui

        # Adicionar plataforma embaixo da bandeira
        final_x = 15960
        self.platforms.append(
            Platform(final_x, HEIGHT - 65, 16, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 165)

    def create_level_29(self):
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

        # Adicionar aranhas (1 por plataforma - seguindo padrão do nível 19)
        for i, platform in enumerate(platforms):
            if i % 1 == 0:
                top_limit = platform[1] - 60
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Nível 29 corresponde ao nível 19 - morcegos são gerados dinamicamente pelo sistema
        # Não adicionar morcegos estáticos aqui

        # Adicionar plataforma embaixo da bandeira
        final_x = 16080
        self.platforms.append(
            Platform(final_x, HEIGHT - 60, 14, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 160)

    def create_level_30(self):
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

        # Adicionar aranhas (1 por plataforma - seguindo padrão do nível 20)
        for i, platform in enumerate(platforms):
            if i % 1 == 0:
                top_limit = platform[1] - 55
                bottom_limit = platform[1] - 30
                spider = Spider(
                    platform[0] + platform[2] // 2,
                    top_limit,
                    top_limit,
                    bottom_limit,
                    self.spider_images,
                )
                self.spiders.append(spider)

        # Nível 30 corresponde ao nível 20 - morcegos são gerados dinamicamente pelo sistema
        # Não adicionar morcegos estáticos aqui

        # Adicionar plataforma embaixo da bandeira
        final_x = 16200
        self.platforms.append(
            Platform(final_x, HEIGHT - 55, 12, 20, self.platform_texture)
        )
        self.flag = Flag(final_x + 20, HEIGHT - 155)
