import pygame
from src.CONSTANTS import *
from src.Tile import Tile
import os

base_directory = os.path.dirname(os.path.abspath(__file__))


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
        self.setup_level(level_data)
        
    def setup_level(self, layout):
       
        TILE_SIZE = min(SCREEN_WIDTH // len(LEVEL_MAP[0]), SCREEN_HEIGHT // len(LEVEL_MAP))
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/middle_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'T':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/top_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'B':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/bot_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'L':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/left_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'R':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/right_tile.png'))
                    self.tile_group.add(tile)
                elif col == '1':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/topleft_tile.png'))
                    self.tile_group.add(tile)
                elif col == '2':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/topright_tile.png'))
                    self.tile_group.add(tile)
                elif col == '3':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/botleft_tile.png'))
                    self.tile_group.add(tile)
                elif col == '4':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/botright_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'G':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/leftcorner_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'H':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/rightcorner_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'J':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/botleftcorner_tile.png'))
                    self.tile_group.add(tile)
                elif col == 'K':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/botrightcorner_tile.png'))
                    self.tile_group.add(tile)
                elif col == '7':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/grass_tile.png'))
                    self.no_collide_group.add(tile)
                elif col == '8':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/vine_tile.png'))
                    self.no_collide_group.add(tile)
                elif col == '9':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/vine_two.png'))
                    self.no_collide_group.add(tile)
                elif col == '#':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/brick.png'))
                    self.no_collide_group.add(tile)
                elif col == '$':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/brick_two.png'))
                    self.no_collide_group.add(tile)
                elif col == '<':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/leaf_left.png'))
                    self.no_collide_group.add(tile)
                elif col == '>':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/leaf_right.png'))
                    self.no_collide_group.add(tile)
                elif col == 'Z':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/rock.png'))
                    self.no_collide_group.add(tile)
                elif col == 'V':
                    tile = Tile((x,y), TILE_SIZE, os.path.join(base_directory, 'assets/img/tileset/rock_leaf.png'))
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

# 7: Grass
# 8: Vine
# 9: Vine 2

# #: Brick One
# $: Brick Two

# <: Leaf Left 
# >: Leaf Right 

# Z: Inside Rock 
# V: Inside Leaf 

    def run(self):
        self.display_surface.blit(self.background_image, (0, 0))
        # Tiles
        self.tile_group.draw(self.display_surface)
        self.no_collide_group.draw(self.display_surface)