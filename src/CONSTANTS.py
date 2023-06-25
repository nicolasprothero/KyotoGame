import pygame

LEVEL_MAP = [
    'XXKBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBJXX',
    'XK4    M         M           M      M3JX',
    'K4                                    3J',
    'R                                      L',
    'R              N          N            L',
    'R            1TTTTTTTTTTTT2            L',
    'RN           3BBBBBBBBBBBB4            L',
    'H2             M     M               N1G',
    'XH2   N                         N    1GX',
    'XXHTTTT2                        1TTTTGXX',
    'XXXKBBB4                        3BBBJXXX',
    'XKB4  M         N        N      M   3BJX',
    'XR           1TT2      1TT2         M LX',
    'K4           LXK4      3JXR           3J',
    'R            LXR        LXR            L',
    'R          N LXR        LXR  N         L',
    'R        1TTTGXR        LXHTTT2        L',
    'R        3BBBBB4        3BBBBB4        L',
    'R           M           M     M        L',
    'R                                      L',
    'R                              N       L',
    'H2 N  1T2                      1T2  N 1G',
    'XHTTTTGXR           N          LXHTTTTGX',
    'XXXXXXXXR    N   1TTTT2  N   N LXXXXXXXX',
    'XXXXXXXXHTTTTTTTTGXXXXHTTTTTTTTGXXXXXXXX',
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

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
GRAVITY = 15
FRICTION = 0.8

# create a dictionary to store key presses for player 1 and player 2
key_presses_1 = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "dash": pygame.K_z,
}

key_presses_2 = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "dash": pygame.K_COMMA,
}