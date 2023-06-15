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
        self.image = pygame.image.load("assets/img/capy.png")
        self.image = pygame.transform.scale(self.image, (60, 60)) # scale image down
        # convert pos to pair of float
        pos = (float(pos[0]), float(pos[1]))
        surface.blit(self.image, pos)
        self.rect = self.image.get_rect()
        self.pos = np.array(pos) # (x_pos, y_pos)
        self.vel = np.array([0.0, 0.0]) # (x_vel, y_vel)
        self.FastFall = False
        self.isOnGround = False
        self.hasDoubleJump = True

    def move(self, pressed_keys):
        if self.isOnGround:
            if pressed_keys[self.keyBinds["up"]]:
                self.vel[1] -= 10
                self.hasDoubleJump = True
                self.isOnGround = False
        else:
            if pressed_keys[self.keyBinds["up"]] and self.hasDoubleJump == True:
                self.vel[1] = 0
                self.vel[1] -= 10
                self.hasDoubleJump = False
                self.isOnGround = False
  
        if pressed_keys[self.keyBinds["down"]]:
            self.FastFall = True
            self.vel[1] += 2
        if pressed_keys[self.keyBinds["left"]]:
            self.vel[0] -= 2
        if pressed_keys[self.keyBinds["right"]]:
            self.vel[0] += 2


        # reset fast fall if player hits the ground
        if self.pos[1] >= C.SCREEN_HEIGHT - self.image.get_height():
            self.FastFall = False
        

    def updatePos(self):
        self.pos += self.vel
        # deccelerate horizontally
        self.vel[0] *= 0.85
        # add gravity
        self.vel[1] += 1.0
        # fast fall
        if self.FastFall:
            self.vel[1] += 2.0

        # check if player is out of bounds
        # ceiling
        if self.pos[1] <= 0:
            self.pos[1] = 0 + 1
            self.vel[1] = 0
        # floor
        if self.pos[1] >= C.SCREEN_HEIGHT - self.image.get_height():
            self.pos[1] = C.SCREEN_HEIGHT - self.image.get_height()
            self.vel[1] = 0
            self.isOnGround = True
            
            
        if self.pos[0] <= 0:
            self.pos[0] = 0
            self.vel[0] = 0
        if self.pos[0] >= C.SCREEN_WIDTH - self.image.get_width():
            self.pos[0] = C.SCREEN_WIDTH - self.image.get_width()
            self.vel[0] = 0
        


