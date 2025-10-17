import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.core.window import Window


class OpeningApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        root = FloatLayout()

        # Video de abertura usando Kivy (com ffpyplayer)
        self.video = Video(
            source="videos/opening.mp4",
            state="play",
            options={"eos": "stop"},
        )
        self.video.allow_stretch = True
        self.video.keep_ratio = True
        self.video.size = Window.size
        self.video.pos = (0, 0)
        self.video.bind(on_eos=self.on_video_end)
        root.add_widget(self.video)
        return root

    def on_video_end(self, *args):
        # Finaliza app Kivy e segue para o jogo
        try:
            self.stop()
        except Exception:
            pass


if __name__ == "__main__":
    # Executa abertura com Kivy e, ao terminar, inicia o jogo (pygame)
    try:
        OpeningApp().run()
    except Exception:
        # Em caso de erro ao reproduzir o vídeo, continuar para o jogo
        pass

    import pygame
    from internal.engine import game as game_module
    from internal.engine.game import Game

    # Sinaliza para o jogo ignorar o vídeo de abertura (já exibido via Kivy)
    try:
        game_module.ENV_CONFIG["skip-opening-video"] = "1"
    except Exception:
        pass

    pygame.init()
    Game().run()