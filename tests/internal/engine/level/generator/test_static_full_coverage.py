import types

import pytest


class DummyRect:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class DummyPlayer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 32
        self.rect = DummyRect()
        self.vel_y = 0
        self.on_ground = False


class DummyImage:
    def __init__(self):
        # Apenas atributos consultados pelo gerador estático
        self.boss_alien_images = object()


class FakeCache:
    def __init__(self):
        self.calls = []

    def get_image(self, path, scale=None):
        # Retorna um objeto simples para evitar I/O real
        self.calls.append((path, scale))
        return object()


class FakeBossAlien:
    def __init__(self, x, y, platforms, images):
        # Registrar parâmetros sem lógica pesada
        self.x = x
        self.y = y
        self.platforms = platforms
        self.images = images


def _make_game():
    game = types.SimpleNamespace()
    # Texturas e listas usadas pelos helpers
    game.platform_texture = object()
    game.platform_texture_city = object()
    game.platform_texture_space = object()
    game.platform_texture_ship = object()
    game.platform_texture_flag = object()
    game.platforms = []
    game.flag = None
    game.spaceship = None
    game.player = DummyPlayer()
    # Coleções de inimigos (alguns níveis podem chamar helpers)
    game.turtles = []
    game.spiders = []
    game.robots = []
    game.aliens = []
    game.airplanes = []
    # Imagens necessárias pelos inimigos e level 51
    game.turtle_images = object()
    game.spider_images = object()
    game.robot_images = object()
    game.missile_images = object()
    game.alien_images = object()
    game.airplane_images = object()
    game.image = DummyImage()
    return game


def test_all_static_levels_create_platforms(monkeypatch):
    # Patchar ResourceCache e BossAlien para evitar dependências externas
    import internal.engine.level.generator.static as static_mod

    monkeypatch.setattr(static_mod, "ResourceCache", lambda: FakeCache(), raising=True)
    # Patchar diretamente o módulo de BossAlien
    import internal.resources.enemies.boss_alien as boss_mod
    monkeypatch.setattr(boss_mod, "BossAlien", FakeBossAlien, raising=True)

    game = _make_game()

    # Iterar por todos os métodos create_level_1 .. create_level_51
    for lvl in range(1, 52):
        # Limpar estado entre níveis
        game.platforms = []
        game.flag = None
        game.spaceship = None

        # Obter referência ao método e invocar
        func = getattr(static_mod.StaticLevelGenerator, f"create_level_{lvl}")
        func(game)

        # Deve haver pelo menos uma plataforma criada
        assert isinstance(game.platforms, list)
        assert len(game.platforms) >= 1

        # PutPlayerInFirstPlatform é usado em todos níveis
        assert isinstance(game.player.x, (int, float))
        assert isinstance(game.player.y, (int, float))

        # Nível 51 configura boss_alien e desabilita tiros
        if lvl == 51:
            assert hasattr(game, "boss_alien")
            assert getattr(game, "can_shoot", False) is False