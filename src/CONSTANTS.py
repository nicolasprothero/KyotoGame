# ISSUE: we need to figure out how to make game full screen and kinda scale the level to the screen size
# This is temporary, but we can use this to test collisions
LEVEL_MAP = [
    'XXKBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBJXX',
    'XK4                                  3JX',
    'K4                                    3J',
    'R                                      L',
    'R                                      L',
    'R            1TTTTTTTTTTTT2            L',
    'R            3BBBBBBBBBBBB4            L',
    'H2                                    1G',
    'XH2                                  1GX',
    'XXHTTTT2                        1TTTTGXX',
    'XXXKBBB4                        3BBBJXXX',
    'XKB4                                3BJX',
    'XR           1TT2      1TT2           LX',
    'K4           LXK4      3JXR           3J',
    'R            LXR        LXR            L',
    'R            LXR        LXR            L',
    'R        1TTTGXR        LXHTTT2        L',
    'R        3BBBBB4        3BBBBB4        L',
    'R                                      L',
    'R                                      L',
    'R                                      L',
    'H2    1T2                      1T2    1G',
    'XHTTTTGXR                      LXHTTTTGX',
    'XXXXXXXXR        1TTTT2        LXXXXXXXX',
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