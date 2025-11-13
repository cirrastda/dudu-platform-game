import types

import pytest


class FakeSurface:
    pass


def test_init_level_initializes_game(monkeypatch):
    from internal.engine.level import level as level_module
    from internal.resources import player as player_module
    from internal.utils.constants import HEIGHT

    # Patch ResourceCache to avoid real I/O
    class FakeCache:
        def __init__(self):
            self.calls = []
        def get_image(self, path, scale):
            self.calls.append((path, scale))
            return FakeSurface()

    monkeypatch.setattr(level_module, "ResourceCache", lambda: FakeCache(), raising=True)

    # Patch Player to avoid pygame dependency and record args
    class FakePlayer:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Level module likely holds its own Player reference; patch there
    monkeypatch.setattr(level_module, "Player", FakePlayer, raising=True)

    # Avoid generator side effects: intercept create_level_platforms
    def fake_create(self, level):
        # Self here is 'game' object passed by Level.init_level
        self.platforms_created = level

    monkeypatch.setattr(level_module.Level, "create_level_platforms", fake_create, raising=True)

    # Fake game object
    game = types.SimpleNamespace()
    game.current_level = 3
    game.update_bird_difficulty = lambda: None

    # Ensure menu background starts empty to exercise branch
    assert not hasattr(game, "menu_background_img")

    level_module.Level.init_level(game)

    # Player initialized at the documented position
    assert isinstance(game.player, FakePlayer)
    assert game.player.x == 50
    assert game.player.y == HEIGHT - 200

    # Lists initialized
    for attr in [
        "platforms", "birds", "bats", "turtles", "spiders", "robots",
        "aliens", "orphan_lasers", "explosions", "flying_disks", "extra_lives",
    ]:
        assert hasattr(game, attr)
        assert isinstance(getattr(game, attr), list)

    # Pools exist
    assert hasattr(game, "bullet_pool") and isinstance(game.bullet_pool, list)
    assert hasattr(game, "explosion_pool") and isinstance(game.explosion_pool, list)

    # Backgrounds loaded through cache
    assert isinstance(game.background_img, FakeSurface)
    assert isinstance(game.menu_background_img, FakeSurface)

    # Platforms creation invoked with current level
    assert getattr(game, "platforms_created", None) == 3