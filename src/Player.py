import pygame
import CONSTANTS as C
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# define constants for the screen width and height


class Player(pygame.sprite.Sprite):
    def __init__(self, keyBinds):
        super(Player, self).__init__()
        self.keyBinds = keyBinds
        self.surf = pygame.image.load("assets/images/capy.jpeg")
        self.surf = pygame.transform.scale(self.surf, (76, 76)) # scale image down
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys, dt):
        if pressed_keys[self.keyBinds["up"]]:
            self.rect.move_ip(0, -3 * dt)
        if pressed_keys[self.keyBinds["down"]]:
            self.rect.move_ip(0, 2 * dt)
        if pressed_keys[self.keyBinds["left"]]:
            self.rect.move_ip(-2 * dt, 0)
        if pressed_keys[self.keyBinds["right"]]:
            self.rect.move_ip(2 * dt, 0)
         # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > C.SCREEN_WIDTH:
            self.rect.right = C.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= C.SCREEN_HEIGHT:
            self.rect.bottom = C.SCREEN_HEIGHT

    def gravity(self):
        self.rect.move_ip(0,C.GRAVITY) # how fast player falls