from internal.engine.difficulty import Difficulty
from internal.engine.level.level import Level


class DifficultyOps:
    def __init__(self, game):
        self.g = game

    def update_bird_difficulty(self):
        """Atualiza parâmetros de spawn por faixa de nível e aplica modificadores da dificuldade.
        Mantém progressão por nível (Level.get_*) e ajusta quantidade/intervalo conforme Difficulty.
        """
        g = self.g

        # Definir fatores de dificuldade (quantidade e intervalo)
        diff = getattr(g, "difficulty", Difficulty.NORMAL)
        if diff == Difficulty.EASY:
            qty_factor = 0.7
            interval_factor = 1.5
        elif diff == Difficulty.HARD:
            qty_factor = 1.4
            interval_factor = 0.7
        else:
            qty_factor = 1.0
            interval_factor = 1.0

        # Faixas de níveis e parâmetros base
        if g.current_level <= 20:
            # Pássaros: base por nível
            base_qty = Level.get_birds_per_spawn(g.current_level)
            base_interval = Level.get_bird_spawn_interval(g.current_level)
            # Aplicar dificuldade com limites
            g.birds_per_spawn = max(1, min(3, int(round(base_qty * qty_factor))))
            # Respeitar limites da progressão (mínimo 60 como nas funções de Level)
            g.bird_spawn_interval = max(60, int(base_interval * interval_factor))
        elif g.current_level <= 30:
            # Morcegos: seguem mesma progressão dos pássaros 11-20
            base_qty = Level.get_birds_per_spawn(g.current_level)
            base_interval = Level.get_bird_spawn_interval(g.current_level)
            g.bats_per_spawn = max(1, min(3, int(round(base_qty * qty_factor))))
            g.bat_spawn_interval = max(60, int(base_interval * interval_factor))
        elif g.current_level <= 40:
            # Aviões: usar valores base fixos e aplicar dificuldade
            base_qty = 1
            base_interval = 150
            g.airplanes_per_spawn = max(1, min(3, int(round(base_qty * qty_factor))))
            g.airplane_spawn_interval = max(60, int(base_interval * interval_factor))
        elif g.current_level <= 50:
            # Flying-disks: valores base fixos com dificuldade
            base_qty = 1
            base_interval = 150
            g.flying_disks_per_spawn = max(1, min(3, int(round(base_qty * qty_factor))))
            g.flying_disk_spawn_interval = max(60, int(base_interval * interval_factor))
        else:
            # Foguinhos (nível 51): valores base fixos com dificuldade
            base_qty = 1
            base_interval = 240
            g.fires_per_spawn = max(1, min(4, int(round(base_qty * qty_factor))))
            g.fire_spawn_interval = max(60, int(base_interval * interval_factor))