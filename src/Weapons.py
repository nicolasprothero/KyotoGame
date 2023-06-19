import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_img_path):
        super().__init__()
        self.image = pygame.image.load(weapon_img_path)
        self.image = pygame.transform.scale(self.image, (60, 60)) # scale image down
        self.rect = self.image.get_rect()

    def attack(self):
        pass
       
class SlashWeapon(Weapon):
    def __init__(self, weapon_img_path):
        super().__init__(weapon_img_path)
        self.image = pygame.image.load(weapon_img_path)
        self.rect = self.image.get_rect()
    
    def attack(self):
        pygame.mixer.Sound.play('assets/sound/slash.wav')

class ThrustWeapon(Weapon):
    def __init__(self, weapon_img_path):
        super().__init__(weapon_img_path)
        self.image = pygame.image.load(weapon_img_path)
        self.rect = self.image.get_rect()
    
    def attack(self):
        pygame.mixer.Sound.play('assets/sound/toot.mp3')
