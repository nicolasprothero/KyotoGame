import pygame
# ISSUE: we need to figure out how to make game full screen and kinda scale the level to the screen size
# This is temporary, but we can use this to test collisions
LEVEL_MAP = [
    'KBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBJ',
    'R  M                         M         L',
    'R                                      L',
    'R                                      L',
    'R                               N      L',
    'R    1TT2                      1TT2    L',
    'R    M  M                        M     L',
    'H2                                    1G',
    'XH2                                  1GX',
    'XXR                                  LXX',
    'XK4           N         N            3JX',
    'K4          1TTTTTTTTTTTTTT2          3J',
    'R                      M               L',
    'R                                      L',
    'R                                      L',
    'R                                      L',
    'R                                      L',
    'R       N                              L',
    'R    1TT2                      1TT2    L',
    'R                                M     L',
    'R                                      L',
    'R                                      L',
    'R                                      L',
    'HT2  N  12              N    12      1TG',
    'XXHTTTTTGHTTTTTTTTTTTTTTTTTTTGHTTTTTTGXX',
]

# T: TOP TILE
# B: BOTTOM TILE
# L: LEFT TILE
# R: RIGHT TILE
# X: MIDDLE TILE
# 1: TOP LEFT
# 2: TOP RIGHT
# 3: BOT LEFT
# 4: BOT RIGHT

# G: LEFT CORNER
# H: RIGHT CORNER
# J: BOTLEFT CORNER
# K: BOTRIGHT CORNER

# N: Grass
# M: Vine

# def get_screen_resolution():

#     if not pygame.get_init():
#         pygame.init()

#     screen_info = pygame.display.Info()
#     resolution = (screen_info.current_w, screen_info.current_h)

#     return resolution

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def setwh(width, height):

    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height

GRAVITY = 15
FRICTION = 0.8
HAND_CORDS = (24, 40)