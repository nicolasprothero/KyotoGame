import pygame
import os


base_directory = os.path.dirname(os.path.abspath(__file__))

class Weapon(pygame.sprite.Sprite):
    def __init__(self, name:str, rarity:str, type:str, weapon_img_path:str, attack_sound_path:str, attack_sound_level=0.1, x_pos_facingright=5, x_pos_facingleft=30, y_pos=-30, scaling=(30, 90), hitbox_scaling=(100, 120), slash_color=(255, 255, 255), character_icon_scale_factor=1.0, gun_screen_scale_factor=1.0, armory_screen_scale_factor=1.0, cooldown=0.7,  speed_buff=12, jump_buff=-17, extra_sheild=False, knockback=3, extra_jump=False, slow=False):
        super().__init__()
        self.image = pygame.image.load(weapon_img_path)
        self.image = pygame.transform.scale(self.image, scaling) # scale image down
        self.orignial_image = self.image
        self.scaling = scaling
        self.x_pos_facingright = x_pos_facingright
        self.x_pos_facingleft = x_pos_facingleft
        self.y_pos = y_pos
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.name = name
        self.rarity = rarity
        self.type = type
        self.attack_sound_path = attack_sound_path
        self.attack_sound_level = attack_sound_level
        self.hitbox_scaling = hitbox_scaling
        self.character_icon_scale_factor = character_icon_scale_factor
        self.gun_screen_scale_factor = gun_screen_scale_factor
        self.armory_screen_scale_factor = armory_screen_scale_factor
        self.slash_color = slash_color

        self.cooldown = cooldown
        self.speed_buff = speed_buff
        self.jump_buff = jump_buff
        self.extra_shield = extra_sheild
        self.knockback = knockback
        self.extra_jump = extra_jump
        self.slow = slow

        if self.type == "Thrust":
            self.image = pygame.transform.rotate(self.image, -90)

    def get_speed_buff(self):
        return self.speed_buff
    
    def get_jump_buff(self):
        return self.jump_buff
    
    def get_extra_shield(self):
        return self.extra_shield
    
    def get_extra_jump(self):
        return self.extra_jump
    
    def get_slow(self):
        return self.slow
