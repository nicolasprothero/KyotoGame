import pygame
import math

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_img_path, scaling):
        super().__init__()
        self.image = pygame.image.load(weapon_img_path)
        self.image = pygame.transform.scale(self.image, scaling) # scale image down
        self.rect = self.image.get_rect()

    def attack(self):
        pass
       

class SlashWeapon(Weapon):
    def __init__(self, weapon_img_path, scaling):
        super().__init__(weapon_img_path, scaling)
        self.attack_sound = pygame.mixer.Sound('assets/sound/swoosh.wav')
        self.attack_sound.set_volume(0.3)

    def attack(self, player, surface): #need reach and speed parameter for hitbox
        pygame.mixer.Sound.play(self.attack_sound)
        hitbox = pygame.Rect(player.rect.centerx, player.rect.y, 2*player.rect.width, player.rect.height)
        pygame.draw.rect(surface, (255, 255, 0), hitbox)

class ThrustWeapon(Weapon):
    def __init__(self, weapon_img_path, scaling):
        super().__init__(weapon_img_path, scaling)
        self.attack_sound = pygame.mixer.Sound('assets/sound/toot.mp3')
        self.attack_sound.set_volume(0.3)
        
    def attack(self, player, surface):
        pygame.mixer.Sound.play(self.attack_sound)

    