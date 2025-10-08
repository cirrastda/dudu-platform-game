from enum import Enum


class GameState(Enum):
    SPLASH = 1  # Tela de splash com logos
    MAIN_MENU = 2  # Menu principal
    PLAYING = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5
    VICTORY = 6  # Nova tela de vitória com troféu
    ENTER_NAME = 7  # Estado para inserir nome no ranking
    SHOW_RANKING = 8  # Estado para mostrar ranking
    CREDITS = 9  # Tela de créditos
    RECORDS = 10  # Tela de recordes
