import types
import pygame

from internal.engine.game import Game
from internal.engine.state import GameState
from internal.engine.difficulty import Difficulty
from internal.resources.enemies.lava_drop import LavaDrop
from internal.engine.screen import Screen
from internal.utils.constants import WIDTH, HEIGHT

# Evitar dependência de display: mock de Screen.init para usar Surface em memória
Screen.init = lambda game: setattr(game, "screen", pygame.Surface((WIDTH, HEIGHT)))


def make_surface(w=20, h=20, color=(255, 80, 0)):
    surf = pygame.Surface((w, h))
    surf.fill(color)
    return surf


def test_lava_drop_basic_update_and_cull():
    img = make_surface(20, 20)
    drop = LavaDrop(10, 10, img)
    assert drop.update() is True
    # Forçar além da tela para cull
    drop.y = HEIGHT + 100
    assert drop.update() is False


def test_lava_drop_spawn_only_in_levels_27_to_30():
    g = Game()
    g.image.lava_drop_img = make_surface(20, 20)
    g.state = GameState.PLAYING

    # Antes da faixa (26): não deve spawnar
    g.current_level = 26
    g.lavadrop_spawn_interval = 1
    g.lavadrops_per_spawn = 3
    g.lavadrop_spawn_timer = 1
    g.update()
    assert len(getattr(g, "lava_drops", [])) == 0

    # Dentro da faixa (27): deve spawnar
    g.current_level = 27
    g.lavadrop_spawn_interval = 1
    g.lavadrops_per_spawn = 2
    g.lavadrop_spawn_timer = 1
    g.update()
    assert len(getattr(g, "lava_drops", [])) >= 2

    # Após a faixa (31): não deve spawnar
    g.current_level = 31
    g.lavadrop_spawn_interval = 1
    g.lavadrops_per_spawn = 3
    g.lavadrop_spawn_timer = 1
    # Limpar drops anteriores
    g.lava_drops = []
    g.update()
    assert len(getattr(g, "lava_drops", [])) == 0


def test_lava_drop_difficulty_scaling_levels_27_to_30():
    g = Game()
    g.current_level = 28

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    assert g.lavadrops_per_spawn == 2
    assert g.lavadrop_spawn_interval >= 60

    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.lavadrops_per_spawn == 3
    assert g.lavadrop_spawn_interval >= 60

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    assert g.lavadrops_per_spawn == 4
    assert g.lavadrop_spawn_interval >= 60


def test_lava_drop_spawn_and_draw_cycle():
    g = Game()
    g.current_level = 27
    g.image.lava_drop_img = make_surface(20, 20)
    g.lavadrop_spawn_interval = 1
    g.lavadrops_per_spawn = 2
    g.lavadrop_spawn_timer = 1
    g.state = GameState.PLAYING

    g.update()
    assert len(getattr(g, "lava_drops", [])) >= 2

    # Desenhar sem erro
    g.draw()
    assert len(g.lava_drops) >= 2


def test_lava_drop_collision_invulnerable_and_shield():
    g = Game()
    g.current_level = 27
    g.image.lava_drop_img = make_surface(20, 20)
    g.state = GameState.PLAYING

    # Colisão com invulnerabilidade: sem dano, gota persiste
    g.player.x, g.player.y = 40, 40
    g.player.rect = pygame.Rect(40, 40, getattr(g.player, "width", 65), getattr(g.player, "height", 95))
    g.player.is_invulnerable = True
    drop1 = LavaDrop(42, 42, g.image.lava_drop_img)
    g.lava_drops = [drop1]
    lives_before = g.lives
    g.update()
    assert g.lives == lives_before
    assert drop1 in g.lava_drops

    # Colisão com escudo: consome escudo, sem dano, gota persiste
    g.player.is_invulnerable = False
    g.shield_active = True
    drop2 = LavaDrop(42, 42, g.image.lava_drop_img)
    g.lava_drops = [drop2]
    lives_before = g.lives
    g.update()
    assert g.shield_active is False
    assert g.lives == lives_before
    assert g.player.is_hit is True
    assert drop2 in g.lava_drops


def test_lava_drop_collision_damage_and_game_over_path():
    g = Game()
    g.current_level = 27
    g.image.lava_drop_img = make_surface(20, 20)
    g.state = GameState.PLAYING

    g.player.x, g.player.y = 50, 50
    g.player.rect = pygame.Rect(50, 50, getattr(g.player, "width", 65), getattr(g.player, "height", 95))
    g.player.is_invulnerable = False
    g.shield_active = False
    g.player.is_hit = False

    drop = LavaDrop(52, 52, g.image.lava_drop_img)
    g.lava_drops = [drop]

    lives_before = g.lives
    g.update()
    assert g.lives == lives_before - 1
    assert g.player.is_hit is True


def test_lava_drop_bullet_collision_no_effect():
    g = Game()
    g.current_level = 27
    g.image.lava_drop_img = make_surface(20, 20)
    g.state = GameState.PLAYING

    drop = LavaDrop(60, 60, g.image.lava_drop_img)
    g.lava_drops = [drop]

    # Criar bala colidindo com a gota
    bullet_rect = pygame.Rect(60, 60, 10, 10)
    bullet = types.SimpleNamespace(
        rect=bullet_rect, x=60, y=60, update=lambda: None, draw=lambda *_: None
    )
    g.player.bullets = [bullet]
    g.return_bullet_to_pool = lambda *_: None

    g.update()
    # Sem lógica de bullets vs lava: bala permanece e gota também
    assert bullet in g.player.bullets
    assert drop in g.lava_drops


def test_lava_drop_reset_on_level_init():
    g = Game()
    g.current_level = 27
    g.lava_drops = [LavaDrop(0, 0, make_surface(20, 20))]
    from internal.engine.level.level import Level

    Level.init_level(g)
    assert getattr(g, "lava_drops", []) == []
    assert getattr(g, "lavadrop_spawn_timer", 999) == 0


def test_lava_drop_culling_with_camera_scroll():
    g = Game()
    g.current_level = 27
    g.state = GameState.PLAYING
    g.image.lava_drop_img = make_surface(20, 20)
    g.camera_x = 1000
    d1 = LavaDrop(1100, 100, g.image.lava_drop_img)
    d2 = LavaDrop(400, 100, g.image.lava_drop_img)
    g.lava_drops = [d1, d2]
    g.update()
    assert d1 in g.lava_drops
    assert d2 not in g.lava_drops


def test_lava_drop_repeated_collision_one_life_loss_per_hit():
    g = Game()
    g.current_level = 27
    g.state = GameState.PLAYING
    g.image.lava_drop_img = make_surface(20, 20)
    g.player.x, g.player.y = 50, 50
    g.player.rect = pygame.Rect(50, 50, getattr(g.player, "width", 65), getattr(g.player, "height", 95))
    g.player.is_invulnerable = False
    g.shield_active = False
    g.player.is_hit = False
    d = LavaDrop(52, 52, g.image.lava_drop_img)
    g.lava_drops = [d]
    lives_before = g.lives
    g.update()
    assert g.lives == lives_before - 1
    g.update()
    assert g.lives == lives_before - 1


def test_lava_drop_multi_wave_spawn_density_varies_by_difficulty():
    g = Game()
    g.current_level = 28
    g.state = GameState.PLAYING
    g.image.lava_drop_img = make_surface(20, 20)
    g.camera_x = 0
    for diff, expected in [(Difficulty.EASY, 1), (Difficulty.NORMAL, 4), (Difficulty.HARD, 6)]:
        g.difficulty = diff
        g.update_bird_difficulty()
        g.lava_drops = []
        for _ in range(3):
            g.lavadrop_spawn_interval = 1
            g.lavadrop_spawn_timer = 1
            g.update()
        assert len(g.lava_drops) >= expected


def test_lava_drop_game_over_restart_resets_and_spawns_again():
    g = Game()
    g.current_level = 27
    g.image.lava_drop_img = make_surface(20, 20)
    g.lava_drops = [LavaDrop(0, 0, g.image.lava_drop_img)]
    g.state = GameState.GAME_OVER
    g.game_over_selected = 0
    g.env_config = {"environment": "development", "initial-stage": "27"}
    pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 0}))
    g.handle_events()
    assert g.state == GameState.PLAYING
    assert g.current_level == 27
    assert g.lava_drops == []
    g.lavadrop_spawn_interval = 1
    g.lavadrops_per_spawn = 1
    g.lavadrop_spawn_timer = 1
    g.update()
    assert len(g.lava_drops) >= 1