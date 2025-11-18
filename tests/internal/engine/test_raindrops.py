import types
import pygame

from internal.engine.game import Game
from internal.engine.state import GameState
from internal.engine.difficulty import Difficulty
from internal.resources.enemies.raindrop import Raindrop
from internal.resources.platform import Platform
from internal.engine.screen import Screen
from internal.utils.constants import WIDTH, HEIGHT

# Evitar dependência de display: mock de Screen.init para usar Surface em memória
Screen.init = lambda game: setattr(game, "screen", pygame.Surface((WIDTH, HEIGHT)))


def make_surface(w=20, h=20, color=(0, 0, 255)):
    surf = pygame.Surface((w, h))
    surf.fill(color)
    return surf


def test_raindrop_difficulty_scaling():
    g = Game()
    g.current_level = 8

    g.difficulty = Difficulty.EASY
    g.update_bird_difficulty()
    assert g.raindrops_per_spawn == 3
    assert g.raindrop_spawn_interval >= 60

    g.difficulty = Difficulty.NORMAL
    g.update_bird_difficulty()
    assert g.raindrops_per_spawn == 6
    assert g.raindrop_spawn_interval >= 60

    g.difficulty = Difficulty.HARD
    g.update_bird_difficulty()
    assert g.raindrops_per_spawn == 9
    assert g.raindrop_spawn_interval >= 60


def test_raindrop_spawn_and_draw():
    g = Game()
    g.current_level = 8
    # Forçar imagem disponível
    g.image.raindrop_img = make_surface(20, 20)
    # Acelerar spawn
    g.raindrop_spawn_interval = 1
    g.raindrops_per_spawn = 2
    g.raindrop_spawn_timer = 1
    g.state = GameState.PLAYING

    # Atualiza para efetuar spawn
    g.update()
    assert len(getattr(g, "raindrops", [])) >= 2

    # Desenhar sem erro
    g.draw()
    # Lista de gotas permanece consistente após draw
    assert len(g.raindrops) >= 2


def test_raindrop_bullet_collision():
    g = Game()
    g.current_level = 8
    g.image.raindrop_img = make_surface(20, 20)
    drop = Raindrop(50, 50, g.image.raindrop_img)
    g.raindrops = [drop]

    # Criar bala colidindo com a gota
    bullet_rect = pygame.Rect(50, 50, 10, 10)
    bullet = types.SimpleNamespace(
        rect=bullet_rect, x=50, y=50, update=lambda: None, draw=lambda *_: None
    )
    g.player.bullets = [bullet]
    g.return_bullet_to_pool = lambda *_: None
    g.state = GameState.PLAYING

    g.update()
    assert bullet not in g.player.bullets
    assert drop.is_dead is True


def test_raindrop_player_collision_jump_vs_stand():
    g = Game()
    g.current_level = 8
    g.image.raindrop_img = make_surface(20, 20)
    # Posicionar jogador e gota em colisão
    g.player.x, g.player.y = 40, 40
    g.player.rect = pygame.Rect(
        g.player.x,
        g.player.y,
        getattr(g.player, "width", 65),
        getattr(g.player, "height", 95),
    )

    drop1 = Raindrop(42, 42, g.image.raindrop_img)
    g.raindrops = [drop1]

    # Caso: pulando (no ar) destrói a gota sem perder vida
    g.player.on_ground = False
    g.player.is_hit = False
    g.state = GameState.PLAYING
    lives_before = g.lives
    g.update()
    assert drop1.is_dead is True
    assert g.lives == lives_before

    # Caso: parado no chão causa hit e perda de vida
    drop2 = Raindrop(42, 42, g.image.raindrop_img)
    g.raindrops = [drop2]
    # Garantir que o jogador esteja de fato no chão durante o update
    # Criar uma plataforma logo abaixo da posição atual do jogador para que ele pouse
    ground_y = g.player.y + g.player.rect.height
    platform = Platform(g.player.x - 10, ground_y, 200, 20)
    g.platforms = [platform]
    # Simular queda para pouso na plataforma
    g.player.vel_y = 2
    g.player.on_ground = False
    g.player.is_hit = False
    g.player.is_invulnerable = False
    g.shield_active = False
    g.state = GameState.PLAYING
    lives_before = g.lives
    g.update()
    assert drop2.is_dead is True
    # Jogador deve entrar em estado de hit
    assert g.player.is_hit is True
