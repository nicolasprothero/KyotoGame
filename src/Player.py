import pygame
import CONSTANTS as C
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# define constants for the screen width and height


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load("capy.jpeg")
        self.surf = pygame.transform.scale(self.surf, (50, 50)) # scale image down
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys, dt):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3 * dt)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2 * dt)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2 * dt, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2 * dt, 0)
         # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > C.SCREEN_WIDTH:
            self.rect.right = C.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= C.SCREEN_HEIGHT:
            self.rect.bottom = C.SCREEN_HEIGHT
    def gravity(self):
        self.rect.move_ip(0,20) # how fast player falls