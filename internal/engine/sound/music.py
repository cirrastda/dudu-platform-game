import os
import pygame
from internal.utils.functions import resource_path
from internal.engine.level.music import LevelMusic


class Music:
    INTRO = "intro"

    def start(self, game):
        game.current_music = None
        game.music_volume = 0.7

        # Volumes individuais para cada música (equalização)
        game.music_volumes = {
            self.INTRO: 0.6,  # Música do menu - geralmente mais alta
            "musicas/fundo1.mp3": 0.7,  # Volume padrão
            "musicas/fundo2.mp3": 0.8,  # Geralmente mais baixa
            "musicas/fundo3.mp3": 0.7,  # Volume padrão
            "musicas/fundo4.mp3": 0.6,  # Geralmente mais alta
        }
        self.load_music(game)

    def load_music(self, game):
        """Carregar todas as músicas do jogo"""
        game.music_files = {
            self.INTRO: "musicas/intro.mp3",  # Música do menu
        }

        level_music = LevelMusic()
        level_music_list = level_music.load_level_music_list()
        if not level_music_list:
            print("Erro: Nenhuma música de nível foi carregada.")
            return

        for level, music_file in level_music_list.items():
            game.music_files[level] = music_file

        # Verificar se os arquivos de música existem
        for level, music_file in game.music_files.items():
            if not self.check_music_exists(music_file):
                continue

    def check_music_exists(self, music_file):
        """Verificar se o arquivo de música existe"""
        full_path = resource_path(music_file)
        if not os.path.exists(full_path):
            print(f"Aviso: Arquivo de música não encontrado: {music_file}")
            return False
        return full_path

    def play_menu_music(self, game):
        """Tocar a música do menu"""
        music_file = game.music_files[self.INTRO]
        full_music_path = self.check_music_exists(music_file)
        if not full_music_path:
            return

        try:
            volume = game.music_volumes.get(self.INTRO, game.music_volume)
            self.play(game, music_file, full_music_path, volume)

            print(f"Tocando música do menu: {music_file} (volume: {volume})")
        except pygame.error as e:
            print(f"Erro ao carregar música do menu {music_file}: {e}")

    def play_level_music(self, game, level):
        """Tocar a música correspondente ao nível"""

        if level in game.music_files:
            music_file = game.music_files[level]
        else:
            print(f"Música não encontrada para o nível {level}")
            return

        if not self.check_music_exists(music_file):
            return

        full_music_path = resource_path(music_file)

        try:
            volume = game.music_volumes.get(music_file, game.music_volume)
            self.play(game, music_file, full_music_path, volume)

            print(f"Tocando música do nível {level}: {music_file} (volume: {volume})")
        except pygame.error as e:
            print(f"Erro ao carregar música {music_file}: {e}")

    def play(self, game, music_file, full_music_path, volume):
        # Parar música atual se estiver tocando
        pygame.mixer.music.stop()
        # Carregar e tocar música
        pygame.mixer.music.load(full_music_path)
        # Usar volume específico para esta música
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # -1 para loop infinito
        game.current_music = music_file
