from internal.engine.level.generator.dynamic import DynamicLevelGenerator
from internal.utils.constants import HEIGHT


def test_get_platforms_stairway_basic():
    platforms = DynamicLevelGenerator.get_platforms_stairway(
        initial_x=0,
        total_platforms=5,
        platform_width=100,
        x_factor=50,
        y_factor=20,
        top_limit=HEIGHT - 300,
    )
    assert isinstance(platforms, list)
    assert len(platforms) == 5
    for x, y, w, h in platforms:
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert w == 100
        assert h == 20


def test_get_platforms_stairway_wrap():
    # Forçar wrap do Y ao ultrapassar o limite superior
    platforms = DynamicLevelGenerator.get_platforms_stairway(
        initial_x=0,
        total_platforms=3,
        platform_width=80,
        x_factor=10,
        y_factor=HEIGHT,
        top_limit=HEIGHT - 10,
    )
    initial_y = HEIGHT - 150
    assert platforms[0][1] == initial_y
    assert platforms[1][1] == initial_y  # y resetado ao initial_y