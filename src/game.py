# Import the pygame module
from distutils.spawn import spawn
from operator import truediv
from select import select
from tkinter import Menu
from Particle import Particle
import time
import random
import pygame
import CONSTANTS as C
from Player import Player
from Level import Level
from Weapons import *
import ctypes
import os
import platform

base_directory = os.path.dirname(os.path.abspath(__file__))

#windows solution to scaling issues with high ppi display
if platform.system() == 'Windows':
    ctypes.windll.user32.SetProcessDPIAware()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_x,
    K_PERIOD,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

clock = pygame.time.Clock()

class Game():
    def __init__(self):
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        pygame.init()
        pygame.mixer.init()
        
        flags = pygame.SCALED | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), flags)
        self.camera = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), flags)
        
        # Instantiate player. Right now, this is just a rectangle.
        self.players = pygame.sprite.Group()
        abs_path = os.path.join(base_directory, "assets/img/character.png")
        self.player = Player(C.key_presses_1, abs_path, (C.SCREEN_WIDTH/6, 100))
        self.players.add(self.player)
        self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (C.SCREEN_WIDTH*5/6, 100))
        self.players.add(self.player2)
        
        self.character1_img = pygame.image.load('src/assets/img/character_icon.png')
        self.character1_img = pygame.transform.scale(self.character1_img, (100, 100))
            
        self.character2_img = pygame.image.load('src/assets/img/character2_icon.png')
        self.character2_img = pygame.transform.scale(self.character2_img, (100, 100))
        
        self.character1_damaged_img = pygame.image.load('src/assets/img/character_icon_damaged.png')
        self.character1_damaged_img = pygame.transform.scale(self.character1_damaged_img, (100, 100))
        
        self.character2_damaged_img = pygame.image.load('src/assets/img/character2_icon_damaged.png')
        self.character2_damaged_img = pygame.transform.scale(self.character2_damaged_img, (100, 100))
        
        self.character_icon = self.character1_img
        self.character2_icon = self.character2_img
        
        self.character1_hud = pygame.image.load('src/assets/img/character1_hud.png')
        self.character1_hud = pygame.transform.scale(self.character1_hud, (310, 140))
        
        self.character2_hud = pygame.image.load('src/assets/img/character2_hud.png')
        self.character2_hud = pygame.transform.scale(self.character2_hud, (310, 140))
        
        self.round_hud = pygame.image.load('src/assets/img/round_hud.png')
        self.round_hud = pygame.transform.scale(self.round_hud, (310, 140))
        
        self.player_weapon = pygame.transform.scale(self.player.weapon.image, (36, 108))
        self.player2_weapon = pygame.transform.scale(self.player2.weapon.image, (36, 108))

        self.the_map_list = []
        
        pygame.mouse.set_visible(False)

        pygame.display.set_caption("WEAPONIZE")
        icon = pygame.image.load(os.path.join(base_directory, "assets/img/icon.png"))
        pygame.display.set_icon(icon)
        
        self.level = Level(C.LEVEL_MAP, self.screen, os.path.join(base_directory, "assets/img/DefaultBackground.png"))

        self.select_sound = pygame.mixer.Sound(os.path.join(base_directory, "assets/sound/Select.wav"))
        self.select_sound.set_volume(0.1)
        
        self.attack_sound = pygame.mixer.Sound(os.path.join(base_directory, 'assets/sound/swoosh.wav'))
        self.attack_sound.set_volume(0.1)
        
        self.chest_open_sound = pygame.mixer.Sound(os.path.join(base_directory, 'assets/sound/chest_open.mp3'))
        self.chest_open_sound.set_volume(0.1)
        
        self.sword_get_sound = pygame.mixer.Sound(os.path.join(base_directory, 'assets/sound/sword_get.wav'))
        self.sword_get_sound.set_volume(0.1)


        self.menu_running = True
        self.game_running = False
        self.paused = False
        self.options_running = False
        self.pregame_running = False
        
        self.color_menu = (40, 40, 40)
        self.color_select = (255, 77, 112)
        self.color_default = (245, 244, 228)

        self.attack_start = time.time()
        self.attack_start2 = time.time()
        
        self.attacking_start = time.time()
        self.attacking_start2 = time.time()
        
        self.invincibility_start = time.time()
        self.invincibility_start2 = time.time()
        
        self.damaged_start = time.time()
        self.damaged_start2 = time.time()
        
        self.winner = 1
        self.isPostGame = False
        
        self.round_num = 1
        self.player_one_wins = 0
        self.player_two_wins = 0
        
        # Used for Dynamic Camera Tracking
        self.player_distance = 0
        self.player_midpoint = pygame.math.Vector2(0, 0)
        self.camera_x = 0
        self.camera_y = 0
        self.camera_width = C.SCREEN_WIDTH
        self.camera_height = C.SCREEN_HEIGHT
        self.cam_dim = [self.camera_width, self.camera_height]
        self.zoom = True
        
        
    def getPlayerMidpoint(self, Player1, Player2):
        midpoint = ((Player1.rect.x + Player2.rect.x)/2, (Player1.rect.y + Player2.rect.y)/2)
        roundedMidPoint = tuple(map(lambda x: round(x), midpoint))
        res = [roundedMidPoint[0], roundedMidPoint[1]]
        return res

    def horizontal_movement_collision(self):
        players = self.players.sprites()
        for player in players:
            player.rect.x += player.direction.x * player.speed            
            for sprite in self.level.tile_group.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    if player.direction.x > 0:
                        player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        players = self.players.sprites()
        for player in players:
            # make a temp rect to check if the player is on the ground, place it 1 pixel below the player
            player.apply_gravity()
            for sprite in self.level.tile_group.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.isOnGround = True
                        player.hasDash = True
                        player.hasDoubleJump = True
                        player.gravity = 0.9
                    if player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0

        if player.direction.y > 0:
            player.isOnGround = False



    def draw_text(self, text, color, size, x, y):
        font = pygame.font.Font(os.path.join(base_directory, "assets/fonts/ThaleahFat.ttf"), size)
        text_surface = font.render(text, True, color)
        #scale surface
        scaled_text_image = pygame.transform.scale(text_surface, (int(text_surface.get_width()), int(text_surface.get_height())))
        text_rect = scaled_text_image.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(scaled_text_image, text_rect)
    
            
    def run_menu(self):
        current_selection = "start"
        
        self.menu_running = True
        
        while self.menu_running:
            if(current_selection == "start"):
                start_text_color = self.color_select
                settings_text_color = self.color_default
                quit_text_color = self.color_default
            elif(current_selection == "settings"):
                start_text_color = self.color_default
                settings_text_color = self.color_select
                quit_text_color = self.color_default
            elif(current_selection == "quit"):
                start_text_color = self.color_default
                settings_text_color = self.color_default
                quit_text_color = self.color_select
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.menu_running = False
                    elif event.key == K_w or event.key == K_UP:
                        if(current_selection == "settings"):
                            current_selection = "start"
                            pygame.mixer.Sound.play(self.select_sound)
                        elif(current_selection == "quit"):
                            current_selection = "settings"
                            pygame.mixer.Sound.play(self.select_sound)
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "start"):
                            current_selection = "settings"
                            pygame.mixer.Sound.play(self.select_sound)
                        elif(current_selection == "settings"):
                            current_selection = "quit"
                            pygame.mixer.Sound.play(self.select_sound)
                    elif event.key == K_RETURN:
                        if(current_selection == "start"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.menu_running = False
                            self.pregame_menu()
                        if(current_selection == "settings"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.gun_screen()
                        elif(current_selection == "quit"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.menu_running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.menu_running = False
            
            self.screen.fill(self.color_menu)
            # create a surface object, image is drawn on it.
            title_img = pygame.image.load(os.path.join(base_directory, "assets/img/title.png"))
            title_img = pygame.transform.scale(title_img,((C.SCREEN_WIDTH * 0.6), (((C.SCREEN_WIDTH* 0.6)/3))))
            self.screen.blit(title_img, ((C.SCREEN_WIDTH/2 - (title_img.get_width()/2)), 100))
            
            #C.SCREEN_WIDTH/2 - ((C.SCREEN_WIDTH* 0.6)/2
            self.draw_text("PLAY", start_text_color, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + (150))
            self.draw_text("OPTIONS", settings_text_color, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + (300))
            self.draw_text("QUIT", quit_text_color, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + (450))
            pygame.display.flip()

    def run_game(self):
        # Setup the level        
        self.game_running = True
        
        if self.round_num is 1:
            self.the_map_list = C.map_list[:]
        elif self.round_num is 6:
            self.the_map_list = C.map_list2[:]
         
        if self.player_one_wins == 4 and self.player_two_wins == 4:
            current_map = C.LEVEL_MAP9
        else:
            current_map = random.choice(self.the_map_list)
            self.the_map_list.remove(current_map)
            
        if current_map == C.LEVEL_MAP:
            self.players.empty()
            spawn_options = [1, 2]
            choice = random.choice(spawn_options)
            if choice == 1:
                self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 800))
                self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 800))
            elif choice == 2:
                self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 300))
                self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 300))
            self.players.add(self.player)
            self.players.add(self.player2)
        elif current_map == C.LEVEL_MAP1:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 300))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 300))
            self.players.add(self.player2)
        elif current_map == C.LEVEL_MAP2:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (400, 800))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1450, 800))
            self.players.add(self.player2)
        elif current_map == C.LEVEL_MAP3:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (400, 800))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1450, 800))
            self.players.add(self.player2)
        elif current_map ==C.LEVEL_MAP4:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 300))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 300))
            self.players.add(self.player2)
        elif current_map == C.LEVEL_MAP5:
            self.players.empty()
            spawn_options = [1, 2]
            choice = random.choice(spawn_options)
            if choice == 1:
                self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 800))
                self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 800))
            elif choice == 2:
                self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 300))
                self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 300))
            self.players.add(self.player)
            self.players.add(self.player2) 
        elif current_map == C.LEVEL_MAP6:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (400, 800))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1450, 800))
            self.players.add(self.player2)
        elif current_map ==C.LEVEL_MAP7:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 300))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 300))
            self.players.add(self.player2)
        elif current_map == C.LEVEL_MAP8:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 300))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 300))
            self.players.add(self.player2)
        elif current_map == C.LEVEL_MAP9:
            self.players.empty()
            self.player = Player(C.key_presses_1, os.path.join(base_directory, "assets/img/character.png"), (200, 0))
            self.players.add(self.player)
            self.player2 = Player(C.key_presses_2, os.path.join(base_directory, "assets/img/character2.png"), (1650, 0))
            self.players.add(self.player2)
        
        self.level = Level(current_map, self.screen, os.path.join(base_directory, "assets/img/DefaultBackground.png"))

        
        self.character_icon = self.character1_img
        self.character2_icon = self.character2_img
        # Main loop

        """
        Working on implementing particles

        ...not working yet
        """
        particle1 = Particle()
        PARTICLE_EVNET = pygame.USEREVENT + 1
        pygame.time.set_timer(PARTICLE_EVNET, 100)


        while self.game_running:
            
            clock.tick(60) # limit fps to 60
            pressed_keys = pygame.key.get_pressed()
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.pause_menu()
                    elif event.key == K_w:
                         self.player.jump()
                    elif event.key == K_UP:
                         self.player2.jump()
                    elif event.key == pygame.K_y:
                        self.zoom = not self.zoom
            # Run the Level
            self.level.run()

            # Draw the player on the screen
            self.players.update(pressed_keys)
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.players.draw(self.screen)
            
            # self.screen.blit(self.player.image, self.player.pos)
            # self.screen.blit(self.player2.image, self.player2.pos)
            if pressed_keys[pygame.K_x] and self.player.canAttack:
                if pressed_keys[pygame.K_d]:
                    self.player.attackRight = True
                elif pressed_keys[pygame.K_a]:
                    self.player.attackRight = False
                else:
                    if self.player.facingRight:
                        self.player.attackRight = True
                    else:
                        self.player.attackRight = False                 
                self.player.attacking = True
                self.player.canAttack = False
                pygame.mixer.Sound.play(self.attack_sound)
                self.attacking_start = time.time()
                self.attack_start = time.time()
                
            if pressed_keys[pygame.K_PERIOD] and self.player2.canAttack:
                if pressed_keys[pygame.K_RIGHT]:
                    self.player2.attackRight = True
                elif pressed_keys[pygame.K_LEFT]:
                    self.player2.attackRight = False
                else:
                    if self.player2.facingRight:
                        self.player2.attackRight = True
                    else:
                        self.player2.attackRight = False                 
                self.player2.attacking = True
                self.player2.canAttack = False
                pygame.mixer.Sound.play(self.attack_sound)
                self.attacking_start2 = time.time()
                self.attack_start2 = time.time()
            
            if self.player.attacking:
                if self.player.attackRight:
                    player_attack_hitbox = pygame.Rect(self.player.rect.x + self.player.image.get_width(), self.player.rect.y, self.player.slash_right_image.get_width(), self.player.slash_right_image.get_height())
                    # pygame.draw.rect(self.screen, (136, 8, 8), player_attack_hitbox)
                    self.screen.blit(self.player.slash_right_image, (self.player.rect.x + self.player.image.get_width(), self.player.rect.y))
                    if pygame.Rect.colliderect(player_attack_hitbox, self.player2.rect):
                        self.player_hit(self.player2, False)
                        self.player2.isHit = True
                        self.player2.knockbackRight = True
                elif not self.player.attackRight:
                    player_attack_hitbox = pygame.Rect(self.player.rect.x - self.player.slash_left_image.get_width(), self.player.rect.y, self.player.slash_right_image.get_width(), self.player.slash_right_image.get_height())
                    # pygame.draw.rect(self.screen, (136, 8, 8), player_attack_hitbox)
                    self.screen.blit(self.player.slash_left_image, (self.player.rect.x - self.player.slash_left_image.get_width(), self.player.rect.y))
                    if pygame.Rect.colliderect(player_attack_hitbox, self.player2.rect):
                        self.player_hit(self.player2, False)
                        self.player2.isHit = True
                        self.player2.knockbackRight = False
                if time.time() - self.attacking_start > 0.1:
                    self.player.attacking = False
                    self.attacking_start = time.time()
            else:
                if self.player.facingRight:
                    self.screen.blit(self.player.weapon.image, (self.player.rect.x + 5, self.player.rect.y - 30))
                else:
                    self.screen.blit(self.player.weapon.image, (self.player.rect.x + 30, self.player.rect.y - 30))
                    
            if self.player2.attacking:
                if self.player2.attackRight:
                    player2_attack_hitbox = pygame.Rect(self.player2.rect.x + self.player2.image.get_width(), self.player2.rect.y, self.player2.slash_right_image.get_width(), self.player2.slash_right_image.get_height())
                    # pygame.draw.rect(self.screen, (136, 8, 8), player2_attack_hitbox)
                    self.screen.blit(self.player2.slash_right_image, (self.player2.rect.x + self.player2.image.get_width(), self.player2.rect.y))
                    if pygame.Rect.colliderect(player2_attack_hitbox, self.player.rect):
                        self.player_hit(self.player, True)
                        self.player.isHit = True
                        self.player.knockbackRight = True
                elif not self.player2.attackRight:
                    player2_attack_hitbox = pygame.Rect(self.player2.rect.x - self.player2.slash_left_image.get_width(), self.player2.rect.y, self.player2.slash_right_image.get_width(), self.player2.slash_right_image.get_height())
                    # pygame.draw.rect(self.screen, (136, 8, 8), player2_attack_hitbox)
                    self.screen.blit(self.player2.slash_left_image, (self.player2.rect.x - self.player2.slash_left_image.get_width(), self.player2.rect.y))
                    if pygame.Rect.colliderect(player2_attack_hitbox, self.player.rect):
                        self.player_hit(self.player, True)
                        self.player.isHit = True
                        self.player.knockbackRight = False
                if time.time() - self.attacking_start2 > 0.1:
                    self.player2.attacking = False
                    self.attacking_start2 = time.time()
            else:
                if self.player2.facingRight:
                    self.screen.blit(self.player2.weapon.image, (self.player2.rect.x + 5, self.player2.rect.y - 30))
                else:
                    self.screen.blit(self.player2.weapon.image, (self.player2.rect.x + 30, self.player2.rect.y - 30))

            if self.zoom:
                # calculate player distance and midpoint
                # self.player_distance = self.getPlayerDistance(self.player, self.player2)
                self.player_midpoint = self.getPlayerMidpoint(self.player, self.player2)
                # self.draw_text("Distance: " + str(self.player_distance), self.color_default, 50, 200, 100)
                # self.draw_text("Midpoint: " + str(self.player_midpoint), self.color_default, 50, 300, 200)

                # move camera, resize as needed
                min_x = min(self.player.rect.x, self.player2.rect.x)
                min_y = min(self.player.rect.y, self.player2.rect.y)
                max_x = max(self.player.rect.x, self.player2.rect.x)
                max_y = max(self.player.rect.y, self.player2.rect.y)
                
                PADDING = 300

                # maintain a 1.6 : 1 aspect ratio
                player_min_y = min(self.player.rect.y, self.player2.rect.y) + self.player.rect.height
                player_max_y = max(self.player.rect.y, self.player2.rect.y)
                player_min_x = min(self.player.rect.x, self.player2.rect.x)
                player_max_x = max(self.player.rect.x, self.player2.rect.x) + self.player.rect.width
                x_dist = player_max_x - player_min_x

                offset = C.SCREEN_WIDTH - 1200
                # if the distance between the players is less than 1200 pixels, zoom in
                if x_dist < 1200:
                    # slowly decrease camera width and height to zoom in
                    # stop zooming once camera width reaches minimum
                    self.camera_width = max(x_dist + offset, 600 + offset)
                    self.camera_height = int(self.camera_width * 0.625)

                    # adjust position based on player center
                    midpoint = self.player_midpoint
                    midpoint[0] = midpoint[0] + self.player.rect.width // 2
                    midpoint[1] = midpoint[1] + self.player.rect.height // 2
                    self.camera_x = midpoint[0] - self.camera_width // 2
                    self.camera_y = midpoint[1] - self.camera_height // 2
                    # self.camera_x, self.camera_y is top left corner of viewport
                    if self.camera_x < 0:
                        self.camera_x = 0
                    elif self.camera_x + self.camera_width > C.SCREEN_WIDTH:
                        self.camera_x = C.SCREEN_WIDTH - self.camera_width
                    if self.camera_y < 0:
                        self.camera_y = 0
                    elif self.camera_y + self.camera_height > C.SCREEN_HEIGHT:
                        self.camera_y = C.SCREEN_HEIGHT - self.camera_height
                else:
                    self.camera_width = C.SCREEN_WIDTH
                    self.camera_height = C.SCREEN_HEIGHT
                    self.camera_x = 0
                    self.camera_y = 0
                
                # limit camera to level boundaries
                self.camera_width = min(self.camera_width, C.SCREEN_WIDTH)
                self.camera_height = min(self.camera_height, C.SCREEN_HEIGHT)

                # draw red box around camera
                # pygame.draw.rect(self.screen, (255, 0, 0), (self.camera_x, self.camera_y, self.camera_width, self.camera_height), 2)
                # draw dot at self.camera_x, self.camera_y
                # pygame.draw.circle(self.screen, (0, 255, 0), (self.camera_x, self.camera_y), 10)
                # make a subsurface of self.screen, using dimensions of camera
                subsurface = self.screen.subsurface((self.camera_x, self.camera_y, self.camera_width, self.camera_height))
                # make a textbox rect object to display the dimensions of self.camera
                #dim_rect = pygame.Rect(50, 50, 200, 100)
                #font = pygame.font.Font(os.path.join(base_directory, "assets/fonts/ThaleahFat.ttf"), 40)
                #text_surface = font.render(str(subsurface.get_width()) + " x " + str(subsurface.get_height()), True, (255, 255, 255))
                #text_rect = text_surface.get_rect(center = dim_rect.center)
                #pygame.draw.rect(subsurface, (0, 0, 0), dim_rect)
                #subsurface.blit(text_surface, text_rect)

                # self.draw_text(str(subsurface.get_width()) + " x " + str(subsurface.get_height()), self.color_default, 50, 200, 100)
                # display the subsurface and scale it to the screen size
                # THIS IS WHAT ZOOMS IN AND OUT
                self.screen.blit(pygame.transform.scale(subsurface, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT)), (0, 0))

            # player 1 attack cooldown
            if self.player.canAttack is False:
                if time.time() - self.attack_start > 0.7:
                    self.player.canAttack = True
                    self.attack_start = time.time()
                    
            # player 2 attack cooldown
            if self.player2.canAttack is False:
                if time.time() - self.attack_start2 > 0.7:
                    self.player2.canAttack = True
                    self.attack_start2 = time.time()
                    
            if self.player2.isInvincible:
                if time.time() - self.invincibility_start2 > 0.3:
                    self.player2.isInvincible = False
                    self.invincibility_start2 = time.time()
                    
            if self.player.isInvincible:
                if time.time() - self.invincibility_start > 0.3:
                    self.player.isInvincible = False
                    self.invincibility_start = time.time()

               
            if self.player.isDamaged:
                if time.time() - self.damaged_start > 5:
                    self.player.isDamaged = False
                    self.player.image = self.player.OriginalImage
                    self.character_icon = self.character1_img
                    self.damaged_start = time.time()
                                        
            if self.player2.isDamaged:
                if time.time() - self.damaged_start2 > 5:
                    self.player2.isDamaged = False
                    self.player2.image = self.player2.OriginalImage
                    self.character2_icon = self.character2_img
                    self.damaged_start2 = time.time()
                    
            if self.player.rect.y > C.SCREEN_HEIGHT + 250:
                self.player.isDamaged = True
                self.player_hit(self.player, True)
            elif self.player2.rect.y > C.SCREEN_HEIGHT + 250:
                self.player2.isDamaged = True
                self.player_hit(self.player2, False)
                
            #HUD
            #round_hud = pygame.Rect((C.SCREEN_WIDTH/2 - 150), 0, 350, 175)
            #pygame.draw.rect(self.screen, (34, 34, 34), round_hud)
                        
            self.draw_text("ROUND", self.color_default, 105, C.SCREEN_WIDTH/2, 60)
            self.draw_text(str(self.round_num), self.color_select, 105, C.SCREEN_WIDTH/2, 120)

            self.screen.blit(self.character1_hud, (120 , C.SCREEN_HEIGHT - 180))
            self.screen.blit(self.character_icon, (222 , C.SCREEN_HEIGHT - 160))
            
            self.screen.blit(self.character2_hud, (C.SCREEN_WIDTH - 430 , C.SCREEN_HEIGHT - 180))
            self.screen.blit(self.character2_icon, ((C.SCREEN_WIDTH - 320) ,  C.SCREEN_HEIGHT - 160))

            self.draw_text(str(self.player_one_wins), self.color_default, 110, 384, C.SCREEN_HEIGHT - 85)
            self.draw_text(str(self.player_two_wins), self.color_default, 100, C.SCREEN_WIDTH - 378, C.SCREEN_HEIGHT - 85)
            
            self.screen.blit(self.player_weapon, (146, C.SCREEN_HEIGHT - 163))
            self.screen.blit(self.player2_weapon, (C.SCREEN_WIDTH - 182, C.SCREEN_HEIGHT - 163))

            
            pygame.display.flip()
                    
    def pause_menu(self):
        current_selection = "resume"
        pygame.mixer.pause()
        self.paused = True
        while self.paused:
            # pause_background = pygame.Surface((C.SCREEN_WIDTH/4, C.SCREEN_HEIGHT/2))
            # pause_background.set_alpha(50)
            # pause_background.fill((34,39,63)) #(34,39,63)
            # self.screen.blit(pause_background, (C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2))
            
            background_image = pygame.image.load(os.path.join(base_directory, "assets/img/menuBackground.png")).convert()
            background_image = pygame.transform.scale(background_image, (C.SCREEN_WIDTH/4, C.SCREEN_HEIGHT/2))
            background_image.set_alpha(100)
            self.screen.blit(background_image, (C.SCREEN_WIDTH/2 - ((C.SCREEN_WIDTH/4)/2), C.SCREEN_HEIGHT/2 - ((C.SCREEN_HEIGHT/2)/2)))

            
            # Check for QUIT event. If QUIT, then set running to false.    
            if(current_selection == "resume"):
                resume_text_color = self.color_select
                settings_text_color = self.color_default
                quit_text_color = self.color_default
            elif(current_selection == "settings"):
                resume_text_color = self.color_default
                settings_text_color = self.color_select
                quit_text_color = self.color_default
            elif(current_selection == "quit"):
                resume_text_color = self.color_default
                settings_text_color = self.color_default
                quit_text_color = self.color_select
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.paused = False
                        pygame.mixer.unpause()
                    elif event.key == K_w or event.key == K_UP:
                        if(current_selection == "settings"):
                            current_selection = "resume"
                            pygame.mixer.Sound.play(self.select_sound)
                        elif(current_selection == "quit"):
                            current_selection = "settings"
                            pygame.mixer.Sound.play(self.select_sound)
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "resume"):
                            current_selection = "settings"
                            pygame.mixer.Sound.play(self.select_sound)
                        elif(current_selection == "settings"):
                            current_selection = "quit"
                            pygame.mixer.Sound.play(self.select_sound)
                    elif event.key == K_RETURN:
                        if(current_selection == "resume"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.paused = False
                        if(current_selection == "quit"):
                            pygame.mixer.Sound.play(self.select_sound)
                            pygame.mixer.stop()
                            self.game_running = False
                            self.paused = False
                            self.menu_running = True
                        
            self.draw_text("RESUME", resume_text_color, 35, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 150)
            self.draw_text("SETTINGS", settings_text_color, 35, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)
            self.draw_text("RETURN TO MENU", quit_text_color, 35, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 150)
            pygame.display.flip()

    def options_menu(self):
        
        self.options_running = True

        while self.options_running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                            self.options_running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.options_running = False
            
            self.screen.fill(self.color_menu)
            self.draw_text("OPTIONS", self.color_default, 75, C.SCREEN_WIDTH/2, 100)
            self.draw_text("There are no options to change yet. Check back later.", self.color_default, 40, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)
            pygame.display.flip()
            
    def pregame_menu(self):
        current_selection = "play"
        
        self.pregame_running = True
        
        while self.pregame_running:
            if(current_selection == "play"):
                start_text_color = self.color_select
                quit_text_color = self.color_default
                controls_text_color = self.color_default
            elif(current_selection == "quit"):
                start_text_color = self.color_default
                quit_text_color = self.color_select
                controls_text_color = self.color_default
            elif(current_selection == "controls"):
                controls_text_color = self.color_select
                start_text_color = self.color_default
                quit_text_color = self.color_default
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.pregame_running = False
                        self.run_menu()
                    elif event.key == K_w or event.key == K_UP:
                        if(current_selection == "quit"):
                            pygame.mixer.Sound.play(self.select_sound)
                            current_selection = "controls"
                        elif(current_selection == "controls"):
                            pygame.mixer.Sound.play(self.select_sound)
                            current_selection = "play"
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "play"):
                            pygame.mixer.Sound.play(self.select_sound)
                            current_selection = "controls"
                        elif(current_selection == "controls"):
                            pygame.mixer.Sound.play(self.select_sound)
                            current_selection = "quit"
                    elif event.key == K_RETURN:
                        if(current_selection == "play"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.round_num = 1
                            self.player_one_wins = 0
                            self.player_two_wins = 0
                            self.pregame_running = False
                            self.isPostGame = False
                            pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(base_directory, "assets/sound/LevelMusic.mp3"))).set_volume(0.1)
                            self.run_game()
                        elif(current_selection == "controls"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.pregame_running = False
                            self.controls_menu()
                        # elif(current_selection == "practice"):
                            # self.menu_running = False
                        elif(current_selection == "quit"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.pregame_running = False
                            self.run_menu()
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.pregame_running = False
                    self.run_menu()
            
            self.screen.fill(self.color_menu)
            round_hud = pygame.Rect((C.SCREEN_WIDTH/2 - (C.SCREEN_WIDTH/4)), (C.SCREEN_HEIGHT/2 - (C.SCREEN_HEIGHT/4 + 100)), C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 200)
            pygame.draw.rect(self.screen, (34,34,34), round_hud)
            self.draw_text("PRE GAME MENU", self.color_default, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 850)
            self.draw_text("START", start_text_color, 60, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 650)
            self.draw_text("ARMORY", (130,130,130), 60, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 550)
            self.draw_text("CONTROLS", controls_text_color, 60, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 450)
            self.draw_text("RETURN TO MENU", quit_text_color, 60, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 350)
            pygame.display.flip()
            
    def controls_menu(self):  
        self.controls_showing = True
        
        while self.controls_showing:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.controls_showing = False
                        self.pregame_menu()
                    elif event.key == K_RETURN:
                            self.controls_showing = False
                            self.pregame_menu()
            self.screen.fill(self.color_menu)
            self.draw_text("CONTROLS", self.color_default, 90, C.SCREEN_WIDTH/2, 150)
            self.draw_text("PLAYER ONE:", self.color_default, 50, C.SCREEN_WIDTH/2 - 400, 400)
            self.draw_text("PLAYER TWO:", self.color_default, 50, C.SCREEN_WIDTH/2 + 400, 400)
            
            player1_controls_image = pygame.image.load(os.path.join(base_directory, "assets/img/player1Controls.png"))
            player1_controls_image = pygame.transform.scale(player1_controls_image, (C.SCREEN_WIDTH/9, (((C.SCREEN_WIDTH/9)/3)*2)))
            self.screen.blit(player1_controls_image, (C.SCREEN_WIDTH/2 - 500, 500))
    
            player2_controls_image = pygame.image.load(os.path.join(base_directory, "assets/img/player2Controls.png"))
            player2_controls_image = pygame.transform.scale(player2_controls_image, (C.SCREEN_WIDTH/9, (((C.SCREEN_WIDTH/9)/3)*2)))
            self.screen.blit(player2_controls_image, (C.SCREEN_WIDTH/2 + 300, 500))
            
            player1_2_controls_image = pygame.image.load(os.path.join(base_directory, "assets/img/player1_2Controls.png"))
            player1_2_controls_image = pygame.transform.scale(player1_2_controls_image, (C.SCREEN_WIDTH/27, (((C.SCREEN_WIDTH/27)*3))))
            self.screen.blit(player1_2_controls_image, (C.SCREEN_WIDTH/2 - 500, 800))
    
            player2_2_controls_image = pygame.image.load(os.path.join(base_directory, "assets/img/player2_2Controls.png"))
            player2_2_controls_image = pygame.transform.scale(player2_2_controls_image, (C.SCREEN_WIDTH/27, (((C.SCREEN_WIDTH/27)*3))))
            self.screen.blit(player2_2_controls_image, (C.SCREEN_WIDTH/2 + 300, 800))
            
            self.draw_text("ATTACK", self.color_default, 50, C.SCREEN_WIDTH/2 - 330, 830)
            self.draw_text("DASH", self.color_default, 50, C.SCREEN_WIDTH/2 - 330, 980)

            self.draw_text("ATTACK", self.color_default, 50, C.SCREEN_WIDTH/2 + 450, 850)
            self.draw_text("DASH", self.color_default, 50, C.SCREEN_WIDTH/2 + 450, 950)

            pygame.display.flip()
            
    def game_over(self):
        self.game_is_over = True
        self.round_is_over = False
        playedSound = False
        while self.game_is_over:
            background_image = pygame.image.load(os.path.join(base_directory, "assets/img/menuBackground.png")).convert()
            background_image = pygame.transform.scale(background_image, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
            background_image.set_alpha(140)
            self.screen.blit(background_image, (0,0))
        
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_RETURN:
                        pygame.mixer.stop()
                        self.game_running = False
                        self.game_is_over = False
                        self.menu_running = True
                        self.run_menu()
            
            final_script = f"PLAYER {self.winner}"
            if not playedSound:
                pygame.mixer.Sound.play(self.sword_get_sound)
                playedSound = True
            self.draw_text(final_script, self.color_select, 70, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 20)
            self.draw_text("WON THE GAME", (255, 255, 255), 70, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 20)
            pygame.display.flip()

    def round_over(self, player):
        self.round_is_over = True
        while self.round_is_over:
            background_image = pygame.image.load(os.path.join(base_directory, "assets/img/menuBackground.png")).convert()
            background_image = pygame.transform.scale(background_image, (C.SCREEN_WIDTH/3, C.SCREEN_HEIGHT/3))
            background_image.set_alpha(140)
            self.screen.blit(background_image, (C.SCREEN_WIDTH/2 - (C.SCREEN_WIDTH/6), (C.SCREEN_HEIGHT/2 - C.SCREEN_HEIGHT/6)))
        
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_RETURN:
                        if self.round_num == 6:
                            self.game_running = False
                            self.round_is_over = False
                            self.gun_screen()
                        else:
                            self.game_running = False
                            self.round_is_over = False
                            self.run_game()
            
            final_script = f"Player {player} won!"
            self.draw_text(final_script, (255, 255, 255), 70, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50)
            self.draw_text("Press ENTER to continue.", (255, 255, 255), 30, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 75)
            pygame.display.flip()
            
    def gun_screen(self):
        self.giving_gun = True
        chest_last_time = pygame.time.get_ticks()
        chest2_last_time = pygame.time.get_ticks()
        chest_current_frame = 0
        chest2_current_frame = 0
        
        self.player_one_wins = 0
        self.player_two_wins = 0
        
        self.isPostGame = True
        
        playedSound = False
        playedSound2 = False

        chest_opened = False
        chest2_opened = False
        
        while self.giving_gun:
            background_image = pygame.image.load(os.path.join(base_directory, "assets/img/menuBackground.png")).convert()
            background_image = pygame.transform.scale(background_image, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
            self.screen.blit(background_image, (0,0))
            
            player1_chest_image = pygame.image.load(os.path.join(base_directory, "assets/img/character_animations/chest_opening.png"))
            player1_chest_image = pygame.transform.scale(player1_chest_image, (4000, 240))
            player2_chest_image = player1_chest_image
            player1_chest_image = pygame.transform.flip(player1_chest_image, True, False)
            
            player_weapon = pygame.transform.scale(self.player.weapon.image, (90, 270))
            player2_weapon = pygame.transform.scale(self.player2.weapon.image, (90, 270))
            
            if not chest_opened:
                self.screen.blit(player1_chest_image, (C.SCREEN_WIDTH/2 - 700, C.SCREEN_HEIGHT/2 + 150), (3600,0,400,240))
            elif chest_opened:
                current_time = pygame.time.get_ticks()
                if current_time - chest_last_time >= 70:
                    chest_current_frame += 1
                    chest_last_time = current_time
                if chest_current_frame < 10:
                    self.screen.blit(player1_chest_image, (C.SCREEN_WIDTH/2 - 700, C.SCREEN_HEIGHT/2 + 150), (4000 - (chest_current_frame*400),0,400,240))
                else:
                    self.screen.blit(player_weapon, (C.SCREEN_WIDTH/2 - 500, C.SCREEN_HEIGHT/2 - 120))
                    if not playedSound:
                        pygame.mixer.Sound.play(self.sword_get_sound)
                        playedSound = True
                    self.screen.blit(player1_chest_image, (C.SCREEN_WIDTH/2 - 700, C.SCREEN_HEIGHT/2 + 150), (0,0,400,240))

            if not chest2_opened:
                self.screen.blit(player2_chest_image, (C.SCREEN_WIDTH/2 + 300, C.SCREEN_HEIGHT/2 + 150), (0,0,400,240))
            elif chest2_opened:
                current_time = pygame.time.get_ticks()
                if current_time - chest2_last_time >= 70:
                    chest2_current_frame += 1
                    chest2_last_time = current_time
                if chest2_current_frame < 10:
                    self.screen.blit(player2_chest_image, (C.SCREEN_WIDTH/2 + 300, C.SCREEN_HEIGHT/2 + 150), ((chest2_current_frame*400),0,400,240))
                else:
                    self.screen.blit(player2_weapon, (C.SCREEN_WIDTH/2 + 410, C.SCREEN_HEIGHT/2 - 120))
                    if not playedSound2:
                        pygame.mixer.Sound.play(self.sword_get_sound)
                        playedSound2 = True
                    self.screen.blit(player2_chest_image, (C.SCREEN_WIDTH/2 + 300, C.SCREEN_HEIGHT/2 + 150), (3600,0,400,240))

            
            if chest_opened and chest2_opened:
                self.draw_text("Press ENTER to continue.", (255, 255, 255), 50, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 100)

            
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_x:
                        if not chest_opened:
                            pygame.mixer.Sound.play(self.chest_open_sound)
                            chest_opened = True
                    if event.key == K_PERIOD:
                        if not chest2_opened:
                            pygame.mixer.Sound.play(self.chest_open_sound)
                            chest2_opened = True
                    if event.key == K_RETURN:
                        if chest_opened and chest2_opened:
                            self.game_running = False
                            self.giving_gun = False
                            self.run_game()
            
            self.draw_text("press attack to open", (255, 255, 255), 75, C.SCREEN_WIDTH/2, 250)

            pygame.display.flip()
            
    def check_player_collisions(self):
        #if pygame.sprite.spritecollide(self.player, self.level.tile_group, False, pygame.sprite.collide_mask):
        if self.player.mask.overlap(self.player2.mask, (self.player.rect.x - self.player2.rect.x, self.player.rect.y - self.player2.rect.y)):
            pygame.display.set_caption("COLLISION DETECTED")
        else:
            pygame.display.set_caption("COLLISION NOT")

    def check_attack(self, player, pressed_keys):
        if player.canAttack:
            if(pressed_keys[player.keyBinds["left"]] or pressed_keys[player.keyBinds["right"]] or pressed_keys[player.keyBinds["up"]] or pressed_keys[player.keyBinds["down"]]):
                if(pressed_keys[player.keyBinds["left"]] and pressed_keys[player.keyBinds["attack"]]):
                    pygame.draw.rect(self.screen, self.color_select, pygame.Rect(player.rect.x - self.player.image.get_width(), player.rect.y, self.player.image.get_width(), self.player.image.get_height()))
                    player.canAttack = False
                if(pressed_keys[player.keyBinds["right"]] and pressed_keys[player.keyBinds["attack"]]):
                    pygame.draw.rect(self.screen, self.color_select, pygame.Rect(player.rect.x + self.player.image.get_width(), player.rect.y, self.player.image.get_width(), self.player.image.get_height()))
                    player.canAttack = False
                # if(pressed_keys[player.keyBinds["up"]] and pressed_keys[player.keyBinds["attack"]]):
                #     pygame.draw.rect(self.screen, self.color_select, pygame.Rect(player.rect.x, player.pos[1] - self.player.image.get_height(), self.player.image.get_width(), self.player.image.get_height()))
                # if(pressed_keys[player.keyBinds["down"]] and pressed_keys[player.keyBinds["attack"]] and player.isOnGround is False):
                #     pygame.draw.rect(self.screen, self.color_select, pygame.Rect(player.rect.x, player.pos[1] + self.player.image.get_height(), self.player.image.get_width(), self.player.image.get_height()))
            elif pressed_keys[player.keyBinds["attack"]]:
                if player.facingRight:
                    pygame.draw.rect(self.screen, self.color_select, pygame.Rect(player.rect.x + self.player.image.get_width(), player.rect.y, self.player.image.get_width(), self.player.image.get_height()))
                    # player.weapon.image = pygame.transform.rotate(player.weapon.image, -10)
                    player.canAttack = False
                else:
                    pygame.draw.rect(self.screen, self.color_select, pygame.Rect(player.rect.x - self.player.image.get_width(), player.rect.y, self.player.image.get_width(), self.player.image.get_height()))
                    #player.weapon.image = pygame.transform.rotate(player.weapon.image, 10)
                    player.canAttack = False

    def player_hit(self, player, isPlayer1):
        if not player.isInvincible:
            if player.isDamaged:
                pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(base_directory, "assets/sound/Hurt_grunt.wav"))).set_volume(0.2)
                if isPlayer1:
                    self.player_two_wins += 1
                    self.round_num += 1
                else:
                    self.player_one_wins += 1
                    self.round_num += 1

                if isPlayer1:
                    if self.isPostGame and self.player_two_wins is 5:
                        self.winner = 2
                        self.game_over()
                    else:
                        self.round_over(2)
                else:
                    if self.isPostGame and self.player_one_wins is 5:
                        self.winner = 1
                        self.game_over()
                    else:
                        self.round_over(1)
            else:
                pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(base_directory, "assets/sound/shieldbreak.mp3"))).set_volume(0.2)
                player.image = player.Damagedimage
                player.isInvincible = True
                player.isDamaged = True
                if isPlayer1:
                    self.invincibility_start = time.time()
                    self.damaged_start = time.time()
                    self.character_icon = self.character1_damaged_img
                else:
                    self.invincibility_start2 = time.time()
                    self.damaged_start2 = time.time()
                    self.character2_icon = self.character2_damaged_img
                