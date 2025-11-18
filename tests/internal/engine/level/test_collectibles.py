import types
import math
import pytest


# Fixture headless mínima para evitar dependências gráficas do pygame
@pytest.fixture(autouse=True)
def headless_pygame(monkeypatch):
    class FakeSurface:
        def __init__(self, w=10, h=10):
            self.w = w
            self.h = h

        def get_rect(self, **kwargs):
            return types.SimpleNamespace(
                center=kwargs.get("center", (self.w // 2, self.h // 2))
            )

    class FakeRect:
        def __init__(self, x=0, y=0, w=10, h=10):
            self.x = x
            self.y = y
            self.width = w
            self.height = h

        @property
        def right(self):
            return self.x + self.width

        @property
        def bottom(self):
            return self.y + self.height

        def colliderect(self, other):
            return not (
                self.right <= other.x
                or other.right <= self.x
                or self.bottom <= other.y
                or other.bottom <= self.y
            )

    fake_pygame = types.SimpleNamespace(
        Rect=FakeRect,
        image=types.SimpleNamespace(load=lambda _p: FakeSurface()),
        transform=types.SimpleNamespace(scale=lambda surf, size: surf),
        draw=types.SimpleNamespace(
            rect=lambda *a, **k: None, polygon=lambda *a, **k: None
        ),
    )
    monkeypatch.setitem(sys.modules, "pygame", fake_pygame)

    # Evitar carregamento de imagens no ResourceCache
    from internal.resources.cache import ResourceCache

    monkeypatch.setattr(ResourceCache, "get_image", lambda self, path, size=None: None)


import sys
import internal.engine.game as game_mod
from internal.engine.level.level import Level
from internal.engine.difficulty import Difficulty
from internal.utils.constants import GRAVITY, JUMP_STRENGTH


def make_game(monkeypatch):
    # Tornar __init__ inofensivo
    monkeypatch.setattr(game_mod.Game, "__init__", lambda self: None)
    # Neutralizar ENV_CONFIG para não interferir com valores de dificuldade
    monkeypatch.setattr(game_mod, "ENV_CONFIG", {}, raising=False)
    g = game_mod.Game()
    g.env_config = {}
    g.difficulty = Difficulty.NORMAL
    g.current_level = 1
    g.score = 0
    g.lives = 0
    milestones, inc = game_mod.Game.get_extra_life_milestones_and_increment(g)
    g.extra_life_milestones = milestones
    g.extra_life_increment_after_milestones = inc
    g.next_extra_life_score = milestones[0]
    g.extra_lives_earned = 0
    g.sound_effects = types.SimpleNamespace(play_sound_effect=lambda name: None)
    g.birds_per_spawn = 0
    g.bird_spawn_interval = 0
    # Texturas esperadas pelos geradores estáticos
    g.platform_texture = object()
    g.platform_texture_city = object()
    g.platform_texture_space = object()
    g.platform_texture_ship = object()
    g.platform_texture_flag = object()
    # Imagens esperadas em níveis avançados (ex.: boss da fase 51)
    g.image = types.SimpleNamespace(
        boss_alien_images={
            "running": [object()],
            "jumping": [object()],
            "stopped": object(),
        }
    )
    return g


def _avg_platform_span(platforms):
    spans = []
    for i in range(len(platforms) - 1):
        span = platforms[i + 1].x - platforms[i].x
        if span > 0:
            spans.append(span)
    if not spans:
        return 200
    return sum(spans) / len(spans)


def _nearest_platforms_for_x(platforms, x_center):
    # Retorna (esquerda, direita) ao redor do x_center
    left = None
    right = None
    for p in sorted(platforms, key=lambda p: p.x):
        if p.x + p.width <= x_center:
            left = p
        elif p.x >= x_center and right is None:
            right = p
    return left, right


def _vertical_base_from_neighbors(left, right):
    ys = []
    if left is not None:
        ys.append(left.y)
    if right is not None:
        ys.append(right.y)
    if not ys:
        return None
    return min(ys)


def _max_jump_height():
    # Aproximação contínua: v^2 = 2 g h
    v = abs(JUMP_STRENGTH)
    g = GRAVITY
    return (v * v) / (2 * g)


def test_collectibles_distance_and_before_flag_and_reachable(monkeypatch):
    g = make_game(monkeypatch)
    g.difficulty = Difficulty.NORMAL
    g.current_level = 3  # Deve gerar pulo_duplo
    Level.init_level(g)

    assert hasattr(g, "platforms") and g.platforms, "Plataformas não inicializadas"
    assert g.flag is not None, "Bandeira não posicionada"

    items = []
    items.extend(getattr(g, "extra_lives", []))
    items.extend(getattr(g, "powerups", []))
    # Pelo menos vida extra deve existir
    assert items, "Nenhum coletável encontrado no nível"

    # Distância mínima dinâmica (~8 plataformas)
    avg_span = _avg_platform_span(g.platforms)
    dynamic_min_distance = int(avg_span * 8)

    centers = [(it.x + 12, it.y) for it in items]
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dx = abs(centers[i][0] - centers[j][0])
            assert (
                dx >= dynamic_min_distance
            ), f"Coletáveis muito próximos: dx={dx} < {dynamic_min_distance}"

    # Antes da bandeira
    for it in items:
        assert it.x < g.flag.x, "Coletável posicionado depois da bandeira da fase"

    # Alcançável pelo pulo: diferença vertical menor que altura máxima de pulo
    hmax = _max_jump_height()
    for it in items:
        x_center = it.x + 12
        left, right = _nearest_platforms_for_x(g.platforms, x_center)
        vb = _vertical_base_from_neighbors(left, right)
        assert vb is not None, "Não foi possível determinar plataformas vizinhas ao gap"
        dv = vb - it.y
        assert dv <= hmax + 20, f"Coletável inalcançável pelo pulo: dv={dv} > {hmax}"


def test_powerup_quantity_by_difficulty(monkeypatch):
    # EASY: sempre 1 por nível
    g = make_game(monkeypatch)
    g.difficulty = Difficulty.EASY
    for lvl in (1, 2, 3, 4, 5):
        g.current_level = lvl
        Level.init_level(g)
        assert (
            len(getattr(g, "powerups", [])) == 1
        ), f"EASY nível {lvl} deve ter 1 power-up"

    # NORMAL: depende do ciclo pos em {0,2,4,5,7,9}
    g = make_game(monkeypatch)
    g.difficulty = Difficulty.NORMAL
    expectations = {
        1: 1,  # invencibilidade
        2: 0,
        3: 1,  # pulo_duplo
        4: 0,
        5: 1,  # escudo
        6: 1,  # invencibilidade
        7: 0,
        8: 1,  # pulo_duplo
        9: 0,
        10: 1,  # escudo
    }
    for lvl, expected in expectations.items():
        g.current_level = lvl
        Level.init_level(g)
        assert (
            len(getattr(g, "powerups", [])) == expected
        ), f"NORMAL nível {lvl} deveria ter {expected} power-ups"

    # HARD: somente pos == 1,4,7
    g = make_game(monkeypatch)
    g.difficulty = Difficulty.HARD
    expectations_h = {
        1: 0,
        2: 1,  # invencibilidade
        3: 0,
        4: 0,
        5: 1,  # pulo_duplo
        6: 0,
        7: 0,
        8: 1,  # escudo
        9: 0,
        10: 0,
    }
    for lvl, expected in expectations_h.items():
        g.current_level = lvl
        Level.init_level(g)
        assert (
            len(getattr(g, "powerups", [])) == expected
        ), f"HARD nível {lvl} deveria ter {expected} power-ups"

    # Fase 51: nunca tem power-ups
    g = make_game(monkeypatch)
    g.difficulty = Difficulty.NORMAL
    g.current_level = 51
    Level.init_level(g)
    assert len(getattr(g, "powerups", [])) == 0, "Fase 51 não deve ter power-ups"
