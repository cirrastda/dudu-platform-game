from enum import Enum


class GameState(Enum):
    SPLASH = 1  # Tela de splash com logos
    TITLE_SCREEN = 2  # Tela de título com cover
    MAIN_MENU = 3  # Menu principal
    PLAYING = 4
    LEVEL_COMPLETE = 5
    GAME_OVER = 6
    VICTORY = 7  # Nova tela de vitória com troféu
    ENTER_NAME = 8  # Estado para inserir nome no ranking
    SHOW_RANKING = 9  # Estado para mostrar ranking
    CREDITS = 10  # Tela de créditos
    RECORDS = 11  # Tela de recordes
