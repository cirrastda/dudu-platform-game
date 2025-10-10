class Info:
    def display(game, screen, font, color):
        level_text = font.render(f"Nível: {game.current_level}", True, color)
        score_text = font.render(f"Pontuação: {game.score}", True, color)
        lives_text = font.render(f"Vidas: {game.lives}", True, color)
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(lives_text, (10, 90))
