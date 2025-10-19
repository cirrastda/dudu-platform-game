from enum import Enum


class GameState(Enum):
    SPLASH = 1  # Tela de splash com logos
    TITLE_SCREEN = 2  # Tela de título com cover
    OPENING_VIDEO = 3  # Vídeo de abertura
    MAIN_MENU = 4  # Menu principal
    PLAYING = 5
    LEVEL_COMPLETE = 6
    GAME_OVER = 7
    VICTORY = 8  # Nova tela de vitória com troféu
    ENTER_NAME = 9  # Estado para inserir nome no ranking
    SHOW_RANKING = 10  # Estado para mostrar ranking
    CREDITS = 11  # Tela de créditos
    RECORDS = 12  # Tela de recordes
    ENDING_VIDEO = 13  # Vídeo de ending após captura do boss
    FIM_SCREEN = 14  # Tela de "FIM" após o vídeo de ending
