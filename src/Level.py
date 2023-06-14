import pygame
from CONSTANTS import *
from Tile import Tile
from Player import Player

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        
    def setup_level(self, layout):
        TILE_SIZE = min(SCREEN_WIDTH // len(LEVEL_MAP[0]), SCREEN_HEIGHT // len(LEVEL_MAP))
        self.Tile = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = Tile((x,y), TILE_SIZE)
                    self.Tile.add(tile)


    def run(self):
        self.Tile.draw(self.display_surface)