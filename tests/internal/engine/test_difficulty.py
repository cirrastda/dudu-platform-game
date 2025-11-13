from internal.engine.difficulty import Difficulty


def test_difficulty_members_exist():
    assert Difficulty.EASY.name == "EASY"
    assert Difficulty.NORMAL.name == "NORMAL"
    assert Difficulty.HARD.name == "HARD"