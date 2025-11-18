import pygame
from internal.utils.constants import FPS


class System:
    def __init__(self, game):
        self.g = game

    def is_development(self):
        return self.g.env_config.get("environment") == "development"

    def run(self):
        g = self.g
        running = True
        while running:
            running = g.handle_events()
            g.update()
            g.draw()
            g.clock.tick(FPS)
        # Encerramento gracioso
        try:
            g.shutdown()
        except Exception:
            pass

    def shutdown(self):
        """Encerrar subsistemas e liberar recursos de forma segura."""
        g = self.g
        # Parar música
        try:
            import pygame as _pg

            _pg.mixer.music.stop()
        except Exception:
            pass

        # Limpar vídeo (áudio/thread)
        try:
            if hasattr(g, "video_player") and g.video_player:
                g.video_player.cleanup()
        except Exception:
            pass

        # Limpar cache de recursos
        try:
            from internal.resources.cache import ResourceCache

            ResourceCache().clear_cache()
        except Exception:
            pass

        # Finalizar pygame
        try:
            import pygame as _pg

            _pg.quit()
        except Exception:
            pass