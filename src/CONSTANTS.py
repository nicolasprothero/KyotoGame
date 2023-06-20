# ISSUE: we need to figure out how to make game full screen and kinda scale the level to the screen size
# This is temporary, but we can use this to test collisions
LEVEL_MAP = [
    'KBBBBBBBBBBBBBBBBBBBBBBBBBBBBJ',
    'R  M               M         L',
    'R                            L',
    'R                            L',
    'R                     N      L',
    'R    1TT2            1TT2    L',
    'R    M  M              M     L',
    'H2                          1G',
    'XH2                        1GX',
    'XXR   9                9   LXX',
    'XK4   0     N   N      0   3JX',
    'K4         1TTTTTT2         3J',
    'R           M                L',
    'R       N                    L',
    'R    1TT2            1TT2    L',
    'R                      M     L',
    'R                            L',
    'R                            L',
    'HT2  N  12     N    12     1TG',
    'XXHTTTTTGHTTTTTTTTTTGHTTTTTGXX',
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
# 9: TorchTop
# 0: TorchBot

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRAVITY = 15
FRICTION = 0.8
HAND_CORDS = (24, 40)