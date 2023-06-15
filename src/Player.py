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

class Player(pygame.sprite.Sprite):
    def __init__(self, keyBinds, pos, surface):
        self.keyBinds = keyBinds
        self.image = pygame.image.load("assets/images/capy.jpeg")
        self.image = pygame.transform.scale(self.image, (76, 76)) # scale image down
        # convert pos to pair of float
        pos = (float(pos[0]), float(pos[1]))
        surface.blit(self.image, pos)
        self.rect = self.image.get_rect()
        self.pos = np.array(pos) # (x_pos, y_pos)
        self.vel = np.array([0.0, 0.0]) # (x_vel, y_vel)

    def move(self, pressed_keys):

        # only jump if on the ground
        if self.pos[1] >= C.SCREEN_HEIGHT - self.image.get_height():
            if pressed_keys[self.keyBinds["up"]]:
                self.vel[1] -= 15
        if pressed_keys[self.keyBinds["down"]]:
            self.vel[1] += 1
        if pressed_keys[self.keyBinds["left"]]:
            self.vel[0] -= 1
        if pressed_keys[self.keyBinds["right"]]:
            self.vel[0] += 1

    def updatePos(self):
        self.pos += self.vel
        # deccelerate horizontally
        self.vel[0] *= 0.90
        # add gravity
        self.vel[1] += 0.7
        # check if player is out of bounds

        # ceiling
        if self.pos[1] <= 0:
            self.pos[1] = 0 + 1
            self.vel[1] = 0
        # floor
        if self.pos[1] >= C.SCREEN_HEIGHT - self.image.get_height():
            self.pos[1] = C.SCREEN_HEIGHT - self.image.get_height()
            self.vel[1] = 0
            
        if self.pos[0] <= 0:
            self.pos[0] = 0
            self.vel[0] = 0
        if self.pos[0] >= C.SCREEN_WIDTH - self.image.get_width():
            self.pos[0] = C.SCREEN_WIDTH - self.image.get_width()
            self.vel[0] = 0
        


