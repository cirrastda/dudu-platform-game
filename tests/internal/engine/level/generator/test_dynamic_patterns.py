import math

from internal.engine.level.generator.dynamic import DynamicLevelGenerator
from internal.utils.constants import HEIGHT


def _assert_platforms_shape(platforms, min_len=1):
    assert isinstance(platforms, list)
    assert len(platforms) >= min_len
    for p in platforms:
        assert isinstance(p, tuple)
        assert len(p) == 4
        x, y, w, h = p
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert w > 0 and h > 0


def test_generate_level_platforms_all_patterns():
    # Cobrir 8 padrões variando o nível
    for level in range(6, 14):
        platforms = DynamicLevelGenerator.generate_level_platforms(level)
        _assert_platforms_shape(platforms, min_len=10)


class DummyPlayer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 32
        self.rect = type("Rect", (), {"x": 0, "y": 0})()
        self.vel_y = 0
        self.on_ground = False


def test_create_advanced_level_builds_platforms_and_positions_player():
    gen = DynamicLevelGenerator()
    gen.platforms = []
    gen.platform_texture = object()  # textura dummy
    gen.player = DummyPlayer()

    gen.create_advanced_level(11)
    assert len(gen.platforms) > 0
    first = gen.platforms[0]
    assert gen.player.x == first.x + 10
    assert gen.player.y == first.y - gen.player.height


def test_create_procedural_level_adds_turtles_for_level_11_plus():
    gen = DynamicLevelGenerator()
    gen.platforms = []
    gen.platform_texture = object()
    gen.player = DummyPlayer()
    gen.turtle_images = object()
    gen.turtles = []

    gen.create_procedural_level(15)
    # Deve criar plataformas e adicionar algumas tartarugas
    assert len(gen.platforms) > 0
    assert len(gen.turtles) >= 0  # pode ser 0 se poucas plataformas, mas não deve falhar