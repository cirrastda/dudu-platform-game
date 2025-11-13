import random
import math
from internal.resources.platform import Platform
from internal.resources.enemies.bird import Bird
from internal.resources.enemies.bat import Bat
from internal.resources.enemies.turtle import Turtle
from internal.resources.enemies.spider import Spider
from internal.resources.flag import Flag
from internal.utils.constants import *


class DynamicLevelGenerator:
    """Gerador procedural de níveis para criar fases variadas e interessantes"""

    @staticmethod
    def get_platforms_stairway(
        initial_x, total_platforms, platform_width, x_factor, y_factor, top_limit
    ):
        """Gera padrão de escada com variações - mais desafiador"""
        platforms = []
        x_pos = initial_x
        initial_y = HEIGHT - 150
        y_pos = initial_y

        for i in range(total_platforms):
            platforms.append((x_pos, y_pos, platform_width, 20))
            x_pos += x_factor
            y_pos -= y_factor
            if (y_pos < top_limit):
                y_pos = initial_y

        return platforms

    @staticmethod
    def generate_staircase_pattern(
        start_x, start_y, num_platforms, direction=1, step_size=160, height_variation=80
    ):
        """Gera padrão de escada com variações - mais desafiador"""
        platforms = []
        x_pos = start_x
        y_pos = start_y

        for i in range(num_platforms):
            # Adicionar variação aleatória na altura (maior)
            height_offset = random.randint(
                -height_variation // 2, height_variation // 2
            )
            platforms.append(
                (x_pos, y_pos + height_offset, random.randint(80, 120), 20)
            )

            # Próxima posição - mais espaçada
            x_pos += step_size + random.randint(-40, 60)
            y_pos += direction * random.randint(40, 80)

            # Inverter direção ocasionalmente
            if random.random() < 0.3:
                direction *= -1

        return platforms

    @staticmethod
    def generate_wave_pattern(
        start_x, start_y, num_platforms, amplitude=120, frequency=0.25
    ):
        """Gera padrão ondulado - mais desafiador"""
        platforms = []
        x_pos = start_x

        for i in range(num_platforms):
            # Calcular altura baseada em função seno (amplitude maior)
            wave_y = start_y + amplitude * math.sin(i * frequency)
            platforms.append((x_pos, wave_y, random.randint(80, 120), 20))
            x_pos += random.randint(140, 200)  # Mais espaçadas

        return platforms

    @staticmethod
    def generate_zigzag_pattern(start_x, start_y, num_platforms, segment_length=4):
        """Gera padrão em zigue-zague - mais desafiador"""
        platforms = []
        x_pos = start_x
        y_pos = start_y
        going_up = True

        for i in range(num_platforms):
            platforms.append((x_pos, y_pos, random.randint(80, 120), 20))

            # Mudar direção a cada segment_length plataformas
            if i % segment_length == segment_length - 1:
                going_up = not going_up

            x_pos += random.randint(150, 220)  # Mais espaçadas
            y_pos += (-70 if going_up else 70) + random.randint(
                -25, 25
            )  # Maior variação vertical

        return platforms

    @staticmethod
    def generate_spiral_pattern(start_x, start_y, num_platforms, radius=200):
        """Gera padrão em espiral - mais desafiador"""
        platforms = []
        center_x = start_x + radius
        center_y = start_y

        for i in range(num_platforms):
            angle = (i / num_platforms) * 5 * math.pi  # Mais voltas
            current_radius = radius * (
                1 - i / (num_platforms * 1.5)
            )  # Raio diminui mais devagar

            x = center_x + current_radius * math.cos(angle)
            y = center_y + current_radius * math.sin(angle)

            platforms.append((x, y, random.randint(70, 100), 20))  # Plataformas maiores

        return platforms

    @staticmethod
    def generate_random_clusters(start_x, start_y, num_platforms, num_clusters=3):
        """Gera grupos aleatórios de plataformas - mais desafiador"""
        platforms = []
        cluster_size = num_platforms // num_clusters

        for cluster in range(num_clusters):
            # Centro do cluster - mais espaçados
            cluster_x = start_x + cluster * 450 + random.randint(-80, 80)
            cluster_y = start_y + random.randint(-150, 150)

            # Gerar plataformas no cluster - mais espalhadas
            for i in range(cluster_size):
                offset_x = random.randint(-120, 120)
                offset_y = random.randint(-100, 100)
                platforms.append(
                    (
                        cluster_x + offset_x,
                        cluster_y + offset_y,
                        random.randint(80, 120),
                        20,
                    )
                )

        # Adicionar plataformas restantes - mais espaçadas
        remaining = num_platforms - len(platforms)
        for i in range(remaining):
            x = start_x + len(platforms) * 180 + random.randint(-50, 50)
            y = start_y + random.randint(-80, 80)
            platforms.append((x, y, random.randint(80, 120), 20))

        return platforms

    @staticmethod
    def generate_maze_pattern(start_x, start_y, num_platforms):
        """Gera um padrão de labirinto com caminhos alternativos"""
        platforms = []
        current_x = start_x
        current_y = start_y

        # Criar caminho principal
        main_path_length = num_platforms // 2
        for i in range(main_path_length):
            platforms.append((current_x, current_y, 80, 20))

            # Decidir direção: para frente ou para cima/baixo
            if random.random() < 0.7:  # 70% chance de ir para frente
                current_x += random.randint(100, 150)
            else:  # 30% chance de mudar altura
                current_y += random.randint(-60, 60)
                current_y = max(100, min(current_y, HEIGHT - 100))
                current_x += random.randint(80, 120)

        # Criar caminhos alternativos (becos sem saída e atalhos)
        for i in range(num_platforms - main_path_length):
            # Escolher uma plataforma existente como ponto de partida
            if platforms:
                base_platform = random.choice(platforms)
                branch_x = base_platform[0] + random.randint(-50, 50)
                branch_y = base_platform[1] + random.randint(-100, 100)
                branch_y = max(50, min(branch_y, HEIGHT - 50))

                platforms.append((branch_x, branch_y, random.randint(60, 100), 20))

        return platforms

    @staticmethod
    def generate_bridge_pattern(start_x, start_y, num_platforms):
        """Gera um padrão de pontes com lacunas desafiadoras"""
        platforms = []
        current_x = start_x
        current_y = start_y

        # Criar seções de ponte com lacunas
        bridge_sections = 4
        platforms_per_section = num_platforms // bridge_sections

        for section in range(bridge_sections):
            # Altura da seção atual
            section_y = start_y + math.sin(section * 0.8) * 80
            section_y = max(100, min(section_y, HEIGHT - 100))

            # Criar plataformas da ponte
            for i in range(platforms_per_section):
                platforms.append((current_x, section_y, 60, 20))
                current_x += random.randint(70, 90)  # Lacunas menores dentro da seção

            # Grande lacuna entre seções
            current_x += random.randint(150, 200)

        return platforms

    @staticmethod
    def generate_tower_pattern(start_x, start_y, num_platforms):
        """Gera um padrão de torres verticais com plataformas de conexão"""
        platforms = []

        # Criar múltiplas torres
        num_towers = 3
        platforms_per_tower = num_platforms // (
            num_towers + 1
        )  # +1 para plataformas de conexão

        for tower in range(num_towers):
            tower_x = start_x + tower * 300
            tower_base_y = start_y

            # Construir torre verticalmente
            for level in range(platforms_per_tower):
                platform_y = tower_base_y - level * 80
                platform_y = max(50, platform_y)

                # Alternar lados da torre para criar desafio
                offset_x = 40 if level % 2 == 0 else -40
                platforms.append((tower_x + offset_x, platform_y, 80, 20))

            # Adicionar plataformas de conexão entre torres
            if tower < num_towers - 1:
                connection_x = tower_x + 150
                connection_y = start_y - random.randint(40, 120)
                connection_y = max(100, connection_y)
                platforms.append((connection_x, connection_y, 100, 20))

        return platforms

    @staticmethod
    def generate_level_platforms(level, base_num_platforms=30):
        """Gera plataformas para um nível específico usando diferentes padrões"""
        # Aumentar número de plataformas com o nível
        num_platforms = base_num_platforms + (level - 6) * 3
        start_x = 60
        start_y = HEIGHT - 200

        # Escolher padrão baseado no nível (agora com 8 padrões diferentes)
        pattern_choice = (level - 6) % 8

        if pattern_choice == 0:
            return DynamicLevelGenerator.generate_staircase_pattern(
                start_x, start_y, num_platforms
            )
        elif pattern_choice == 1:
            return DynamicLevelGenerator.generate_wave_pattern(start_x, start_y, num_platforms)
        elif pattern_choice == 2:
            return DynamicLevelGenerator.generate_zigzag_pattern(
                start_x, start_y, num_platforms
            )
        elif pattern_choice == 3:
            return DynamicLevelGenerator.generate_spiral_pattern(
                start_x, start_y, num_platforms
            )
        elif pattern_choice == 4:
            return DynamicLevelGenerator.generate_random_clusters(
                start_x, start_y, num_platforms
            )
        elif pattern_choice == 5:
            return DynamicLevelGenerator.generate_maze_pattern(start_x, start_y, num_platforms)
        elif pattern_choice == 6:
            return DynamicLevelGenerator.generate_bridge_pattern(
                start_x, start_y, num_platforms
            )
        else:
            return DynamicLevelGenerator.generate_tower_pattern(
                start_x, start_y, num_platforms
            )

    def create_advanced_level(self, level):
        """Cria níveis avançados (11+) com base no padrão das fases anteriores"""
        # Calcular parâmetros baseados no nível
        num_platforms = min(70 + (level - 11) * 2, 100)  # Máximo 100 plataformas
        platform_width = max(40, 50 - (level - 11))  # Plataformas menores
        max_gap = min(120 + (level - 11) * 5, 200)  # Gaps maiores

        platforms = []
        x_pos = 30

        for i in range(num_platforms):
            # Variação de altura mais extrema
            y_variation = 60 + (level - 11) * 10
            y_pos = HEIGHT - (
                80
                + (i % 12) * y_variation // 3
                + random.randint(-y_variation // 2, y_variation // 2)
            )

            # Garantir que não fique muito alto ou baixo
            y_pos = max(60, min(y_pos, HEIGHT - 40))

            platforms.append((x_pos, y_pos, platform_width, 20))

            # Próxima posição com gap variável
            gap = 80 + random.randint(0, max_gap - 80)
            x_pos += gap

        for x, y, w, h in platforms:
            self.platforms.append(Platform(x, y, w, h, self.platform_texture))

        # Posicionar jogador na primeira plataforma
        if platforms:
            first_platform = platforms[0]
            self.player.x = first_platform[0] + 10
            self.player.y = first_platform[1] - self.player.height
            self.player.rect.x = self.player.x
            self.player.rect.y = self.player.y
            self.player.vel_y = 0
            self.player.on_ground = True

            # Adicionar plataforma final e bandeira
            last_platform = platforms[-1]
            final_x = last_platform[0] + 200
            final_y = HEIGHT - 200
            self.platforms.append(
                Platform(final_x, final_y, platform_width, 20, self.platform_texture)
            )
            self.flag = Flag(final_x + 20, final_y - 100)

    def create_procedural_level(self, level):
        """Cria níveis com layouts manuais específicos"""
        # Usar layouts manuais específicos para cada fase
        self.create_advanced_level(level)

        # Adicionar tartarugas apenas a partir da fase 11
        if level >= 11:
            # Usar as plataformas já criadas em self.platforms
            platform_count = (
                len(self.platforms) - 1
            )  # -1 para não incluir a plataforma da bandeira
            turtle_frequency = max(
                3, 20 - level
            )  # De 1 a cada 9 plataformas até 1 a cada 3
            for i in range(turtle_frequency, platform_count, turtle_frequency):
                if i < platform_count:
                    platform = self.platforms[i]
                    turtle = Turtle(
                        platform.x,
                        platform.y - 30,
                        platform.x,
                        platform.x + platform.width,
                        self.turtle_images,
                    )
                    self.turtles.append(turtle)
