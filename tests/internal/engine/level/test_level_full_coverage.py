import types


class FakeSurface:
    pass


class FakeCache:
    def __init__(self):
        self.calls = []

    def get_image(self, path, scale):
        self.calls.append((path, scale))
        return FakeSurface()


class DummyRect:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class DummyPlayer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 32
        self.rect = DummyRect()
        self.vel_y = 0
        self.on_ground = False


def _make_game():
    g = types.SimpleNamespace()
    g.current_level = 1
    g.update_bird_difficulty = lambda: None
    g.platform_texture = object()
    g.platform_texture_city = object()
    g.platform_texture_space = object()
    g.platform_texture_ship = object()
    g.platform_texture_flag = object()
    g.platforms = []
    g.player = DummyPlayer()
    g.image = DummyImage()
    # Espelhar imagens para LevelEnemy via Level module
    g.turtle_images = object()
    g.spider_images = object()
    g.robot_images = object()
    g.missile_images = object()
    g.alien_images = object()
    g.airplane_images = object()
    # Coleções usadas pelo LevelEnemy
    g.turtles = []
    g.spiders = []
    g.robots = []
    g.aliens = []
    g.airplanes = []
    return g


def test_create_level_platforms_all_branches(monkeypatch):
    from internal.engine.level import level as level_mod

    # Patch ResourceCache
    monkeypatch.setattr(level_mod, "ResourceCache", lambda: FakeCache(), raising=True)

    game = _make_game()

    # Exercitar background por níveis
    for lvl in (1, 11, 21, 31, 41, 51, 99):
        img = level_mod.Level.get_background_for_level(level_mod.Level, lvl)
        assert isinstance(img, str)

    # Chamar create_level_platforms para cada nível conhecido (1..51)
    for lvl in range(1, 52):
        game.current_level = lvl
        level_mod.Level.create_level_platforms(game, lvl)
        assert len(game.platforms) >= 1
        game.platforms.clear()

    # Exercitar draw_level_bg caminho principal
    game.background_img = level_mod.Level.draw_level_bg(game, 5)
    assert isinstance(game.background_img, FakeSurface)


def test_level_value_functions_cover_branches():
    from internal.engine.level.level import Level

    # get_birds_per_spawn branches
    assert Level.get_birds_per_spawn(1) == 1
    assert Level.get_birds_per_spawn(4) == 1
    assert Level.get_birds_per_spawn(15) == 2
    assert Level.get_birds_per_spawn(17) == 3
    assert Level.get_birds_per_spawn(18) == 2
    assert Level.get_birds_per_spawn(25) in (1, 2, 3)
    assert Level.get_birds_per_spawn(30) in (2, 3)
    assert Level.get_birds_per_spawn(99) == 2

    # get_bird_spawn_interval branches
    assert 60 <= Level.get_bird_spawn_interval(1) <= 180
    assert 60 <= Level.get_bird_spawn_interval(16) <= 180
    assert Level.get_bird_spawn_interval(17) >= 70
    assert Level.get_bird_spawn_interval(20) >= 70
    assert 60 <= Level.get_bird_spawn_interval(25) <= 180
    assert Level.get_bird_spawn_interval(30) >= 70
    assert Level.get_bird_spawn_interval(99) >= 60


def test_level_value_functions_beyond_30_exact():
    from internal.engine.level.level import Level

    # Cobrir exatamente os retornos dos blocos else (level > 30)
    assert Level.get_birds_per_spawn(31) == 2
    assert Level.get_bird_spawn_interval(31) == 60


def test_level_value_functions_exact_edges_30_31():
    from internal.engine.level.level import Level

    # Cobrir else interno do bloco 21..30 e o else geral
    assert Level.get_birds_per_spawn(30) == 2
    assert Level.get_bird_spawn_interval(30) == 75


def test_birds_per_spawn_21_24_and_27_precise():
    from internal.engine.level.level import Level

    # Cobrir retorno 2 no bloco 21..24 seguindo padrão das fases 11-20
    assert Level.get_birds_per_spawn(21) == 2
    assert Level.get_birds_per_spawn(24) == 2
    # Cobrir retorno 3 no bloco 27..30 quando equivalente_bird_level <= 17
    assert Level.get_birds_per_spawn(27) == 3


def test_place_extra_life_clamps_and_level_draw_turtle():
    from internal.engine.level import level as level_mod

    # Forçar clamp item_y < 80 no caminho principal
    game = _make_game()
    # Criar plataformas com gap grande e y muito alto (perto do topo)
    game.platforms = [
        types.SimpleNamespace(x=100, y=60, width=200, height=20),
        types.SimpleNamespace(x=500, y=60, width=150, height=20),
    ]
    game.extra_lives = []
    level_mod.Level.place_extra_life(game)
    assert len(game.extra_lives) == 1
    assert game.extra_lives[0].y == 80  # clamped

    # Forçar ajuste de ">=100 acima" no fallback_best
    game.platforms = [
        types.SimpleNamespace(x=100, y=200, width=200, height=20),
        types.SimpleNamespace(x=301, y=210, width=5, height=20),  # gap de 1
    ]
    game.extra_lives = []
    level_mod.Level.place_extra_life(game)
    assert len(game.extra_lives) == 1
    highest_y = min(game.platforms[0].y, game.platforms[1].y)
    assert highest_y - game.extra_lives[0].y >= 100

    # Cobrir Level.drawTurtle
    level_mod.Level.drawTurtle(game, (100, 300, 120))
    assert len(game.turtles) >= 1


def test_place_extra_life_last_resort_branch():
    from internal.engine.level import level as level_mod

    game = _make_game()
    # Plataformas que se sobrepõem (sem vão > 0) para forçar último recurso
    game.platforms = [
        types.SimpleNamespace(x=100, y=250, width=200, height=20),  # right=300
        types.SimpleNamespace(
            x=280, y=245, width=150, height=20
        ),  # right=430, gap_right < gap_left
    ]
    game.extra_lives = []

    level_mod.Level.place_extra_life(game)
    assert len(game.extra_lives) == 1
    # Deve posicionar acima da plataforma central; sem clamp (<80) aqui
    assert game.extra_lives[0].y >= 80


def test_place_extra_life_fallback_best_clamp_and_ensure_100():
    from internal.engine.level import level as level_mod

    game = _make_game()
    # Pequeno vão (>0) e plataformas baixas para acionar clamp e garantia de 100px
    game.platforms = [
        types.SimpleNamespace(x=100, y=150, width=200, height=20),  # right=300
        types.SimpleNamespace(x=301, y=151, width=5, height=20),  # gap=1
    ]
    game.extra_lives = []

    level_mod.Level.place_extra_life(game)
    assert len(game.extra_lives) == 1
    # Primeiro clamp a 80, depois garantia de 100px deveria ajustar mas voltar a clamp
    assert game.extra_lives[0].y == 80


def test_place_extra_life_last_resort_clamp():
    from internal.engine.level import level as level_mod

    game = _make_game()
    # Sem vão (>0) e plataforma baixa para acionar clamp no último recurso
    game.platforms = [
        types.SimpleNamespace(x=100, y=100, width=200, height=20),  # right=300
        types.SimpleNamespace(x=280, y=95, width=150, height=20),  # overlap
    ]
    game.extra_lives = []

    level_mod.Level.place_extra_life(game)
    assert len(game.extra_lives) == 1
    assert game.extra_lives[0].y == 80


def test_get_background_for_level_all_ranges():
    from internal.engine.level.level import Level

    game = _make_game()

    # Faixa cidade (<=20)
    bg_city = Level.get_background_for_level(game, 10)
    assert isinstance(bg_city, str) and bg_city.endswith("fase 1.5.png")

    # Faixa espaço (21..40)
    bg_space = Level.get_background_for_level(game, 25)
    assert isinstance(bg_space, str) and bg_space.endswith("fase 3.png")

    # Faixa nave (==51)
    bg_ship = Level.get_background_for_level(game, 51)
    assert isinstance(bg_ship, str) and bg_ship.endswith("fase 6.png")


class DummyImage:
    def __init__(self):
        self.boss_alien_images = object()
