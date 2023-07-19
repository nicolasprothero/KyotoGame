import pygame
import os


base_directory = os.path.dirname(os.path.abspath(__file__))

class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, screen, weapon_img_path, attack_sound_path, scaling, cooldown=0.7,  speed_buff=0, jump_buff=0, extra_sheild=False, knockback_buff=0):
        super().__init__()
        self.image = pygame.image.load(weapon_img_path)
        self.image = pygame.transform.scale(self.image, scaling) # scale image down
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.screen = screen
        self.name = name
        self.attack_sound = pygame.mixer.Sound(os.path.join(base_directory, attack_sound_path))
        self.attack_sound.set_volume(0.1)

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
    def __init__(self, name, screen, weapon_img_path, attack_sound_path, scaling, cooldown=0.7,  speed_buff=0, jump_buff=0, extra_sheild=False, knockback_buff=0):
        super().__init__(name, screen, weapon_img_path, attack_sound_path, scaling, cooldown,  speed_buff, jump_buff, extra_sheild, knockback_buff)
        self.slash_right_image = pygame.image.load(os.path.join(base_directory, "assets/img/slash.png")).convert_alpha()
        self.slash_left_image = pygame.transform.flip(self.slash_right_image, True, False)
        self.hitbox_x = self.slash_left_image.get_width()
        self.hitbox_y = self.slash_left_image.get_height()
    
    def animate(self, attackRight, player):
        if attackRight:
            self.screen.blit(self.slash_right_image, (player.rect.x + player.image.get_width(), player.rect.y))
        else:
            self.screen.blit(self.slash_left_image, (player.rect.x + player.image.get_width(), player.rect.y))
        pygame.mixer.Sound.play(self.attack_sound)
        

class ThrustWeapon(Weapon):
    def __init__(self, name, screen, weapon_img_path, attack_sound_path, scaling, cooldown=0.7,  speed_buff=0, jump_buff=0, extra_sheild=False, knockback_buff=0):
        super().__init__(name, screen, weapon_img_path, attack_sound_path, scaling, cooldown,  speed_buff, jump_buff, extra_sheild, knockback_buff)

    def animate(self, attackRight):
        pass
    