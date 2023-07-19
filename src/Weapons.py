import pygame
import os


base_directory = os.path.dirname(os.path.abspath(__file__))

class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, rarity, weapon_img_path, attack_sound_path, attack_sound_level, scaling, hitbox_scaling, cooldown=0.7,  speed_buff=12, jump_buff=-17, extra_sheild=False, knockback_buff=3):
        super().__init__()
        self.image = pygame.image.load(weapon_img_path)
        self.image = pygame.transform.scale(self.image, scaling) # scale image down
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.name = name
        self.rarity = rarity
        self.attack_sound_path = attack_sound_path
        self.attack_sound_level = attack_sound_level
        self.hitbox_scaling = hitbox_scaling

        self.cooldown = cooldown
        self.speed_buff = speed_buff
        self.jump_buff = jump_buff
        self.extra_shield = extra_sheild
        self.knockback_buff = knockback_buff

    def get_speed_buff(self):
        return self.speed_buff
    
    def get_jump_buff(self):
        return self.jump_buff
    
    def get_extra_shield(self):
        return self.extra_shield
    
    def get_knockback_buff(self):
        return self.knockback_buff


class SlashWeapon(Weapon):
    def __init__(self, name, rarity, weapon_img_path, attack_sound_path, attack_sound_level, scaling, hitbox_scaling, cooldown=0.7,  speed_buff=12, jump_buff=-17, extra_sheild=False, knockback_buff=3):
        super().__init__(name, rarity, weapon_img_path, attack_sound_path, attack_sound_level, scaling, hitbox_scaling, cooldown, speed_buff, jump_buff, extra_sheild, knockback_buff)
        
        

class ThrustWeapon(Weapon):
    def __init__(self, name, rarity, weapon_img_path, attack_sound_path, attack_sound_level, scaling, hitbox_scaling, cooldown=0.7,  speed_buff=12, jump_buff=-17, extra_sheild=False, knockback_buff=3):
        super().__init__(name, rarity, weapon_img_path, attack_sound_path, attack_sound_level, scaling, hitbox_scaling, cooldown,  speed_buff, jump_buff, extra_sheild, knockback_buff)

    