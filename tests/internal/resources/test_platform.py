from internal.resources.platform import Platform


class DummyTexture:
    def __init__(self, w, h):
        self._w = w
        self._h = h

    def get_width(self):
        return self._w

    def get_height(self):
        return self._h

    def subsurface(self, x, y, w, h):
        return DummyTexture(w, h)


class DummyScreen:
    def __init__(self):
        self.blit_calls = []

    def blit(self, img, pos):
        self.blit_calls.append((img, pos))


def test_platform_draw_tiled_texture():

    tex = DummyTexture(16, 10)
    p = Platform(10, 20, 40, 25, texture=tex)
    screen = DummyScreen()
    p.draw(screen)

    # Deve ter renderizado múltiplos blits (tiles completos e parciais)
    assert len(screen.blit_calls) > 0


def test_get_platform_texture_levels():
    class Image:
        platform_texture = object()
        platform_texture_city = object()

    class Game:
        image = Image()

    game = Game()
    assert Platform.get_platform_texture(game, 10) is game.image.platform_texture
    assert Platform.get_platform_texture(game, 40) is game.image.platform_texture_city