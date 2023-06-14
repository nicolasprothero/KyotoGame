import pygame
import numpy as np
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
    def __init__(self, keyBinds, x, y):
        # velocity and acceleration are vectors
        self.vel = np.array[0.0, 0.0]
        self.accel = np.array[0.0, 0.0]
        self.pos = np.array[x, y]
        self.gravity = np.array[0.0, 0.5] # set value
        super(Player, self).__init__()
        self.keyBinds = keyBinds
        self.surf = pygame.image.load("src/capy.jpeg")
        self.surf = pygame.transform.scale(self.surf, (50, 50)) # scale image down
        self.rect = self.surf.get_rect()

    def move_up(self, dt):
        self.vel += np.array([0, -1])
        self.accel += np.array([0, -1])

class Player(pygame.sprite.Sprite):
    def __init__(self, keyBinds):
        super(Player, self).__init__()
        self.keyBinds = keyBinds
        self.surf = pygame.image.load("src/capy.jpeg")
        self.surf = pygame.transform.scale(self.surf, (50, 50)) # scale image down
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys, dt):
        if pressed_keys[self.keyBinds["up"]]:
            self.rect.move_ip(0, -3 * dt)
        if pressed_keys[self.keyBinds["down"]]:
            self.rect.move_ip(0, 2 * dt)
        if pressed_keys[self.keyBinds["left"]]:
            self.rect.move_ip(-2 * dt, 0)
        if pressed_keys[self.keyBinds["right"]]:
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
        self.rect.move_ip(0,C.GRAVITY) # how fast player falls