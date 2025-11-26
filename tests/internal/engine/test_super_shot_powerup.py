import pygame
import pytest

from internal.engine.level.level import Level
from internal.engine.difficulty import Difficulty


def make_game():
    from internal.engine.game import Game, GameState
    pygame.init(); pygame.display.init(); pygame.display.set_mode((1,1))
    g = Game()
    g.player.update = lambda *a, **k: None
    g.state = GameState.PLAYING
    return g


def test_collect_super_shot_enables_burst_and_speed():
    g = make_game()
    g.current_level = 5
    Level.init_level(g)

    # Criar power-up supertiro na posição do jogador
    from internal.resources.powerup import PowerUp, PowerUpSpec
    spec = PowerUpSpec(kind="supertiro", image=getattr(g, "powerup_super_shot_img", None), width=24, height=24)
    pu = PowerUp(g.player.rect.x, g.player.rect.y, spec)
    g.powerups = [pu]

    # Coletar
    g.update()
    assert g.super_shot_active is True

    # Disparar um tiro
    pre_count = len(g.player.bullets)
    g.player.vel_x = 0
    g.player.shoot(getattr(g.image, "bullet_image", None), g)
    assert len(g.player.bullets) >= pre_count + 3
    # Verificar velocidade aumentada
    speeds = [b.speed for b in g.player.bullets[-3:]]
    assert all(s >= 13 for s in speeds)  # 8 * 1.7 ~= 14


def test_super_shot_expires(monkeypatch):
    g = make_game()
    g.current_level = 5
    Level.init_level(g)
    g.super_shot_active = True
    g.super_shot_frames_left = 3

    for _ in range(4):
        g.update()
    assert g.super_shot_active is False


def test_super_shot_ends_on_level_end():
    g = make_game()
    g.current_level = 5
    Level.init_level(g)
    g.super_shot_active = True
    g.super_shot_frames_left = 999
    g.hold_active = True
    g.hold_type = "level_end"
    g.update()
    assert g.super_shot_active is False


def test_schedule_includes_super_shot():
    game = type("G", (), {"current_level": 10, "difficulty": Difficulty.NORMAL})()
    kinds = Level._get_powerups_for_level(game)
    assert kinds == ["supertiro"]

    game = type("G", (), {"current_level": 5, "difficulty": Difficulty.EASY})()
    kinds = Level._get_powerups_for_level(game)
    assert kinds == ["supertiro"]


def test_env_start_super_shot_dev(monkeypatch):
    from internal.engine import game as game_mod
    game_mod.ENV_CONFIG = {"environment": "development", "initial-stage": "3", "supertiro": "on"}
    g = make_game()
    assert g.super_shot_active is True
    assert g.super_shot_frames_left > 0