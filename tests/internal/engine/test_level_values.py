import types

import pytest


def test_get_background_for_level_mapping():
    from internal.engine.level.level import Level

    lvl = Level()
    assert lvl.get_background_for_level(1) == "imagens/fundo3.png"
    assert lvl.get_background_for_level(15) == "imagens/fundo5.png"
    assert lvl.get_background_for_level(25) == "imagens/fundo7.png"
    assert lvl.get_background_for_level(35) == "imagens/fundoMundo4.2.jpg"
    assert lvl.get_background_for_level(45) == "imagens/fundoEspaco.png"
    assert lvl.get_background_for_level(51) == "imagens/fundoNave.png"
    assert lvl.get_background_for_level(100) == "imagens/fundo6.png"


def test_draw_level_bg_calls_cache(monkeypatch):
    from internal.engine.level import level as level_module
    from internal.utils.constants import WIDTH, HEIGHT

    class FakeSurface:
        pass

    class FakeCache:
        def __init__(self):
            self.last_path = None
            self.last_scale = None

        def get_image(self, path, scale):
            self.last_path = path
            self.last_scale = scale
            return FakeSurface()

    # Patch the ResourceCache symbol used inside Level
    instance = FakeCache()
    monkeypatch.setattr(level_module, "ResourceCache", lambda: instance, raising=True)

    lvl = level_module.Level()
    surf = lvl.draw_level_bg(1)

    assert isinstance(surf, FakeSurface)
    # Verify that width/height scaling is requested
    assert instance.last_path == "imagens/fundo3.png"
    assert instance.last_scale == (WIDTH, HEIGHT)


def test_get_birds_per_spawn_rules():
    from internal.engine.level.level import Level

    assert Level.get_birds_per_spawn(1) == 1
    assert Level.get_birds_per_spawn(16) == 3
    assert Level.get_birds_per_spawn(17) == 3
    assert Level.get_birds_per_spawn(19) == 2
    # Levels 21-30 follow birds 11-20 rules
    assert Level.get_birds_per_spawn(25) == 2
    assert Level.get_birds_per_spawn(30) == 2


def test_get_bird_spawn_interval_bounds():
    from internal.engine.level.level import Level

    # Specific expected values from the formula
    assert Level.get_bird_spawn_interval(17) == 90
    assert Level.get_bird_spawn_interval(20) == 75
    # Range checks for other levels to avoid float rounding edge cases
    assert 60 <= Level.get_bird_spawn_interval(1) <= 180
    assert 60 <= Level.get_bird_spawn_interval(16) <= 180
    # Levels 21-30 mirrored behaviour; level 30 should be 75
    assert Level.get_bird_spawn_interval(30) == 75