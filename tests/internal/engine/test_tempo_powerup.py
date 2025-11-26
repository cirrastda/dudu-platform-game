import types
from types import SimpleNamespace

import pygame
import pytest

from internal.engine.level.level import Level
from internal.engine.difficulty import Difficulty


def make_game(monkeypatch):
    from internal.engine.game import Game, GameState

    # Forçar dummy display
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1, 1))

    # Construir jogo
    g = Game()
    # Tornar update do player um no-op
    g.player.update = lambda *a, **k: None
    g.state = GameState.PLAYING
    return g


def _tempo_powerup_spec(g):
    from internal.resources.powerup import PowerUpSpec

    img = getattr(g, "powerup_tempo_img", None)
    return PowerUpSpec(kind="tempo", image=img, width=24, height=24)


def test_collect_tempo_slows_bird(monkeypatch):
    g = make_game(monkeypatch)
    g.current_level = 5
    Level.init_level(g)
    # Colocar um pássaro com velocidade conhecida
    from internal.resources.enemies.bird import Bird

    bird = Bird(g.camera_x + 200, 100, None)
    bird.speed = 5.0
    g.birds = [bird]

    # Criar power-up tempo na posição do player
    from internal.resources.powerup import PowerUp

    spec = _tempo_powerup_spec(g)
    pu = PowerUp(g.player.rect.x, g.player.rect.y, spec)
    g.powerups = [pu]

    # Coletar e aplicar efeito
    g.update()  # coleta e ativa tempo antes de atualizar inimigos
    assert g.tempo_active is True

    # Próximo frame: deslocamento reduzido (80% menos => 20% do original)
    x1 = bird.x
    g.update()
    delta = x1 - bird.x
    assert 0.9 < delta < 1.1  # ~1.0 (20% de 5.0)


def test_tempo_expires_after_duration(monkeypatch):
    g = make_game(monkeypatch)
    g.current_level = 3
    Level.init_level(g)
    # Ativar tempo manualmente
    g.tempo_active = True
    g.tempo_frames_left = 5
    g.tempo_factor = 0.2

    from internal.resources.enemies.bird import Bird

    bird = Bird(g.camera_x + 200, 100, None)
    bird.speed = 5.0
    g.birds = [bird]

    # Consumir tempo
    for _ in range(g.tempo_frames_left + 1):
        g.update()

    assert g.tempo_active is False

    # Após expirar: deslocamento volta ao normal (~5.0)
    pre = bird.x
    g.update()
    delta = pre - bird.x
    assert 4.9 < delta < 5.1


def test_tempo_ends_on_level_end(monkeypatch):
    g = make_game(monkeypatch)
    g.current_level = 2
    Level.init_level(g)
    g.tempo_active = True
    g.tempo_frames_left = 999999
    g.tempo_factor = 0.2
    # Simular hold de fim de fase
    g.hold_active = True
    g.hold_type = "level_end"
    g.hold_frames_left = 10

    g.update()
    assert g.tempo_active is False


def test_projectiles_slow_with_tempo_robot(monkeypatch):
    g = make_game(monkeypatch)
    g.current_level = 31
    from internal.resources.enemies.robot import Robot

    # Configuração simples de robô que dispara imediatamente
    r = Robot(g.camera_x + 300, 140, g.camera_x + 280, g.camera_x + 340, None, None)
    r.shoot_timer = r.shoot_interval  # força disparo
    g.robots = [r]
    g.tempo_active = True
    g.tempo_frames_left = 50
    g.tempo_factor = 0.2

    # Atualiza para criar míssil
    g.update()
    assert r.missiles, "Robô deveria ter criado míssil"
    m = r.missiles[0]
    pre = m.x
    g.update()
    delta = pre - m.x
    assert 0.7 < delta < 0.9  # ~0.8 (20% de 4)


def test_projectiles_slow_with_tempo_alien(monkeypatch):
    g = make_game(monkeypatch)
    g.current_level = 41
    from internal.resources.enemies.alien import Alien

    a = Alien(g.camera_x + 300, 120, g.camera_x + 280, g.camera_x + 340, None)
    a.shoot_timer = a.shoot_interval
    g.aliens = [a]
    g.tempo_active = True
    g.tempo_frames_left = 50
    g.tempo_factor = 0.2

    g.update()
    assert a.lasers, "Alien deveria ter criado laser"
    lz = a.lasers[0]
    pre = lz.x
    g.update()
    delta = pre - lz.x
    assert 0.9 < delta < 1.1  # ~1.0 (20% de 5)


def test_music_slow_flag_on_off(monkeypatch):
    g = make_game(monkeypatch)
    g.current_level = 5
    Level.init_level(g)
    assert not getattr(g, "_tempo_music_active", False)
    # Ativar tempo
    g.tempo_active = True
    g.tempo_frames_left = 2
    g.tempo_factor = 0.2
    # Entrar em modo tempo via update
    g.update()
    # Consumir
    g.update()
    g.update()
    assert g.tempo_active is False
    # Encerrado


def test_schedule_includes_tempo(monkeypatch):
    # EASY: ciclo deve incluir tempo
    game = SimpleNamespace(current_level=4, difficulty=Difficulty.EASY)
    kinds = Level._get_powerups_for_level(game)
    assert kinds == ["tempo"]

    # NORMAL: pos==5 inclui tempo
    game = SimpleNamespace(current_level=6, difficulty=Difficulty.NORMAL)
    kinds = Level._get_powerups_for_level(game)
    assert kinds == ["tempo"]


def test_env_start_tempo_development(monkeypatch):
    # Iniciar com tempo via .env em dev
    from internal.engine import game as game_mod
    game_mod.ENV_CONFIG = {
        "environment": "development",
        "initial-stage": "3",
        "tempo": "on",
    }
    g = make_game(monkeypatch)
    assert g.tempo_active is True
    assert g.tempo_frames_left > 0