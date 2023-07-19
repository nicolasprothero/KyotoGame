import pygame
import CONSTANTS as C
from Weapons import *
import os
import time
from game import *

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
    def __init__(self, keyBinds, img, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.keyBinds = keyBinds
        self.slash_right_image = pygame.image.load(os.path.join(base_directory, "assets/img/slash.png")).convert_alpha()
        self.slash_left_image = pygame.transform.flip(self.slash_right_image, True, False)
        
        self.OriginalImage = pygame.image.load(img).convert_alpha()
        self.OriginalImage = pygame.transform.scale(self.OriginalImage, (65, 90)) # scale image down; 13 by 18
        
        self.Damagedimage = pygame.image.load(os.path.join(base_directory, "assets/img/characterDamaged.png"))
        self.Damagedimage = pygame.transform.scale(self.Damagedimage, (65, 90))
        
        self.image = self.OriginalImage
        
        self.rect = self.image.get_rect(topleft = pos)
        self.game = game
        self.screen = game.screen

        self.extra_shield = False

        # player movment
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 12
        self.jump_speed = -17
        self.dash_speed = 5
        self.gravity = 0.9
        self.knockback_distance = 3
        
        self.isHit = False
        self.knockbackRight = True
        self.FastFall = False
        self.isOnGround = False
        self.hasDoubleJump = True
        self.hasDash = True
        
        self.facingRight = True
        self.attackRight = True
        self.attacking = False
        self.canAttack = True
        self.attack_start = time.time()
        self.attacking_start = time.time()
        self.invincibility_start = time.time()
        self.damaged_start = time.time()
        
        
        self.isDamaged = False
        self.isInvincible = False
        
        self.mask = pygame.mask.from_surface(self.image)

        # Make the default weapon.
        self.weapon = SlashWeapon(os.path.join(base_directory, 'assets/img/sword.png'), (30,90), )
        self.attack_hitbox = pygame.Rect(self.player.rect.x + self.player.image.get_width(), self.player.rect.y, self.weapon.hitbox_x, self.weapon.hitbox_y)
        self.cooldown = self.weapon.cooldown


    def move(self, pressed_keys): 
        if self.isHit:
            self.knockback(self.knockback_distance, self.knockbackRight)
        elif pressed_keys[self.keyBinds["dash"]] and self.isOnGround == False:
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
            elif pressed_keys[self.keyBinds["right"]]:
                if not self.facingRight:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.OriginalImage = pygame.transform.flip(self.OriginalImage, True, False)
                    self.Damagedimage = pygame.transform.flip(self.Damagedimage, True, False)
                    self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
                    self.facingRight = True
                self.direction.x = 1

        if pressed_keys[self.keyBinds["down"]]:
            self.FastFall = True
            self.gravity = 3

        self.direction.x = round(self.direction.x * 0.85, 2)

    def update(self, pressed_keys):
        self.move(pressed_keys)
        if pressed_keys[self.keyBinds["attack"]] and self.canAttack:
            self.attack()

    
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

    def knockback(self, distance, isRight):
        if isRight:
            self.isHit = False
            self.direction.x = distance
        else:
            self.isHit = False
            self.direction.x = -distance
                
    def changeWeapon(self, weapon):
        self.weapon = weapon

        if self.weapon.get_speed_buff() != 0:
            self.speed += self.weapon.get_speed_buff()
        if self.weapon.get_jump_buff() != 0:
            self.jump_speed += self.weapon.get_jump_buff()
        if self.weapon.get_extra_shield():
            self.extra_shield = True
        if self.weapon.get_knockback_buff() != 0:
            self.knockback_distance += self.weapon.get_knockback_buff()

    def attack(self):
        if self.facingRight:
            self.attackRight = True
        else:
            self.attackRight = False 
        self.attacking = True
        self.canAttack = False
        self.weapon.animate(self.attackRight)
        self.attacking_start = time.time()
        self.attack_start = time.time()

    def handle_attack(self, other_player):
        if self.attacking:
            if self.attackRight:
                attack_hitbox = pygame.Rect(self.rect.x + self.image.get_width(), self.rect.y, self.slash_right_image.get_width(), self.slash_right_image.get_height())
                # pygame.draw.rect(self.screen, (136, 8, 8), attack_hitbox)
                self.screen.blit(self.slash_right_image, (self.rect.x + self.image.get_width(), self.rect.y))
            else:
                attack_hitbox = pygame.Rect(self.rect.x - self.slash_left_image.get_width(), self.rect.y, self.slash_right_image.get_width(), self.slash_right_image.get_height())
                # pygame.draw.rect(self.screen, (136, 8, 8), attack_hitbox)
                self.screen.blit(self.slash_left_image, (self.rect.x - self.slash_left_image.get_width(), self.rect.y))

            if pygame.Rect.colliderect(attack_hitbox, other_player.rect):
                other_player.player_hit(not self.attackRight)
                other_player.isHit = True
                other_player.knockbackRight = not self.attackRight

            if time.time() - self.attacking_start_time > 0.1:
                self.attacking = False
                self.attacking_start_time = time.time()
        else:
            if self.facingRight:
                self.screen.blit(self.weapon.image, (self.rect.x + 5, self.rect.y - 30))
            else:
                self.screen.blit(self.weapon.image, (self.rect.x + 30, self.rect.y - 30))

    # this checks if the player is hit and does logic accordingly
    def player_hit(self, isPlayer1):
        if not self.isInvincible:
            if self.isDamaged:
                pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(base_directory, "assets/sound/Hurt_grunt.wav"))).set_volume(0.2)
                if isPlayer1:
                    self.game.winner = 2
                else:
                    self.game.winner = 1
                self.game.game_over()
            else:
                pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(base_directory, "assets/sound/shieldbreak.mp3"))).set_volume(0.2)
                self.image = self.Damagedimage
                self.isInvincible = True
                self.isDamaged = True
                self.invincibility_start_time = time.time()
                self.damaged_start_time = time.time()

