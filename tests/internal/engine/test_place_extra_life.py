import types

import pytest


def make_platform(x, y, width, height=30):
    return types.SimpleNamespace(x=x, y=y, width=width, height=height)


def test_place_extra_life_primary_gap(monkeypatch):
    from internal.engine.level.level import Level

    # Game with two platforms leaving a wide gap
    game = types.SimpleNamespace()
    game.platforms = [
        make_platform(100, 400, 200),
        make_platform(500, 380, 250),
    ]
    game.extra_lives = []

    Level.place_extra_life(game)

    assert len(game.extra_lives) == 1
    item = game.extra_lives[0]

    # X should be near the gap center minus 12
    gap_left = game.platforms[0].x + game.platforms[0].width
    gap_right = game.platforms[1].x
    center_x = gap_left + (gap_right - gap_left) / 2
    assert abs(item.x - int(center_x - 12)) <= 1

    # Y should be at least 100 px above the higher platform, and >= 80
    highest_y = min(game.platforms[0].y, game.platforms[1].y)
    assert item.y >= 80
    assert highest_y - item.y >= 100


def test_place_extra_life_fallback_small_gap(monkeypatch):
    from internal.engine.level.level import Level

    # Small positive gap triggers fallback_best branch
    game = types.SimpleNamespace()
    game.platforms = [
        make_platform(100, 400, 200),
        make_platform(301, 390, 5),  # gap of 1px
    ]
    game.extra_lives = []

    Level.place_extra_life(game)

    assert len(game.extra_lives) == 1
    item = game.extra_lives[0]
    assert item.y >= 80
    highest_y = min(game.platforms[0].y, game.platforms[1].y)
    assert highest_y - item.y >= 90  # relaxed vs primary path


def test_place_extra_life_last_resort_no_gap(monkeypatch):
    from internal.engine.level.level import Level

    # No gap at all triggers final branch (central platform)
    game = types.SimpleNamespace()
    game.platforms = [
        make_platform(100, 400, 200),
        make_platform(300, 400, 200),  # touches previous (gap 0)
        make_platform(500, 410, 200),
    ]
    game.extra_lives = []

    Level.place_extra_life(game)

    assert len(game.extra_lives) == 1
    item = game.extra_lives[0]
    # Placed above central-ish platform index
    # Ensure plausible bounds
    assert item.y >= 80
    # Check X lies within central platform horizontal span +/- few px
    platform = sorted(game.platforms, key=lambda p: p.x)[len(game.platforms)//2]
    assert platform.x - 20 <= item.x <= platform.x + platform.width + 20