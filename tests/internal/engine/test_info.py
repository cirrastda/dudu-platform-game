import pygame
import pytest
from internal.engine.info import Info
from internal.engine.difficulty import Difficulty


class FakeFont:
    def __init__(self):
        self.calls = []

    def render(self, text, antialias, color):
        self.calls.append((text, antialias, color))
        # Retornar uma superfície fake com get_height/get_width
        class _FakeTextSurface:
            def __init__(self, t):
                self._t = t
            def get_height(self):
                return 40
            def get_width(self):
                return max(40, len(self._t) * 10)
        return _FakeTextSurface(text)


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
    # Simular ambiente de desenvolvimento para exibir a dificuldade
    def is_development(self):
        return True


def test_info_display_labels_and_positions(monkeypatch):
    game = FakeGame(level=3, score=120, lives=2, difficulty=Difficulty.HARD)
    font = FakeFont()
    screen = FakeScreen()

    # Capturar textos renderizados no topo
    top_font = FakeFont()
    monkeypatch.setattr(pygame.font, "SysFont", lambda *_a, **_k: top_font)

    Info.display(game, screen, font, (255, 255, 255))

    # Topo: rótulos atuais
    top_texts = [t for (t, _a, _c) in top_font.calls]
    assert any("Fase: 3" in t for t in top_texts)
    assert any("Pontos: 120" in t for t in top_texts)
    assert any("Dificuldade: Difícil" in t for t in top_texts)

    # Rodapé: texto de vidas (agora renderizado via SysFont stub)
    bottom_texts = [t for (t, _a, _c) in top_font.calls]
    assert any("x 2" in t for t in bottom_texts)

    positions = [pos for _surf, pos in screen.blits]
    assert (10, 10) in positions
    # Com FakeTextSurface.get_height()=40 e spacing=8, posição do rótulo de dificuldade
    assert (10, 58) in positions


def test_info_display_difficulty_easy_label(monkeypatch):
    game = FakeGame(level=1, score=0, lives=3, difficulty=Difficulty.EASY)
    font = FakeFont()
    screen = FakeScreen()
    top_font = FakeFont()
    monkeypatch.setattr(pygame.font, "SysFont", lambda *_a, **_k: top_font)
    Info.display(game, screen, font, (255, 255, 255))
    texts = [t for (t, _a, _c) in top_font.calls]
    assert any("Dificuldade: Fácil" in t for t in texts)


class MinimalGame:
    # Sem atributo difficulty — deve usar Normal por padrão
    def __init__(self):
        self.current_level = 2
        self.score = 10
        self.lives = 1
    def is_development(self):
        return True


def test_info_display_default_difficulty_normal(monkeypatch):
    game = MinimalGame()
    font = FakeFont()
    screen = FakeScreen()
    top_font = FakeFont()
    monkeypatch.setattr(pygame.font, "SysFont", lambda *_a, **_k: top_font)
    Info.display(game, screen, font, (255, 255, 255))
    texts = [t for (t, _a, _c) in top_font.calls]
    assert any("Dificuldade: Normal" in t for t in texts)