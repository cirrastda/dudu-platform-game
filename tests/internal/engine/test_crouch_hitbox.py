import pygame
import types


def make_rect(x=0, y=0, w=10, h=10):
    return pygame.Rect(x, y, w, h)


def test_player_effective_rect_crouch_avoids_bottom_overlap(monkeypatch):
    import internal.resources.player as player_mod

    pygame.init()

    p = player_mod.Player(100, 100)
    # Simular abaixado
    p.is_crouching = True
    p.rect = make_rect(100, 100, 50, 40)

    # Inimigo que invade apenas 6px pela parte de baixo (colidiria com rect normal)
    enemy = make_rect(110, 138, 10, 10)  # 138..148 sobrepõe 140..140+6

    # Com rect normal, deve colidir
    assert p.rect.colliderect(enemy)

    # Com hitbox efetiva (reduz 8px na base), não deve colidir
    eff = p.get_airborne_collision_rect()
    assert not eff.colliderect(enemy)


def test_update_bird_collision_respects_crouch_effective_hitbox(monkeypatch):
    # Setup de jogo básico
    from internal.engine.game import Game, GameState

    pygame.init()
    pygame.font.init()
    g = Game()
    g.state = GameState.PLAYING
    g.current_level = 5  # níveis de pássaros

    # Assets mínimos
    g.image.bird_img1 = pygame.Surface((6, 6))
    g.image.bird_img2 = pygame.Surface((6, 6))
    g.image.explosion_image = pygame.Surface((6, 6))

    # Jogador agachado com rect conhecido
    g.player.rect = make_rect(200, 200, 50, 40)
    g.player.is_crouching = True
    # Não atualiza o jogador neste teste
    g.player.update = lambda *a, **k: None
    g.player.is_hit = False
    g.player.is_invulnerable = False
    if hasattr(g, "shield_active"):
        g.shield_active = False

    # Pássaro posicionado para colidir com rect normal, mas não com hitbox efetiva
    bird = types.SimpleNamespace(
        x=210,
        y=238,
        id="b1",
        rect=make_rect(210, 238, 10, 10),
        update=lambda *a, **k: True,
        draw=lambda *a, **k: None,
    )
    g.birds = [bird]

    pre_lives = g.lives
    g.update()

    # Não deve ter tomado dano nem removido o pássaro
    assert g.player.is_hit is False
    assert g.lives == pre_lives
    assert bird in g.birds


def test_update_bat_collision_respects_crouch_effective_hitbox(monkeypatch):
    # Setup de jogo básico
    from internal.engine.game import Game, GameState

    pygame.init()
    pygame.font.init()
    g = Game()
    g.state = GameState.PLAYING
    g.current_level = 17  # níveis de morcegos/estrelas

    # Assets mínimos
    g.image.bat_img1 = pygame.Surface((6, 6))
    g.image.bat_img2 = pygame.Surface((6, 6))
    g.image.explosion_image = pygame.Surface((6, 6))

    # Jogador agachado com rect conhecido
    g.player.rect = make_rect(300, 300, 50, 40)
    g.player.is_crouching = True
    g.player.update = lambda *a, **k: None
    g.player.is_hit = False
    g.player.is_invulnerable = False
    if hasattr(g, "shield_active"):
        g.shield_active = False

    bat = types.SimpleNamespace(
        x=310,
        y=338,
        id="bat1",
        rect=make_rect(310, 338, 10, 10),
        update=lambda *a, **k: True,
        draw=lambda *a, **k: None,
        is_dead=False,
    )
    g.bats = [bat]
    g.shooting_stars = []

    pre_lives = g.lives
    g.update()

    assert g.player.is_hit is False
    assert g.lives == pre_lives
    assert bat in g.bats
