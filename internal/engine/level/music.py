class LevelMusic:
    level_music_list = {}

    def __init__(self):
        self.level_music_list = {}

    def load_level_music_list(self):
        """Carregar a lista de músicas do nível"""
        self.level_music_list = {
            1: "musicas/fundo1.mp3",  # Primeira fase
            2: "musicas/fundo2.mp3",  # Segunda fase
            3: "musicas/fundo1.mp3",  # Terceira fase (também fundo1)
        }
        # Criar rodízio para fases 4-20 usando fundo2, fundo3 e fundo4
        background_music = [
            "musicas/fundo2.mp3",
            "musicas/fundo3.mp3",
            "musicas/fundo4.mp3",
        ]
        for level in range(4, 21):  # Fases 4 a 20
            # Usar módulo para criar rodízio: fase 4 = índice 0, fase 5 = índice 1, etc.
            music_index = (level - 4) % len(background_music)
            self.level_music_list[level] = background_music[music_index]

        background_music_third_world = [
            "musicas/fundo6.mp3",
            "musicas/fundo5.mp3",
        ]
        for level in range(21, 31):  # Fases 21 a 30
            music_file = background_music_third_world[level % 2]
            self.level_music_list[level] = music_file

        # Configurar trilhas sonoras para níveis 31-40
        # Primeiras 4 fases (31-34): alternar entre night1.mp3 e night2.mp3
        background_music_fourth_world_part1 = [
            "musicas/night1.mp3",
            "musicas/night2.mp3",
        ]
        for level in range(31, 35):  # Fases 31 a 34
            music_index = (level - 31) % len(background_music_fourth_world_part1)
            self.level_music_list[level] = background_music_fourth_world_part1[music_index]

        # Últimas 6 fases (35-40): alternar entre night3.mp3 e night4.mp3
        background_music_fourth_world_part2 = [
            "musicas/night3.mp3",
            "musicas/night4.mp3",
        ]
        for level in range(35, 41):  # Fases 35 a 40
            music_index = (level - 35) % len(background_music_fourth_world_part2)
            self.level_music_list[level] = background_music_fourth_world_part2[music_index]

        return self.level_music_list

    def get_level_music(self, level):
        """Retorna a música do nível"""
        return self.level_music_list.get(level, None)
