import types


def _make_game():
    g = types.SimpleNamespace()
    g.turtles = []
    g.spiders = []
    g.robots = []
    g.aliens = []
    g.airplanes = []
    g.turtle_images = object()
    g.spider_images = object()
    g.robot_images = object()
    g.missile_images = object()
    g.alien_images = object()
    g.airplane_images = object()
    return g


def test_level_enemy_draw_all():
    from internal.engine.level.enemy import LevelEnemy

    game = _make_game()
    # Plataforma base (x, y, width)
    p = (100, 300, 120)

    # Cobrir todos os métodos
    LevelEnemy.drawTurtle(game, p)
    LevelEnemy.drawSpider(game, p)
    LevelEnemy.drawRobot(game, p)
    LevelEnemy.drawAlien(game, p)
    LevelEnemy.drawAirplane(game, p)

    # drawAirplanes com fator gera múltiplas chamadas
    platforms = [(100, 300, 120), (300, 280, 100), (500, 260, 90), (700, 240, 80)]
    LevelEnemy.drawAirplanes(game, platforms, factor=2)

    # As listas devem ter sido preenchidas
    assert len(game.turtles) >= 1
    assert len(game.spiders) >= 1
    assert len(game.robots) >= 1
    assert len(game.aliens) >= 1
    assert len(game.airplanes) >= 1