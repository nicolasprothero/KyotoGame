import pygame
import CONSTANTS as C
from Weapons import *
import os
import copy

base_directory = os.path.dirname(os.path.abspath(__file__))
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self, keyBinds, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.keyBinds = keyBinds
        self.slash_right_image = pygame.image.load(os.path.join(base_directory, "assets/img/slash.png")).convert_alpha()
        self.slash_left_image = pygame.transform.flip(self.slash_right_image, True, False)
        self.slash_right_rect = self.slash_right_image.get_rect()
        self.slash_left_rect = self.slash_left_image.get_rect()
        
        self.OriginalImage = pygame.image.load(img).convert_alpha()
        self.OriginalImage = pygame.transform.scale(self.OriginalImage, (65, 90)) # scale image down; 13 by 18
        
        self.Damagedimage = pygame.image.load(os.path.join(base_directory, "assets/img/characterDamaged.png"))
        self.Damagedimage = pygame.transform.scale(self.Damagedimage, (65, 90))
        
        self.image = self.OriginalImage
        
        self.rect = self.image.get_rect(topleft = pos)

        # player movment
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 12
        self.original_speed = self.speed
        self.jump_speed = -17
        self.dash_speed = 5
        self.gravity = 0.9

        self.isHit = False
        self.knockbackRight = True
        self.FastFall = False
        self.isOnGround = False
        self.hasDoubleJump = True
        self.hasDash = True
        self.extra_shield = False
        self.extra_jump = False
        
        self.facingRight = True

        self.attackRight = True
        self.attacking = False
        self.canAttack = True
        
        self.isDamaged = False
        self.isInvincible = False
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.isRunning = False

        # Make the default weapon.

        self.weapon = copy.copy(C.weapon_dict["shard"])

        self.slash_right_image = pygame.transform.scale(self.slash_right_image, self.weapon.hitbox_scaling)
        self.slash_left_image = pygame.transform.scale(self.slash_left_image, self.weapon.hitbox_scaling)


    def move(self, pressed_keys): 
        if pressed_keys[self.keyBinds["dash"]] and self.isOnGround == False:
            if self.hasDash:
                self.dash()
        elif abs(self.direction.x) <= 1:
            if pressed_keys[self.keyBinds["left"]]:
                if self.facingRight:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.OriginalImage = pygame.transform.flip(self.OriginalImage, True, False)
                    self.Damagedimage = pygame.transform.flip(self.Damagedimage, True, False)
                    self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                    self.facingRight = False
                self.direction.x = -1 
                self.isRunning = True
            elif pressed_keys[self.keyBinds["right"]]:
                if not self.facingRight:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.OriginalImage = pygame.transform.flip(self.OriginalImage, True, False)
                    self.Damagedimage = pygame.transform.flip(self.Damagedimage, True, False)
                    self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                    self.facingRight = True
                self.direction.x = 1
                self.isRunning = True
            else:
                self.isRunning = False

        if pressed_keys[self.keyBinds["down"]]:
            self.FastFall = True
            self.gravity = 3

        self.direction.x = round(self.direction.x * 0.85, 3)

    def update(self, pressed_keys):
        self.move(pressed_keys)

    
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
        elif self.extra_jump:
            self.direction.y = self.jump_speed
            self.extra_jump = False
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

    def knockback(self, distance, isRight):
        if isRight:
            self.isHit = False
            self.direction.x = distance
        else:
            self.isHit = False
            self.direction.x = -distance
                
    def changeWeapon(self, weapon):
        self.weapon = copy.copy(weapon)
        self.slash_right_image = pygame.transform.scale(self.slash_right_image, self.weapon.hitbox_scaling)
        self.slash_left_image = pygame.transform.scale(self.slash_left_image, self.weapon.hitbox_scaling)

        self.slash_right_rect = self.slash_right_image.get_rect()
        self.slash_left_rect = self.slash_left_image.get_rect()

        self.slash_right_image.fill(self.weapon.slash_color, special_flags=pygame.BLEND_MULT)
        self.slash_left_image.fill(self.weapon.slash_color, special_flags=pygame.BLEND_MULT)

        if self.weapon.get_speed_buff() != 0:
            self.speed = self.weapon.get_speed_buff()
            self.original_speed = self.speed
        if self.weapon.get_jump_buff() != 0:
            self.jump_speed = self.weapon.get_jump_buff()
        if self.weapon.get_extra_shield():
            self.extra_shield = True
        if self.weapon.get_extra_jump():
            self.extra_jump = True            
        
