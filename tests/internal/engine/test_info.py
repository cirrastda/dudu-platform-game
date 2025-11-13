from internal.engine.info import Info
from internal.engine.difficulty import Difficulty


class FakeFont:
    def __init__(self):
        self.calls = []

    def render(self, text, antialias, color):
        self.calls.append((text, antialias, color))
        return f"surf:{text}"


class FakeScreen:
    def __init__(self):
        self.blits = []

    def blit(self, surf, pos):
        self.blits.append((surf, pos))


class FakeGame:
    def __init__(self, level, score, lives, difficulty):
        self.current_level = level
        self.score = score
        self.lives = lives
        self.difficulty = difficulty


def test_info_display_labels_and_positions():
    game = FakeGame(level=3, score=120, lives=2, difficulty=Difficulty.HARD)
    font = FakeFont()
    screen = FakeScreen()
    Info.display(game, screen, font, (255, 255, 255))

    texts = [t for (t, _a, _c) in font.calls]
    assert any("Nível: 3" in t for t in texts)
    assert any("Pontuação: 120" in t for t in texts)
    assert any("Vidas: 2" in t for t in texts)
    assert any("Dificuldade: Difícil" in t for t in texts)

    positions = [pos for _surf, pos in screen.blits]
    assert (10, 10) in positions
    assert (10, 130) in positions


def test_info_display_difficulty_easy_label():
    game = FakeGame(level=1, score=0, lives=3, difficulty=Difficulty.EASY)
    font = FakeFont()
    screen = FakeScreen()
    Info.display(game, screen, font, (255, 255, 255))
    texts = [t for (t, _a, _c) in font.calls]
    assert any("Dificuldade: Fácil" in t for t in texts)


class MinimalGame:
    # Sem atributo difficulty — deve usar Normal por padrão
    def __init__(self):
        self.current_level = 2
        self.score = 10
        self.lives = 1


def test_info_display_default_difficulty_normal():
    game = MinimalGame()
    font = FakeFont()
    screen = FakeScreen()
    Info.display(game, screen, font, (255, 255, 255))
    texts = [t for (t, _a, _c) in font.calls]
    assert any("Dificuldade: Normal" in t for t in texts)