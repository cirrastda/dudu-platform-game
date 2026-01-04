from internal.engine.difficulty import Difficulty
from internal.engine.level.level import Level


class DifficultyOps:
    def __init__(self, game):
        self.g = game

    def update_bird_difficulty(self):
        """Atualiza parâmetros de spawn por faixa de nível e aplica
        modificadores da dificuldade.
        Mantém progressão por nível (Level.get_*) e ajusta quantidade e
        intervalo conforme Difficulty.
        """
        g = self.g

        # Definir fatores de dificuldade (quantidade e intervalo)
        diff = getattr(g, "difficulty", Difficulty.NORMAL)
        if diff == Difficulty.EASY:
            qty_factor = 0.7
            interval_factor = 1.5
            drop_interval_factor = 1.1
        elif diff == Difficulty.HARD:
            qty_factor = 1.4
            interval_factor = 0.7
            drop_interval_factor = 0.8
        else:
            qty_factor = 1.0
            interval_factor = 1.0
            drop_interval_factor = 1.0

        # Faixas de níveis e parâmetros base
        if g.current_level <= 20:
            # Pássaros: base por nível
            base_qty = Level.get_birds_per_spawn(g.current_level)
            base_interval = Level.get_bird_spawn_interval(g.current_level)
            # Aplicar dificuldade com limites
            g.birds_per_spawn = max(
                1,
                min(3, int(round(base_qty * qty_factor))),
            )
            # Respeitar limites da progressão
            # (mínimo 60 como nas funções de Level)
            g.bird_spawn_interval = max(
                60,
                int(base_interval * interval_factor),
            )
            # Gotas de chuva (fases 7-10): quantidade ajustada por dificuldade
            # 1x/2x/3x
            if 7 <= g.current_level <= 10:
                # Quantidade baseada na dificuldade: EASY=1, NORMAL=2, HARD=3
                if diff == Difficulty.EASY:
                    g.raindrops_per_spawn = 2
                elif diff == Difficulty.HARD:
                    g.raindrops_per_spawn = 5
                else:
                    g.raindrops_per_spawn = 3
                # Intervalo acompanha o dos pássaros com fator de dificuldade
                g.raindrop_spawn_interval = max(
                    60, int(base_interval * drop_interval_factor)
                )
            # A partir do nível 17, introduzir morcegos e estrelas cadentes
            if g.current_level >= 17:
                # Morcegos seguem a progressão dos pássaros
                # e aplicam dificuldade
                bat_base_qty = Level.get_birds_per_spawn(g.current_level)
                bat_base_interval = Level.get_bird_spawn_interval(
                    g.current_level
                )
                g.bats_per_spawn = max(
                    1,
                    min(3, int(round(bat_base_qty * qty_factor))),
                )
                g.bat_spawn_interval = max(
                    60,
                    int(bat_base_interval * interval_factor),
                )

                # Limitar quantidade máxima de morcegos visíveis (estabiliza
                # densidade na tela)
                # Aplica apenas nas fases 17-20 para manter consistência de
                # dificuldade
                g.max_bats_visible = 8 * qty_factor

                # Estrelas cadentes com presença moderada
                star_base_qty = 1
                star_base_interval = max(90, int(bat_base_interval * 1.2))
                g.shooting_stars_per_spawn = max(
                    1,
                    min(2, int(round(star_base_qty * qty_factor))),
                )
                g.shooting_star_spawn_interval = max(
                    80,
                    int(star_base_interval * interval_factor),
                )
        elif g.current_level <= 30:
            # Morcegos: seguem mesma progressão dos pássaros 11-20
            base_qty = Level.get_birds_per_spawn(g.current_level)
            base_interval = Level.get_bird_spawn_interval(g.current_level)
            g.bats_per_spawn = max(
                1,
                min(3, int(round(base_qty * qty_factor))),
            )
            g.bat_spawn_interval = max(
                60,
                int(base_interval * interval_factor),
            )
            # Fases 21–30: sem shooting stars
            g.shooting_stars_per_spawn = 0
            g.shooting_star_spawn_interval = 999999
            g.max_bats_visible = 8 * qty_factor
            # Gotas de lava (fases 27–30):
            # quantidade ajustada por dificuldade
            if 27 <= g.current_level <= 30:
                if diff == Difficulty.EASY:
                    g.lavadrops_per_spawn = 1
                elif diff == Difficulty.HARD:
                    g.lavadrops_per_spawn = 3
                else:
                    g.lavadrops_per_spawn = 2
                g.lavadrop_spawn_interval = max(
                    60,
                    int(base_interval * drop_interval_factor),
                )
                # Reduzir ainda mais a presença de morcegos na dificuldade EASY
                # nas fases 27–30
                if diff == Difficulty.EASY:
                    g.bats_per_spawn = 1
        elif g.current_level <= 40:
            # Aviões: usar valores base fixos e aplicar dificuldade
            base_qty = 1
            base_interval = 150
            g.airplanes_per_spawn = max(
                1,
                min(3, int(round(base_qty * qty_factor))),
            )
            g.airplane_spawn_interval = max(
                60,
                int(base_interval * interval_factor),
            )
            # Densidade de geradores/raios nas fases 37-40
            if 37 <= g.current_level <= 40:
                base_spacing = 180
                if diff == Difficulty.EASY:
                    # menos geradores
                    g.generator_spacing = int(base_spacing * 1.3)
                elif diff == Difficulty.HARD:
                    # mais geradores
                    g.generator_spacing = int(base_spacing * 0.7)
                else:
                    g.generator_spacing = base_spacing
        elif g.current_level <= 50:
            # Flying-disks: valores base fixos com dificuldade
            base_qty = 1
            base_interval = 150
            g.flying_disks_per_spawn = max(
                1,
                min(3, int(round(base_qty * qty_factor))),
            )
            g.flying_disk_spawn_interval = max(
                60,
                int(base_interval * interval_factor),
            )
            star_base_qty = 1
            star_base_interval = 120
            g.meteors_per_spawn = max(
                1,
                min(2, int(round(star_base_qty * qty_factor))),
            )
            g.meteor_spawn_interval = max(
                80,
                int(star_base_interval * interval_factor),
            )
        else:
            # Foguinhos (nível 51): valores base fixos com dificuldade
            base_qty = 1
            base_interval = 240
            g.fires_per_spawn = max(
                1,
                min(4, int(round(base_qty * qty_factor))),
            )
            g.fire_spawn_interval = max(
                60,
                int(base_interval * interval_factor),
            )
