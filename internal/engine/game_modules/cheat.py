import pygame


class Cheat:
    def __init__(self, game):
        self.g = game

    def process_cheat_token(self, token):
        g = self.g
        if not token:
            return
        g._cheat_buffer.append(token)
        if len(g._cheat_buffer) > len(g._cheat_sequence):
            g._cheat_buffer = g._cheat_buffer[-len(g._cheat_sequence) :]
        if g._cheat_buffer == g._cheat_sequence:
            g.cheat_99_lives_enabled = True
            g.max_lives = 99
            g.lives = 99

    def map_key_to_cheat_token(self, key, unicode_val=""):
        if key == pygame.K_UP:
            return "UP"
        if key == pygame.K_DOWN:
            return "DOWN"
        if key == pygame.K_LEFT:
            return "LEFT"
        if key == pygame.K_RIGHT:
            return "RIGHT"
        if key == pygame.K_b or unicode_val.lower() == "b":
            return "B"
        if key == pygame.K_a or unicode_val.lower() == "a":
            return "A"
        return None