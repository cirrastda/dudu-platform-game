import types
from types import SimpleNamespace

import pytest

from internal.engine.level.level import Level
from internal.engine.difficulty import Difficulty


def test_level_51_no_powerups_easy():
    game = SimpleNamespace(current_level=51, difficulty=Difficulty.EASY)
    kinds = Level._get_powerups_for_level(game)
    assert kinds == []


def test_level_51_no_powerups_normal():
    game = SimpleNamespace(current_level=51, difficulty=Difficulty.NORMAL)
    kinds = Level._get_powerups_for_level(game)
    assert kinds == []


def test_level_51_no_powerups_hard():
    game = SimpleNamespace(current_level=51, difficulty=Difficulty.HARD)
    kinds = Level._get_powerups_for_level(game)
    assert kinds == []


def test_place_powerups_level_51_no_spawn(monkeypatch):
    game = SimpleNamespace(current_level=51, difficulty=Difficulty.NORMAL, powerups=[])
    # Evita dependências do mapa: assegura que há um ponto válido
    monkeypatch.setattr(Level, "_find_collectible_spot", staticmethod(lambda g: (100, 100)))
    Level.place_powerups(game)
    assert len(game.powerups) == 0