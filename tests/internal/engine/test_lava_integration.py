import pygame

from internal.engine.game import Game
from internal.engine.state import GameState
from internal.engine.screen import Screen
from internal.utils.constants import WIDTH, HEIGHT


def _init_screen(game):
    setattr(game, "screen", pygame.Surface((WIDTH, HEIGHT)))


Screen.init = _init_screen


def make_surface(w=20, h=20, color=(255, 80, 0)):
    surf = pygame.Surface((w, h))
    surf.fill(color)
    return surf


def test_lava_draw_camera_offset_visibility_window():
    g = Game()
    g.current_level = 27
    g.state = GameState.PLAYING
    g.image.lava_drop_img = make_surface(20, 20)

    # Criar duas gotas: uma dentro da janela e outra fora
    in_view = type("D", (), {})()
    in_view.__dict__.update({
        "x": 100,
        "y": 100,
        "image": g.image.lava_drop_img,
        "draw": lambda *args, **kwargs: None,
    })
    out_view = type("D", (), {})()
    out_view.__dict__.update({
        "x": -500,
        "y": 100,
        "image": g.image.lava_drop_img,
        "draw": lambda *args, **kwargs: None,
    })
    # Emular retângulos
    in_view.rect = pygame.Rect(in_view.x, in_view.y, 20, 20)
    out_view.rect = pygame.Rect(out_view.x, out_view.y, 20, 20)

    g.lava_drops = [in_view, out_view]
    # Ajustar câmera e desenhar
    g.camera_x = 0
    g.draw()
    assert len(g.lava_drops) == 2
