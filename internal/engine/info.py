from internal.engine.difficulty import Difficulty

class Info:
    def display(game, screen, font, color):
        level_text = font.render(f"Nível: {game.current_level}", True, color)
        score_text = font.render(f"Pontuação: {game.score}", True, color)
        lives_text = font.render(f"Vidas: {game.lives}", True, color)

        # Mapear dificuldade para rótulos em PT-BR
        diff = getattr(game, 'difficulty', Difficulty.NORMAL)
        diff_label_map = {
            Difficulty.EASY: "Fácil",
            Difficulty.NORMAL: "Normal",
            Difficulty.HARD: "Difícil",
        }
        difficulty_text = font.render(f"Dificuldade: {diff_label_map.get(diff, 'Normal')}", True, color)

        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(lives_text, (10, 90))
        screen.blit(difficulty_text, (10, 130))
