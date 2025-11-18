from internal.engine.difficulty import Difficulty


class Score:
    def __init__(self, game):
        self.game = game

    def get_score_multiplier(self):
        """Multiplicador de pontuação com base na dificuldade atual"""
        diff = getattr(self.game, "difficulty", Difficulty.NORMAL)
        if diff == Difficulty.EASY:
            return 0.4
        elif diff == Difficulty.HARD:
            return 3.0
        return 1.0

    def add_score(self, base_points):
        """Adiciona pontuação aplicando multiplicador da dificuldade e verifica vida extra.
        Retorna os pontos efetivamente adicionados.
        """
        try:
            # Usar o método do Game para permitir monkeypatch nos testes
            multiplier = self.game.get_score_multiplier()
        except Exception:
            multiplier = 1.0
        points = int(round(base_points * multiplier))
        # Garante pelo menos 1 ponto em incrementos positivos
        if base_points > 0 and points <= 0:
            points = 1
        self.game.score += points
        # Checar vida extra conforme sistema configurado por dificuldade
        # O método foi reencaminhado para Game no __init__ durante a ligação
        self.game.check_extra_life()
        return points
