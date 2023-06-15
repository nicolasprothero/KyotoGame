import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(topleft = pos)