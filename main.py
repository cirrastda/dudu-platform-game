import pygame
import sys
import math
import os
import json
from enum import Enum
import random
import math
from pathlib import Path

# Inicializar pygame
pygame.init()

# Importar constantes do jogo
from internal.engine.game import Game


if __name__ == "__main__":
    game = Game()
    game.run()
