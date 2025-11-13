import math

from internal.engine.level.generator.dynamic import DynamicLevelGenerator
from internal.utils.constants import HEIGHT


def _assert_platforms_shape(platforms, expected_len=None, min_len=1):
    assert isinstance(platforms, list)
    if expected_len is not None:
        assert len(platforms) == expected_len
    else:
        assert len(platforms) >= min_len
    for p in platforms:
        assert isinstance(p, tuple) and len(p) == 4
        x, y, w, h = p
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert w > 0 and h > 0
        # y deve estar em uma faixa plausível da tela
        assert -50 <= y <= HEIGHT + 50


def test_generate_random_clusters_properties():
    platforms = DynamicLevelGenerator.generate_random_clusters(
        start_x=60, start_y=HEIGHT - 200, num_platforms=30, num_clusters=3
    )
    _assert_platforms_shape(platforms, expected_len=30)


def test_generate_maze_pattern_properties():
    platforms = DynamicLevelGenerator.generate_maze_pattern(
        start_x=60, start_y=HEIGHT - 220, num_platforms=28
    )
    _assert_platforms_shape(platforms, expected_len=28)


def test_generate_level_platforms_dispatch_clusters_and_maze():
    # level 10 -> pattern_choice 4 (clusters)
    clusters = DynamicLevelGenerator.generate_level_platforms(10)
    _assert_platforms_shape(clusters, min_len=10)
    # level 11 -> pattern_choice 5 (maze)
    maze = DynamicLevelGenerator.generate_level_platforms(11)
    _assert_platforms_shape(maze, min_len=10)