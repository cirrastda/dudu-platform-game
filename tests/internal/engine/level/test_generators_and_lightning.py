import types


def _make_platform(x, y, w, h=20):
    return types.SimpleNamespace(x=x, y=y, width=w, height=h, rect=types.SimpleNamespace(x=x, y=y, width=w, height=h, right=x+w))


def test_generators_avoid_platform_columns(monkeypatch):
    from internal.engine.level.generator import static as static_mod
    game = types.SimpleNamespace()
    # Plataformas cobrindo várias faixas de x
    game.platforms = [
        (100, 400, 150, 20),
        (400, 360, 200, 20),
        (800, 300, 180, 20),
    ]
    game.player = types.SimpleNamespace(height=30)
    game.image = types.SimpleNamespace(generator_img=None)
    static_mod.StaticLevelGenerator.drawGenerators(game, game.platforms)
    assert hasattr(game, 'generators')
    # Garantir que nenhuma coluna escolhida caia dentro do span horizontal das plataformas
    blocked = [(p[0], p[0] + p[2]) for p in game.platforms]
    for g in game.generators:
        gx = g.x + g.width // 2
        assert all(not (l <= gx <= r) for (l, r) in blocked)


def test_difficulty_changes_generator_density(monkeypatch):
    from internal.engine.game import DifficultyOps
    from internal.engine.difficulty import Difficulty
    from internal.engine.level.generator import static as static_mod
    # Layout largo sem muitas obstruções
    platforms = [
        (50, 420, 120, 20),
        (300, 380, 120, 20),
        (600, 360, 140, 20),
        (950, 340, 140, 20),
    ]
    def run_for_diff(diff):
        game = types.SimpleNamespace()
        game.current_level = 37
        game.difficulty = diff
        game.player = types.SimpleNamespace(height=30)
        DifficultyOps(game).update_bird_difficulty()
        game.image = types.SimpleNamespace(generator_img=None)
        static_mod.StaticLevelGenerator.drawGenerators(game, platforms)
        return len(game.generators)
    easy_n = run_for_diff(Difficulty.EASY)
    normal_n = run_for_diff(Difficulty.NORMAL)
    hard_n = run_for_diff(Difficulty.HARD)
    assert easy_n < normal_n <= hard_n


def test_lightning_segments_do_not_cross_platforms(monkeypatch):
    import internal.resources.lightning as lightning_mod
    # Stub pygame.Rect
    class Rect:
        def __init__(self, x, y, w, h):
            self.x, self.y, self.w, self.h = x, y, w, h
            self.width, self.height = w, h
        def copy(self):
            return Rect(self.x, self.y, self.w, self.h)
        def colliderect(self, other):
            return not (
                self.x + self.w <= other.x or other.x + other.width <= self.x or
                self.y + self.h <= other.y or other.y + other.height <= self.y
            )
    monkeypatch.setattr(lightning_mod, 'pygame', types.SimpleNamespace(Rect=Rect), False)
    # Fake segment image with fixed size
    class Img:
        def get_width(self): return 12
        def get_height(self): return 6
    # Platforms rects (using Rect-compatible objects)
    plats = [types.SimpleNamespace(x=200, y=350, width=160, height=20), types.SimpleNamespace(x=500, y=330, width=140, height=20)]
    # Horizontal beam that would pass across platforms; segments must skip
    lb = lightning_mod.LightningBeam((100, 360), (700, 360), 'h', Img())
    lightning_mod.LightningBeam.build_segments(lb, [types.SimpleNamespace(x=p.x, y=p.y, width=p.width, height=p.height) for p in plats])
    assert len(lb.segments) > 0
    assert all(not Rect(getattr(seg, 'x', seg.x), getattr(seg, 'y', seg.y), getattr(seg, 'width', getattr(seg, 'w', 0)), getattr(seg, 'height', getattr(seg, 'h', 0))).colliderect(types.SimpleNamespace(x=p.x, y=p.y, width=p.width, height=p.height)) for seg in lb.segments for p in plats)