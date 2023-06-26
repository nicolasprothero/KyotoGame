import pygame
import src.CONSTANTS as C
from src.CONSTANTS import *
from src.Tile import Tile
from src.Player import Player

"""
Made a no_collide_group for non collidable tiles.
"""

class Level:
    def __init__(self, level_data, surface, background_img_path):
        self.display_surface = surface
        self.background_image = pygame.image.load(background_img_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tile_group = pygame.sprite.Group() # collidable tiles
        self.no_collide_group = pygame.sprite.Group() # non-collidable tiles
        self.players = pygame.sprite.Group()
        self.setup_level(level_data)
        
    def setup_level(self, layout):
        TILE_SIZE = min(C.SCREEN_WIDTH // len(LEVEL_MAP[0]), C.SCREEN_HEIGHT // len(LEVEL_MAP))
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/middle_tile.png')
                    self.tile_group.add(tile)
                elif col == 'T':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/top_tile.png')
                    self.tile_group.add(tile)
                elif col == 'B':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/bot_tile.png')
                    self.tile_group.add(tile)
                elif col == 'L':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/left_tile.png')
                    self.tile_group.add(tile)
                elif col == 'R':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/right_tile.png')
                    self.tile_group.add(tile)
                elif col == '1':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/topleft_tile.png')
                    self.tile_group.add(tile)
                elif col == '2':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/topright_tile.png')
                    self.tile_group.add(tile)
                elif col == '3':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/botleft_tile.png')
                    self.tile_group.add(tile)
                elif col == '4':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/botright_tile.png')
                    self.tile_group.add(tile)
                elif col == 'G':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/leftcorner_tile.png')
                    self.tile_group.add(tile)
                elif col == 'H':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/rightcorner_tile.png')
                    self.tile_group.add(tile)
                elif col == 'J':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/botleftcorner_tile.png')
                    self.tile_group.add(tile)
                elif col == 'K':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/botrightcorner_tile.png')
                    self.tile_group.add(tile)
                elif col == 'N':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/grass_tile.png')
                    self.no_collide_group.add(tile)
                elif col == 'M':
                    tile = Tile((x,y), TILE_SIZE, 'assets/img/tileset/vine_tile.png')
                    self.no_collide_group.add(tile)
                # T: TOP TILE
                # B: BOTTOM TILE
                # L: LEFT TILE
                # R: RIGHT TILE
                # X: MIDDLE TILE

                # 1: TOP LEFT
                # 2: TOP RIGHT
                # 3: BOT LEFT
                # 4: BOT RIGHT

                # G: LEFT CORNER
                # H: RIGHT CORNER
                # J: BOTLEFT CORNER
                # K: BOTRIGHT CORNER

                # N: Grass
                # M: Vine

    def run(self):
        self.display_surface.blit(self.background_image, (0, 0))
        # Tiles
        self.tile_group.draw(self.display_surface)
        self.no_collide_group.draw(self.display_surface)