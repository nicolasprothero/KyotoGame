import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_img_path, scaling, cooldown):
        super().__init__()
        self.image = pygame.image.load(weapon_img_path)
        self.image = pygame.transform.scale(self.image, scaling) # scale image down
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.type = ""
        self.cooldown = cooldown

class SlashWeapon(Weapon):
    def __init__(self, weapon_img_path, scaling, cooldown):
        super().__init__(weapon_img_path, scaling, cooldown)
        self.type = "slash"
class ThrustWeapon(Weapon):
    def __init__(self, weapon_img_path, scaling, cooldown):
        super().__init__(weapon_img_path, scaling, cooldown)
        self.type = "thrust"
    