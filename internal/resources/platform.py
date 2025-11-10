import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Platform:
    _id_counter = 0  # Contador de ID para plataformas

    def __init__(self, x, y, width, height, texture=None):
        Platform._id_counter += 1
        self.id = Platform._id_counter
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.texture = texture

    def draw(self, screen):
        if self.texture:
            # Obter dimensões da textura original
            texture_width = self.texture.get_width()
            texture_height = self.texture.get_height()

            # Calcular quantas repetições cabem na plataforma
            tiles_x = self.width // texture_width
            tiles_y = self.height // texture_height

            # Desenhar os azulejos completos
            for row in range(tiles_y):
                for col in range(tiles_x):
                    x_pos = self.x + (col * texture_width)
                    y_pos = self.y + (row * texture_height)
                    screen.blit(self.texture, (x_pos, y_pos))

            # Desenhar azulejos parciais nas bordas direita e inferior
            remainder_x = self.width % texture_width
            remainder_y = self.height % texture_height

            # Borda direita
            if remainder_x > 0:
                for row in range(tiles_y):
                    x_pos = self.x + (tiles_x * texture_width)
                    y_pos = self.y + (row * texture_height)
                    partial_texture = self.texture.subsurface(
                        0, 0, remainder_x, texture_height
                    )
                    screen.blit(partial_texture, (x_pos, y_pos))

            # Borda inferior
            if remainder_y > 0:
                for col in range(tiles_x):
                    x_pos = self.x + (col * texture_width)
                    y_pos = self.y + (tiles_y * texture_height)
                    partial_texture = self.texture.subsurface(
                        0, 0, texture_width, remainder_y
                    )
                    screen.blit(partial_texture, (x_pos, y_pos))

            # Canto inferior direito
            if remainder_x > 0 and remainder_y > 0:
                x_pos = self.x + (tiles_x * texture_width)
                y_pos = self.y + (tiles_y * texture_height)
                corner_texture = self.texture.subsurface(0, 0, remainder_x, remainder_y)
                screen.blit(corner_texture, (x_pos, y_pos))
        else:
            # Fallback para cor sólida
            pygame.draw.rect(screen, BROWN, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

    def get_platform_texture(game, level):
        if level <= 30:
            return game.image.platform_texture
        elif level <= 40:
            return game.image.platform_texture_city
