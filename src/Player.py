import pygame
import numpy as np
import CONSTANTS as C
from Weapons import *
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
    def __init__(self, keyBinds, img, pos, surface):
        self.keyBinds = keyBinds
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (47, 65)) # scale image down 13 by 18
        # convert pos to pair of float
        pos = (float(pos[0]), float(pos[1]))
        surface.blit(self.image, pos)
        self.rect = self.image.get_rect()
        self.pos = np.array(pos) # (x_pos, y_pos)
        self.vel = np.array([0.0, 0.0]) # (x_vel, y_vel)
        
        self.FastFall = False
        self.isOnGround = False
        self.hasDoubleJump = True
        self.hasDash = True
        
        self.facingRight = True
        
        self.mask = pygame.mask.from_surface(self.image)

        # Make the default weapon.
        self.weapon = SlashWeapon('assets/img/sword.png', (40, 60))


    def move(self, pressed_keys):  
        if pressed_keys[self.keyBinds["down"]]:
            self.FastFall = True
            self.vel[1] += 1.5
        if pressed_keys[self.keyBinds["left"]]:
            if self.facingRight:
                self.image = pygame.transform.flip(self.image, True, False)
                self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                self.facingRight = False
            self.vel[0] -= 1.5
        if pressed_keys[self.keyBinds["right"]]:
            if not self.facingRight:
                self.image = pygame.transform.flip(self.image, True, False)
                self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                self.facingRight = True
            self.vel[0] += 1.5


        # reset fast fall if player hits the ground
        if self.pos[1] >= C.SCREEN_HEIGHT - self.image.get_height():
            self.FastFall = False
        

    def updatePos(self):
        self.pos += self.vel
        # deccelerate horizontally
        self.vel[0] *= 0.85
        # add gravity
        self.vel[1] += 0.9
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
            self.hasDoubleJump = True
            self.hasDash = True
            
            
        if self.pos[0] <= 0:
            self.pos[0] = 0
            self.vel[0] = 0
        if self.pos[0] >= C.SCREEN_WIDTH - self.image.get_width():
            self.pos[0] = C.SCREEN_WIDTH - self.image.get_width()
            self.vel[0] = 0

        
    def jump(self):
        if self.isOnGround:
            self.vel[1] -= 15
            self.isOnGround = False
        elif self.hasDoubleJump:
            self.vel[1] = 0
            self.vel[1] -= 15
            self.hasDoubleJump = False
            self.isOnGround = False
            
    def dash(self, pressed_keys):
        if not self.isOnGround and self.hasDash:
            if pressed_keys[self.keyBinds["left"]]:
                self.hasDash = False
                self.vel[0] -= 20
            if pressed_keys[self.keyBinds["right"]]:
                self.hasDash = False
                self.vel[0] += 20
                
    def changeWeapon(self, weapon):
        self.weapon = weapon
