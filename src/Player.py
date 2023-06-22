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
    def __init__(self, keyBinds, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.keyBinds = keyBinds
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 90)) # scale image down; 13 by 18
        self.rect = self.image.get_rect(topleft = pos)

        # player movment
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 10
        self.jump_speed = -20
        self.dash_speed = 5
        self.gravity = 0.9


        
        self.FastFall = False
        self.isOnGround = False
        self.hasDoubleJump = True
        self.hasDash = True
        
        self.facingRight = True
        
        self.mask = pygame.mask.from_surface(self.image)

        # Make the default weapon.
        self.weapon = SlashWeapon('assets/img/sword.png', (40, 60))


    def move(self):  
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[self.keyBinds["left"]]:
            if self.facingRight:
                self.image = pygame.transform.flip(self.image, True, False)
                self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                self.facingRight = False
            self.direction.x = -1 
        elif pressed_keys[self.keyBinds["right"]]:
            if not self.facingRight:
                self.image = pygame.transform.flip(self.image, True, False)
                self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                self.facingRight = True
            self.direction.x = 1
        else:
            self.direction.x = round(self.direction.x * 0.85, 2)

        if pressed_keys[self.keyBinds["down"]]:
            self.FastFall = True
            self.gravity = 3


    def update(self):
        self.move()

    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        
    def jump(self):
        if self.isOnGround:
            self.direction.y = self.jump_speed
            self.isOnGround = False
        elif self.hasDoubleJump:
            self.direction.y = self.jump_speed
            self.hasDoubleJump = False
        self.FastFall = False
        self.gravity = 0.9
        
            
    def dash(self):
        if not self.isOnGround and self.hasDash:
            if not self.facingRight:
                self.hasDash = False
                self.direction.x = -self.dash_speed
            if self.facingRight:
                self.hasDash = False
                self.direction.x = self.dash_speed
                
    def changeWeapon(self, weapon):
        self.weapon = weapon
