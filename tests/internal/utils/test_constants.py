from internal.utils.constants import WIDTH, HEIGHT, FPS, GRAVITY, JUMP_STRENGTH, PLAYER_SPEED


def test_core_constants_ranges():
    assert WIDTH >= 320
    assert HEIGHT >= 240
    assert FPS >= 30
    assert 0 < GRAVITY < 1
    assert JUMP_STRENGTH < 0
    assert abs(JUMP_STRENGTH) > 0
    assert abs(PLAYER_SPEED) > 0