import pygame
import os
from Weapons import *
import json

LEVEL_MAP = [
    'XXKBBBBBBBBBBBBJXXXXXXZXKBBBBBBBBBBBBJXX',
    'VK4>           LVXXXXXXXR       89   3JX',
    'K4             3BBBBBBBB4#$          <3J',
    'R>                89$#####$            L',
    'R                    $#$               L',
    'RN                       $             L',
    'H2                           $ #$ #  N1G',
    'XH2 7                         ###### 1GX',
    'XXHTTTT2                     $##1TTTTGXX',
    'XXZKBBB4>     7         7     #$3BBBJZXX',
    'XKB4 89      1TTT2    1TTT2    $####3BJX',
    'XR           LXKB4    3BJXR         ##LX',
    'K4           LX4        LXR       $  $3J',
    'R$           LXR        LXR            L',
    'R#$          LXR        LXR            L',
    'R##       1TTGXR        LXHTT2>        L',
    'R#$       3BBBB4   12   3BBBB4         L',
    'R#$        89      34       8          L',
    'R##$ $                                 L',
    'R### #$                                L',
    'H2####1T2                      1T2    1G',
    'XHTTTTGXR            7        <LXHTTTTGX',
    'XXZXXXXVR   7    1TTTT2    7   LXXXZVXXX',
    'XXXXXZXXHTTTTTTTTGXVXXHTTTTTTTTGZXXXXVXX',
]

LEVEL_MAP1 = [
    'XXKBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBJXX',
    'XK4      8     89     8    89        3JX',
    'K4                                    3J',
    'R>                                     L',
    'R                                     <L',
    'R                                      L',
    'R                                      L',
    'RN                       $             L',
    'H2                           $ #$ #  N1G',
    'XH2 7                         ###### 1GX',
    'XXHTTTT2                     $##1TTTTGXX',
    'XXZKBBB4>                     #$3BBBJZXX',
    'XXK4                              893JXX',
    'XXRM                                 LXX',
    'XK4>            7    7     7         3JX',
    'K4      $   1TTTTTTTTTTTTTT2          3J',
    'RM    $     LXXXXXXXXXXXXXXR           L',
    'R  $ #$    <LXXXXXXXXXXXXXXR           L',
    'R> ##$      LXXXXXXXXXXXXXXR           L',
    'R#$##$      LXXXXXXXXXXXXXXR          <L',
    'R###$       LXXXXXXXXXXXXXXR           L',
    'R##$        LXXXXXXXXXXXXXXR           L',
    'R>#$        LXXXXXXXXXXXXXXR           L',
    'R           LXXXXXXXXXXXXXXR>          L',
    'R           LXXXXXXXXXXXXXXR           L',
]

LEVEL_MAP_ERROR = [
    'XXXXXXXXXKBBBBBJXXXXXXXXKBBBBBJXXXXXXXXX',
    'XXXXXXKBB4     LXXXXXXXXR  M  3BJXXXXXXX',
    'XXXKBB4        3BBBBBBBB4       3BBJXXXX',
    'XXK4 M                M            LXXXX',
    'XXR                                3JXXX',
    'XXR                                 LXXX',
    'XXR                                 3JXX',
    'XK4                                  LXX',
    'XR                                   LXX',
    'XR                                   LXX',
    'XR                                   3JX',
    'XR                                    LX',
    'XR                                    LX',
    'XR                                    LX',
    'K4                                    LX',
    'R                                     3J',
    'R      NN N  NN    NN N NN   NNN       L',
    'R      1TTTTTTTTTTTTTTTTTTTTTTTT2      L',
    'R      LXXXXXXXXXXXXXXXXXXXXXXXXR      L',
    'R      3BBBBBBBBBBBBBBBBBBBBBBBB4      L',
    'R        M           M     M   M       L',
    'R                                      L',
    'R                                      L',
    'R                                      L',
    'R                                      L',
]

LEVEL_MAP2 = [
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '     7      7         77 7     7   7    ',
    '  1TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT2  ',
    '  LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXR  ',
    ' <LXXXXXXZXXXXXXXXXXXXXZXXXXXZXXXXXZXR  ',
    '  LXXXXXXXXXZXXXXXXXXXXXXXXXXXZXXXXXXR  ',
    '  LXXXXZXXXXXXXXXZXXXXXXXXXXXXXXXXXXXR> ',
    '  LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXZXXXXR  ',
    '  LXXXXXXXXXXZXXXXXXXXXXXXXZXXXXXXXXXR  ',
    '  LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXR  ',
]

LEVEL_MAP3 = [
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '         7           7      7           ',
    '       1TTTTTTTTTTTTTTTTTTTTTTTT2       ',
    '       LXXXXXXXXXXXXXXXXXXXXXXXXR       ',
    '       3BBBBBBBBBBBBBBBBBBBBBBBB4       ',
    '             8          89     8        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
]

LEVEL_MAP4 = [
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                    7   ',
    '                                <1TT2   ',
    '                                 LVXR   ',
    '                                <LXXR   ',
    '   7                             LXVR   ',
    '  1TT2                           LXXR>  ',
    '  LXVR         7   7    7 7      LXXR   ',
    '  LXVR>     1TTTTTTTTTTTTTT2     LXXR   ',
    '  LXXR      LXXXXXXXXXXXXVXR     LVXR   ',
    '  LXXR      LXXVXXXXXXXXXXXR     LXXR   ',
    '  LVXR     <LVXXXXVXXXXXXVXR     LXXR   ',
    '  LXXR      LXXXXXXXXVXXXXXR     LVXR>  ',
    '  LXXR      LXXVXXXXXXXXXXVR>    LXVR   ',
    '  LXXR>     LVXXXXXXXXXXVXXR    <LXXR   ',
    '  LXVR      LXXXXXXXXXVXXXXR     LXXR   ',
]

LEVEL_MAP5 = [
    'XXKBBBBBBBBBBBBJXXXXXXZXKBBBBBBBBBBBBJXX',
    'VK4>           LVXXXXXXXR       89   3JX',
    'K4             3BBBBBBBB4#$          <3J',
    'R>                89$#####$            L',
    'R                    $#$               L',
    'RN                       $             L',
    'H2                           $ #$ #  N1G',
    'XH2 7                         ###### 1GX',
    'XXHTTTT2                     $##1TTTTGXX',
    'XXZKBBB4>     7         7     #$3BBBJZXX',
    'XKB4 89      1TTT2    1TTT2    $####3BJX',
    'XR           LXKB4    3BJXR         ##LX',
    'K4           LX4        LXR       $  $3J',
    'R$           LXR        LXR            L',
    'R#$          LXR        LXR            L',
    'R##       1TTGXR        LXHTT2>        L',
    'R#$       3BBBB4        3BBBB4         L',
    'R#$        89               8          L',
    'R##$ $                                 L',
    'R### #$                                L',
    'H2####1T2                      1T2    1G',
    'XHTTTTGXR                     <LXHTTTTGX',
    'XXZXXXXVR   7              7   LXXXZVXXX',
    'XXXXXZXXHTTTTT2         1TTTTTTGZXXXXVXX',
    'XXXXXZXXXXXVXXR         LXXXXXZXXZXXXXXX',
]

LEVEL_MAP6 = [
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                 1TTTT2                 ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '          1TTTT2        1TTTT2          ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '       1TTTTTTTTTTTTTTTTTTTTTTTT2       ',
    '       LXXXXXXXXXXXXXXXXXXXXXXXXR       ',
    '       3BBBBBBBBBBBBBBBBBBBBBBBB4       ',
    '                                        ',
    '                                        ',
    '                                        ',
]

LEVEL_MAP7 = [
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                    7   ',
    '              77                <1TT2   ',
    '            1TT2                 LVXR   ',
    '            LXX4>               <LXXR   ',
    '   7       <LVX4                 LXVR   ',
    '  1TT2      LXV4                 LXXR>  ',
    '  LXVR      LXXR        7 7      LXXR   ',
    '  LXVR>     LXXR        1TT2     LXXR   ',
    '  LXXR      LXXR        LVXR     LVXR   ',
    '  LXXR      LXXR        LXXR     LXXR   ',
    '  LVXR      LVXR>       LVXR     LXXR   ',
    '  LXXR      LXXR        LXXR     LVXR>  ',
    '  LXXR      LXVR       <LXVR     LXVR   ',
    '  LXXR>     LVXR        LXXR    <LXXR   ',
    '  LXVR      LXXR>       LXXR     LXXR   ',
]

LEVEL_MAP8 = [
    'XXKBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBJXX',
    'XK4      8     89     8    89        3JX',
    'K4                                    3J',
    'R>                                     L',
    'R                                     <L',
    'R                                      L',
    'R                                      L',
    'RN                       $             L',
    'H2                           $ #$ #  N1G',
    'XH2 7                         ###### 1GX',
    'XXHTTTT2                     $##1TTTTGXX',
    'XXZKBBB4>                     #$3BBBJZXX',
    'XXK4                              893JXX',
    'XXRM         7          7            LXX',
    'XK4>        1TT2        1TT2         3JX',
    'K4      $   LXX4        LXVR          3J',
    'RM    $     LVXR       <LVXR           L',
    'R  $ #$    <LXXR        LXXR           L',
    'R> ##$      LXXR        LXXR           L',
    'R#$##$      LXXR        LXVR          <L',
    'R###$       LVXR>       LXXR           L',
    'R##$        LXVR        LXXR           L',
    'R>#$        LXXR        LXXR           L',
    'R           LXXR        LVXR>          L',
    'R           LXXR        LXXR           L',
]

LEVEL_MAP9 = [
    '                                        ',
    '                                        ',
    '                                        ',
    '     7                          7   7   ',
    '   1TTTT2                      1TTTT2   ',
    '   3BBBB4                      3BBBB4   ',
    '     89                            8     ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '        7   7      77   7      7        ',
    '       1TTTTTTTTTTTTTTTTTTTTTTTT2       ',
    '       LXXXXXXXXXXXXXXXXXXXXXXXXR       ',
    '       3BBBBBBBBBBBBBBBBBBBBBBBB4       ',
    '                                        ',
    '                                        ',
    '                                        ',
]

map_list = [LEVEL_MAP, LEVEL_MAP1, LEVEL_MAP2, LEVEL_MAP3, LEVEL_MAP4]

map_list2 = [LEVEL_MAP, LEVEL_MAP1, LEVEL_MAP2, LEVEL_MAP3, LEVEL_MAP4, LEVEL_MAP5, LEVEL_MAP6, LEVEL_MAP7, LEVEL_MAP8]

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

# 7: Grass
# 8: Vine
# 9: Vine 2

# #: Brick One
# $: Brick Two

# <: Leaf Left 
# >: Leaf Right 

# Z: Inside Rock 
# V: Inside Leaf 

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
GRAVITY = 15
FRICTION = 0.8

def change_res(x, y):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = x
    SCREEN_HEIGHT = y

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

# dictionary for all weapons
weapon_dict = {
    "shard": Weapon(
        "The Shard", 
        "Common",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/shard.png"), 
        os.path.join(base_directory, "assets/sound/swoosh.wav"), 
        0.5,
        5,
        30,
        -30,
        (30, 90), 
        (100, 120),
        (255, 255, 255),
        1,
        1,
        1,
    ),
    "devSword": Weapon(
        "Dev Sword", 
        "Mythic",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/dev_sword.png"), 
        os.path.join(base_directory, "assets/sound/toot.mp3"), 
        0.2, 
        5,
        30,
        -30,
        (30, 90), 
        (300, 300),
        (255, 255, 255),
        1,
        1,
        1,
        0.2, 
        25, 
        -20, 
        True, 
        10,
        True
    ),
    "dagger": Weapon(
        "Dagger",
        "Rare",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/dagger.png"),
        os.path.join(base_directory, "assets/sound/swoosh.wav"),
        0.1,
        0,
        30,
        0,
        (30, 50),
        (50, 90),
        (255, 255, 255),
        2,
        1.5,
        1,
        0.2,
        13,
        -17,
        False,
        2,
        False
    ),
    "katana": Weapon(
        "Katana",
        "Rare",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/katana.png"),
        os.path.join(base_directory, "assets/sound/swoosh.wav"),
        0.1,
        0,
        30,
        -70,
        (30, 130),
        (200, 160),
        (255, 255, 255),
        0.8,
        1,
        1,
        1.2,
        14,
        -17,
        False,
        1,
        False
    ),
    "wingedSword": Weapon(
        "Winged Sword",
        "Mythic",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/winged_sword.png"),
        os.path.join(base_directory, "assets/sound/swoosh.wav"),
        0.1,
        -10,
        15,
        -30,
        (60, 90),
        (75, 120),
        (255, 255, 255),
        1,
        1,
        1,
        0.2,
        12,
        -20,
        False,
        2,
        True
    ),
    "momsKnife": Weapon(
        "Mom's Knife",
        "Common",
        "Thrust",
        os.path.join(base_directory, "assets/img/swords/moms_knife.png"),
        os.path.join(base_directory, "assets/sound/stab.mp3"),
        0.1,
        0,
        -30,
        40,
        (30, 90),
        (120, 50),
        (255, 255, 255),
        1,
        1,
        1,
        0.7,
        13,
        -17,
        False,
        3,
        False
    ),
    "thiefsTorch": Weapon(
        "Thief's Torch",
        "Common",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/theifs_torch.png"),
        os.path.join(base_directory, "assets/sound/swoosh.wav"),
        0.1,
        -10,
        20,
        -22,
        (50, 80),
        (100, 112),
        (255, 109, 0),
        1,
        1,
        1,
    ),
    "iceSword": Weapon(
        "Ice Sword",
        "Mythic",
        "Slash",
        os.path.join(base_directory, "assets/img/swords/ice_sword.png"),
        os.path.join(base_directory, "assets/sound/swoosh.wav"),
        0.1,
        5,
        30,
        -30,
        (30, 90),
        (100, 120),
        (204, 255, 255),
        1,
        1,
        1,
        0.7,
        12,
        -17,
        False,
        3,
        False,
        True
    ),
    "momoSword": Weapon(
        "Momotaro's Sword",
        "Rare",
        "Thrust",
        os.path.join(base_directory, "assets/img/swords/momotaros_sword.png"),
        os.path.join(base_directory, "assets/sound/momo_strike.mp3"),
        0.1,
        0,
        -140,
        35,
        (20, 200),
        (300, 50),
        (255, 255, 255),
        0.6,
        0.8,
        1,
        2,
        12,
        -17,
        False,
        4,
        False,
        False
    )
}


def writeToJson(data_dict, output_file):
    try:
        # Load the existing JSON data from the file if it exists
        with open(output_file, 'r') as file:
            existing_data = json.load(file)
    except json.JSONDecodeError:
        # If the file exists but is empty, set existing_data to an empty list
        existing_data = []
    except FileNotFoundError:
        # If the file doesn't exist, set existing_data to an empty list
        existing_data = []

    # Create a set of existing names to keep track of names already in the JSON
    existing_names = set(item["name"] for item in existing_data)

    # Update existing_data with new keys and default "seen" value if the name does not exist
    for key in data_dict.keys():
        if data_dict[key].name not in existing_names:
            if data_dict[key].name != "The Shard":
                existing_data.append({"name": data_dict[key].name, "seen": 0})
            else:
                existing_data.append({"name": data_dict[key].name, "seen": 1})
        for entry in existing_data:
            if entry["name"] == "The Shard":
                entry["seen"] = 1
                
    # Write the updated JSON data to the output file
    # override previous json data
    with open(output_file, 'w') as file:
        json.dump(existing_data, file, indent=4)
