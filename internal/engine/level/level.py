import pygame
from internal.utils.constants import *
from internal.resources.platform import Platform
from internal.resources.flag import Flag
from internal.resources.cache import ResourceCache
from internal.engine.level.generator.static import StaticLevelGenerator
from internal.resources.player import Player
from internal.resources.enemies.turtle import Turtle
from internal.resources.extra_life import ExtraLife
from internal.resources.powerup import PowerUp, PowerUpSpec


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
            if (
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
        # Fases 1 a 6
        if 1 <= level <= 6:
            return "imagens/bg/fase 1.png"
        # Fases 7 a 10
        elif 7 <= level <= 10:
            return "imagens/bg/fase 1.5.png"
        # Fases 11 a 16
        elif 11 <= level <= 16:
            return "imagens/bg/fase 2.png"
        # Fases 17 a 20
        elif 17 <= level <= 20:
            return "imagens/bg/fase 2.5.png"
        # Fases 21 a 26
        elif 21 <= level <= 26:
            return "imagens/bg/fase 3.png"
        # Fases 27 a 30
        elif 27 <= level <= 30:
            return "imagens/bg/fase 3.5.png"
        # Fases 31 a 36
        elif 31 <= level <= 36:
            return "imagens/bg/fase 4.png"
        # Fases 37 a 40
        elif 37 <= level <= 40:
            return "imagens/bg/fase 4.5.png"
        # Fases 41 a 46
        elif 41 <= level <= 46:
            return "imagens/bg/fase 5.png"
        # Fases 47 a 50
        elif 47 <= level <= 50:
            return "imagens/bg/fase 5.5.png"
        # Fase 51
        elif level == 51:
            return "imagens/bg/fase 6.png"
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
        elif level == 51:
            StaticLevelGenerator.create_level_51(self)

    def init_level(game):
        """Inicializar o nível atual"""
        game.player = Player(50, HEIGHT - 200)
        game.platforms = []
        game.flag = None
        game.spaceship = None
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
            cache = ResourceCache()
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

        # Resetar e posicionar item de vida extra
        game.extra_lives = []
        # Não reposicionar vida extra se já foi coletada neste nível
        if not hasattr(game, "collected_extra_life_levels") or (
            game.current_level not in game.collected_extra_life_levels
        ):
            Level.place_extra_life(game)

        # Resetar e posicionar power-ups conforme dificuldade
        game.powerups = []
        Level.place_powerups(game)

    def place_extra_life(game):
        """Posiciona um item de vida em uma plataforma, exigindo um salto para alcançar"""
        if not hasattr(game, "platforms") or not game.platforms:
            return

        # Ordenar plataformas por posição X
        platforms_sorted = sorted(game.platforms, key=lambda p: p.x)

        # Calcular o meio da fase em X
        min_x = platforms_sorted[0].x
        max_x = max(p.x + p.width for p in platforms_sorted)
        mid_x = (min_x + max_x) / 2

        # Escolher o vão cujo centro esteja mais próximo do meio da fase
        # Primeiro tentar vãos maiores, depois relaxar o critério se necessário
        best = None  # (a, b, gap_left, gap_width, distance)
        min_gap_sizes = [60, 40, 20]  # Tentar diferentes tamanhos mínimos de vão

        for min_gap in min_gap_sizes:
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width >= min_gap:
                    center_x = gap_left + gap_width / 2
                    distance = abs(center_x - mid_x)
                    if best is None or distance < best[4]:
                        best = (a, b, gap_left, gap_width, distance)
            # Se encontrou um vão com este tamanho mínimo, usar ele
            if best is not None:
                break

        if best is not None:
            a, b, gap_left, gap_width, _ = best
            vertical_base = min(a.y, b.y)
            item_x = int(gap_left + gap_width / 2 - 12)
            # Aumentar dificuldade: maior distância vertical das plataformas
            extra_offset = int(140 + min(60, gap_width * 0.25))
            item_y = int(vertical_base - extra_offset)
            # Garantir que não saia muito do topo
            if item_y < 80:
                item_y = 80
            # Garantir pelo menos 120px acima da plataforma mais alta do par
            highest_platform_y = min(a.y, b.y)
            if highest_platform_y - item_y < 120:
                item_y = highest_platform_y - 120
                if item_y < 80:
                    item_y = 80
            item_image = getattr(game, "extra_life_img", None)
            game.extra_lives.append(ExtraLife(item_x, item_y, image=item_image))
            placed = True
        else:
            placed = False

        if not placed:
            # Fallback melhorado: tentar encontrar qualquer vão, mesmo pequeno
            fallback_best = None
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width > 0:  # Qualquer vão, mesmo muito pequeno
                    center_x = gap_left + gap_width / 2
                    distance = abs(center_x - mid_x)
                    if fallback_best is None or distance < fallback_best[4]:
                        fallback_best = (a, b, gap_left, gap_width, distance)

            if fallback_best is not None:
                # Usar o vão encontrado, mesmo que pequeno
                a, b, gap_left, gap_width, _ = fallback_best
                vertical_base = min(a.y, b.y)
                item_x = int(gap_left + gap_width / 2 - 12)
                # Ajustar offset baseado no tamanho do vão
                extra_offset = int(120 + min(40, gap_width * 0.2))
                item_y = int(vertical_base - extra_offset)
                if item_y < 80:
                    item_y = 80
                # Garantir pelo menos 100px acima da plataforma mais alta
                highest_platform_y = min(a.y, b.y)
                if highest_platform_y - item_y < 100:
                    item_y = highest_platform_y - 100
                    if item_y < 80:
                        item_y = 80
                item_image = getattr(game, "extra_life_img", None)
                game.extra_lives.append(ExtraLife(item_x, item_y, image=item_image))
            else:
                # Último recurso: posicionar acima de uma plataforma central
                idx = max(1, min(len(platforms_sorted) // 2, len(platforms_sorted) - 2))
                platform = platforms_sorted[idx]
                item_x = int(platform.x + platform.width // 2 - 12)
                item_y = int(platform.y - 140)
                if item_y < 80:
                    item_y = 80
                item_image = getattr(game, "extra_life_img", None)
                game.extra_lives.append(ExtraLife(item_x, item_y, image=item_image))

    def _find_collectible_spot(game):
        """Encontrar um vão apropriado para posicionamento de itens colecionáveis."""
        if not hasattr(game, "platforms") or not game.platforms:
            return None
        platforms_sorted = sorted(game.platforms, key=lambda p: p.x)
        min_x = platforms_sorted[0].x
        max_x = max(p.x + p.width for p in platforms_sorted)
        mid_x = (min_x + max_x) / 2
        best = None
        min_gap_sizes = [60, 40, 20]
        for min_gap in min_gap_sizes:
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width >= min_gap:
                    center_x = gap_left + gap_width / 2
                    distance = abs(center_x - mid_x)
                    if best is None or distance < best[4]:
                        best = (a, b, gap_left, gap_width, distance)
            if best is not None:
                break
        if best is None:
            fallback_best = None
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width > 0:
                    center_x = gap_left + gap_width / 2
                    distance = abs(center_x - mid_x)
                    if fallback_best is None or distance < fallback_best[4]:
                        fallback_best = (a, b, gap_left, gap_width, distance)
            if fallback_best is None:
                return None
            a, b, gap_left, gap_width, _ = fallback_best
        else:
            a, b, gap_left, gap_width, _ = best
        vertical_base = min(a.y, b.y)
        item_x = int(gap_left + gap_width / 2 - 12)
        extra_offset = int(140 + min(60, gap_width * 0.25))
        item_y = int(vertical_base - extra_offset)
        if item_y < 80:
            item_y = 80
        highest_platform_y = min(a.y, b.y)
        if highest_platform_y - item_y < 120:
            item_y = highest_platform_y - 120
            if item_y < 80:
                item_y = 80
        return (item_x, item_y)

    def _find_collectible_spot_excluding(game, exclude_points=None, exclude_gap_ranges=None, min_distance=200):
        """Como _find_collectible_spot, mas evita vãos próximos aos pontos excluídos e não reutiliza vãos.

        exclude_points: lista de tuplas (x, y) a evitar (apenas x é considerado para distância).
        exclude_gap_ranges: lista de tuplas (gap_left, gap_right) para vãos já utilizados.
        min_distance: distância mínima em X entre o centro do vão escolhido e qualquer ponto excluído.
        """
        if exclude_points is None:
            exclude_points = []
        if exclude_gap_ranges is None:
            exclude_gap_ranges = []
        if not hasattr(game, "platforms") or not game.platforms:
            return None

        platforms_sorted = sorted(game.platforms, key=lambda p: p.x)
        min_x = platforms_sorted[0].x
        max_x = max(p.x + p.width for p in platforms_sorted)
        mid_x = (min_x + max_x) / 2

        candidates = []  # (a, b, gap_left, gap_width, distance)
        min_gap_sizes = [60, 40, 20]
        for min_gap in min_gap_sizes:
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width >= min_gap:
                    center_x = gap_left + gap_width / 2
                    distance = abs(center_x - mid_x)
                    candidates.append((a, b, gap_left, gap_width, distance))
            if candidates:
                break

        if not candidates:
            # Fallback para qualquer vão positivo
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width > 0:
                    center_x = gap_left + gap_width / 2
                    distance = abs(center_x - mid_x)
                    candidates.append((a, b, gap_left, gap_width, distance))

        # Ordenar por proximidade ao meio
        candidates.sort(key=lambda c: c[4])

        # Escolher primeiro candidato que respeite a distância mínima de exclusão
        selected = None
        for a, b, gap_left, gap_width, _ in candidates:
            center_x = gap_left + gap_width / 2
            conflict = False
            for ex in exclude_points:
                ex_x = ex[0]
                if abs(center_x - ex_x) < min_distance:
                    conflict = True
                    break
            # Evitar reutilizar o mesmo vão
            if not conflict:
                candidate_gr = gap_left + gap_width
                for gl, gr in exclude_gap_ranges:
                    if gl == gap_left and gr == candidate_gr:
                        conflict = True
                        break
            if conflict:
                continue
            selected = (a, b, gap_left, gap_width)
            break

        # Se não encontramos respeitando min_distance, relaxar gradativamente
        if selected is None:
            for relax_frac in (0.75, 0.6, 0.5, 0.35, 0.25, 0.1, 0.05):
                relax = max(0, int(min_distance * relax_frac))
                for a, b, gap_left, gap_width, _ in candidates:
                    center_x = gap_left + gap_width / 2
                    conflict = False
                    for ex in exclude_points:
                        ex_x = ex[0]
                        if abs(center_x - ex_x) < relax:
                            conflict = True
                            break
                    if not conflict:
                        candidate_gr = gap_left + gap_width
                        for gl, gr in exclude_gap_ranges:
                            if gl == gap_left and gr == candidate_gr:
                                conflict = True
                                break
                    if conflict:
                        continue
                    selected = (a, b, gap_left, gap_width)
                    break
                if selected is not None:
                    break

        if selected is None:
            return None

        a, b, gap_left, gap_width = selected
        vertical_base = min(a.y, b.y)
        item_x = int(gap_left + gap_width / 2 - 12)
        extra_offset = int(140 + min(60, gap_width * 0.25))
        item_y = int(vertical_base - extra_offset)
        if item_y < 80:
            item_y = 80
        highest_platform_y = min(a.y, b.y)
        if highest_platform_y - item_y < 120:
            item_y = highest_platform_y - 120
            if item_y < 80:
                item_y = 80
        return (item_x, item_y, gap_left, gap_right)

    def _get_powerups_for_level(game):
        from internal.engine.difficulty import Difficulty
        lvl = getattr(game, "current_level", 1)
        diff = getattr(game, "difficulty", Difficulty.NORMAL)
        kinds = []
        # Fase 51: não deve haver power-ups
        if lvl == 51:
            return kinds
        if diff == Difficulty.EASY:
            cycle = ["invencibilidade", "pulo_duplo", "escudo"]
            kinds.append(cycle[(lvl - 1) % len(cycle)])
        elif diff == Difficulty.NORMAL:
            pos = (lvl - 1) % 10
            if pos in (0, 5):
                kinds.append("invencibilidade")
            elif pos in (2, 7):
                kinds.append("pulo_duplo")
            elif pos in (4, 9):
                kinds.append("escudo")
        else:
            pos = (lvl - 1) % 10
            if pos == 1:
                kinds.append("invencibilidade")
            elif pos == 4:
                kinds.append("pulo_duplo")
            elif pos == 7:
                kinds.append("escudo")
        return kinds

    def place_powerups(game):
        # Construir lista de vãos disponíveis e vãos já utilizados (vidas extras) para garantir separação
        kinds = Level._get_powerups_for_level(game)
        if not kinds:
            return

        # Excluir vãos próximos à vida extra e os próprios vãos usados por ela
        exclude_points = []
        exclude_gap_ranges = []
        if hasattr(game, "platforms") and game.platforms:
            platforms_sorted = sorted(game.platforms, key=lambda p: p.x)
            gaps = []
            for i in range(len(platforms_sorted) - 1):
                a = platforms_sorted[i]
                b = platforms_sorted[i + 1]
                gap_left = a.x + a.width
                gap_right = b.x
                gap_width = gap_right - gap_left
                if gap_width > 0:
                    gaps.append((gap_left, gap_right))
            if hasattr(game, "extra_lives") and game.extra_lives:
                for item in game.extra_lives:
                    exclude_points.append((item.x, item.y))
                    # Mapear vida extra ao vão mais próximo do seu X
                    closest = None
                    cx = item.x + 12  # aproximar ao centro do item
                    for gl, gr in gaps:
                        center = (gl + gr) / 2
                        dist = abs(center - cx)
                        if closest is None or dist < closest[0]:
                            closest = (dist, gl, gr)
                    if closest is not None:
                        _, gl, gr = closest
                        exclude_gap_ranges.append((gl, gr))

        # Calcular distância mínima equivalente a ~8 plataformas
        dynamic_min_distance = 200
        if hasattr(game, "platforms") and game.platforms:
            platforms_sorted = sorted(game.platforms, key=lambda p: p.x)
            spans = []
            for i in range(len(platforms_sorted) - 1):
                span = platforms_sorted[i + 1].x - platforms_sorted[i].x
                if span > 0:
                    spans.append(span)
            if spans:
                avg_span = sum(spans) / len(spans)
                dynamic_min_distance = int(avg_span * 8)

        # Selecionar um vão distinto para cada power-up
        chosen_spots = []  # (x, y)
        used_gap_ranges = list(exclude_gap_ranges)
        for idx, kind in enumerate(kinds):
            found = Level._find_collectible_spot_excluding(
                game,
                exclude_points=exclude_points + chosen_spots,
                exclude_gap_ranges=used_gap_ranges,
                min_distance=dynamic_min_distance,
            )
            if found is None:
                # Último recurso: tentar um spot padrão e garantir deslocamento em X fora do vão mapeado
                base = Level._find_collectible_spot(game)
                if base is None:
                    continue
                # Evitar reutilizar o mesmo vão: procurar outro gap por aproximação de centro
                # Deslocar 96px para fora do centro atual (tende a cair em outro vão em níveis com múltiplos)
                spot_x, spot_y = base[0] + (96 * (idx + 1)), base[1]
                chosen_spots.append((spot_x, spot_y))
            else:
                spot_x, spot_y, gl, gr = found
                chosen_spots.append((spot_x, spot_y))
                used_gap_ranges.append((gl, gr))

        if not chosen_spots:
            return

        # Criar os power-ups nas posições escolhidas
        for (spot_x, spot_y), kind in zip(chosen_spots, kinds):
            if kind == "invencibilidade":
                img = getattr(game, "powerup_invincibility_img", None)
            elif kind == "pulo_duplo":
                img = getattr(game, "powerup_double_jump_img", None)
            elif kind == "escudo":
                img = getattr(game, "powerup_shield_img", None)
            else:
                img = None
            x = spot_x
            y = spot_y
            spec = PowerUpSpec(kind=kind, image=img, width=24, height=24)
            game.powerups.append(PowerUp(x, y, spec))

    def drawTurtle(game, platform):
        turtle = Turtle(
            platform[0],
            platform[1] - 30,
            platform[0],
            platform[0] + platform[2],
            game.turtle_images,
        )
        game.turtles.append(turtle)
