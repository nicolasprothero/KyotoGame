import pygame
import src.CONSTANTS as C
from src.CONSTANTS import *
import os

base_directory = os.path.dirname(os.path.abspath(__file__))

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        