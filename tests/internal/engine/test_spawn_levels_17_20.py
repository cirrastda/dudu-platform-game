import types
import pygame
import pytest

from internal.engine.game import Game
from internal.engine.level.level import Level
from internal.engine.state import GameState


def _setup_game_at_level(level: int):
    g = Game()
    g.current_level = level
    g.state = GameState.PLAYING
    # Inicializa nível (reseta listas e aplica dificuldade)
    Level.init_level(g)
    # Garantir que câmera começa em 0
    g.camera_x = 0
    return g


def test_spawn_bats_and_shooting_stars_on_level_17(monkeypatch):
    g = _setup_game_at_level(17)

    # Forçar timers curtos e quantidades para garantir spawn imediato
    g.bat_spawn_interval = 1
    g.bats_per_spawn = 2
    g.shooting_star_spawn_interval = 1
    g.shooting_stars_per_spawn = 1

    # Rodar uma atualização: deve spawnar morcegos e estrelas
    g.update()

    assert len(getattr(g, "bats", [])) >= 1
    assert len(getattr(g, "shooting_stars", [])) >= 1
    # Pássaros não devem spawnar em 17–20
    assert len(getattr(g, "birds", [])) == 0


def test_spawn_bats_and_shooting_stars_on_level_20(monkeypatch):
    g = _setup_game_at_level(20)

    g.bat_spawn_interval = 1
    g.bats_per_spawn = 1
    g.shooting_star_spawn_interval = 1
    g.shooting_stars_per_spawn = 1

    g.update()

    assert len(getattr(g, "bats", [])) >= 1
    assert len(getattr(g, "shooting_stars", [])) >= 1
    assert len(getattr(g, "birds", [])) == 0


def test_draw_renders_bats_and_stars_on_level_17(monkeypatch):
    g = _setup_game_at_level(17)

    # Garantir entidades presentes para o desenho
    g.bat_spawn_interval = 1
    g.bats_per_spawn = 1
    g.shooting_star_spawn_interval = 1
    g.shooting_stars_per_spawn = 1
    g.update()

    # Contadores de chamadas draw
    bat_draw_calls = {"n": 0}
    star_draw_calls = {"n": 0}

    # Posicionar entidades dentro da janela visível
    for bat in g.bats:
        bat.x = g.camera_x + 10
    for star in g.shooting_stars:
        star.x = g.camera_x + 10

    # Monkeypatch nos métodos draw das entidades reais
    for bat in g.bats:
        monkeypatch.setattr(
            bat,
            "draw",
            lambda screen, _b=bat_draw_calls: _b.__setitem__("n", _b["n"] + 1),
        )
    for star in g.shooting_stars:
        monkeypatch.setattr(
            star,
            "draw",
            lambda screen, _s=star_draw_calls: _s.__setitem__("n", _s["n"] + 1),
        )

    # Executar desenho
    g.draw()

    assert bat_draw_calls["n"] >= 1
    assert star_draw_calls["n"] >= 1


def test_birds_do_not_spawn_on_level_17(monkeypatch):
    g = _setup_game_at_level(17)

    # Mesmo com valores agressivos, pássaros não devem spawnar em 17–20
    g.bird_spawn_interval = 1
    g.birds_per_spawn = 3

    # Atualizar e validar que lista continua vazia
    g.update()
    assert len(getattr(g, "birds", [])) == 0
