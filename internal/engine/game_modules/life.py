from internal.engine.difficulty import Difficulty
from internal.utils.constants import DEFAULT_INITIAL_LIVES


class Life:
    def __init__(self, game):
        self.game = game

    def get_initial_lives(self):
        """Obter o número inicial de vidas baseado na configuração e dificuldade"""
        # Código secreto habilita 99 vidas
        if getattr(self.game, "cheat_99_lives_enabled", False):
            return 99

        # Ler do .env em modo development, se válido
        env = getattr(self.game, "env_config", {})
        if env.get("environment") == "development" and "lives" in env:
            lives_val = env.get("lives")
            if (
                isinstance(lives_val, str)
                and lives_val.isdigit()
                and int(lives_val) > 0
            ):
                return int(lives_val)

        # Padrões por dificuldade
        diff = getattr(self.game, "difficulty", Difficulty.NORMAL)
        if diff == Difficulty.EASY:
            return 5
        elif diff == Difficulty.HARD:
            return 2
        else:
            return DEFAULT_INITIAL_LIVES

    def get_extra_life_milestones_and_increment(self):
        """Retorna (marcos_iniciais, incremento) conforme dificuldade"""
        diff = getattr(self.game, "difficulty", Difficulty.NORMAL)
        if diff == Difficulty.EASY:
            return [1000, 2000, 3000], 1000
        elif diff == Difficulty.HARD:
            return [5000, 10000, 20000], 20000
        else:  # Normal
            return [1000, 5000, 10000], 10000

    def check_extra_life(self):
        """Verificar se o jogador merece uma vida extra baseada na pontuação"""
        game = self.game
        if game.score >= game.next_extra_life_score:
            # Conceder vida extra
            game.lives += 1
            game.extra_lives_earned += 1

            # Tocar som de vida extra
            game.sound_effects.play_sound_effect("new-life")

            # Calcular próxima pontuação para vida extra conforme dificuldade
            if game.extra_lives_earned < len(game.extra_life_milestones):
                game.next_extra_life_score = game.extra_life_milestones[
                    game.extra_lives_earned
                ]
            else:
                # Após os marcos iniciais, usar incremento configurado pela dificuldade
                increment = getattr(
                    game, "extra_life_increment_after_milestones", 10000
                )
                game.next_extra_life_score += increment

            return True  # Indica que uma vida extra foi concedida
        return False
