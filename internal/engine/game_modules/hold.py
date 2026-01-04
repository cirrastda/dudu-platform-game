import pygame
from internal.utils.constants import FPS


class Hold:
    def __init__(self, game):
        self.game = game

    def _compute_sound_frames(self, sound_key, default_seconds=2.0):
        try:
            sound = self.game.sound_effects.sound_effects.get(sound_key)
            if sound:
                length = sound.get_length()
                if length and length > 0:
                    return max(1, int(length * FPS))
        except Exception:
            pass
        return max(1, int(default_seconds * FPS))

    def _start_hold(self, hold_type, frames, pending_state=None, next_level=False):
        self.game.hold_active = True
        self.game.hold_type = hold_type
        self.game.hold_frames_left = frames
        self.game.hold_total_frames = frames
        self.game._pending_state_after_hold = pending_state
        self.game._next_level_after_hold = next_level

    def start_game_over_hold(self):
        frames = self.game._compute_sound_frames("game-over", 2.0)
        self.game.sound_effects.play_sound_effect("game-over")
        # Para game over, apenas ativar esmaecimento enquanto a rotina atual continua
        self._start_hold("game_over", frames, pending_state=None, next_level=False)

    def start_level_end_hold(self, is_last_level):
        frames = self.game._compute_sound_frames("level-end", 2.0)
        self.game.sound_effects.play_sound_effect("level-end")
        # Apenas inicia esmaecimento; avanço de fase/estado acontece imediatamente
        self._start_hold("level_end", frames, pending_state=None, next_level=False)
        # Aplicar ducking na música para destacar o som de fim de fase
        self._apply_hold_ducking()

    def _apply_hold_ducking(self):
        """Reduz temporariamente o volume da música durante o hold."""
        try:
            # Guardar volume atual apenas na primeira aplicação
            if self.game._music_duck_original_volume is None:
                self.game._music_duck_original_volume = pygame.mixer.music.get_volume()
            # Reduzir volume para destacar efeitos sonoros
            ducked = max(0.0, self.game._music_duck_original_volume * 0.5)
            pygame.mixer.music.set_volume(ducked)
        except Exception:
            pass
