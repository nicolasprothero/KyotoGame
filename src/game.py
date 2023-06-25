# Import the pygame module
from select import select
from tkinter import Menu
import time
import pygame
import CONSTANTS as C
from Player import Player
from Level import Level
from Weapons import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_x,
    K_z,
    K_PERIOD,
    K_COMMA,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

clock = pygame.time.Clock()

class Game():
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.FULLSCREEN)
        
        # Instantiate player. Right now, this is just a rectangle.
        self.players = pygame.sprite.Group()
        self.player = Player(C.key_presses_1, "assets/img/character.png", (C.SCREEN_WIDTH - 300, 100))
        self.players.add(self.player)
        self.player2 = Player(C.key_presses_2, "assets/img/character2.png", (C.SCREEN_WIDTH - 200, 100))
        self.players.add(self.player2)
        
        # fart = ThrustWeapon('assets/img/mario.png', (40, 60))
        # self.player2.changeWeapon(fart)
        
        pygame.mouse.set_visible(False)

        pygame.display.set_caption("WEAPONIZE")
        icon = pygame.image.load("assets/img/icon.png")
        pygame.display.set_icon(icon)
        
        self.level = Level(C.LEVEL_MAP, self.screen, "assets/img/DefaultBackground.png")

        self.select_sound = pygame.mixer.Sound("assets/sound/Select.wav")
        self.select_sound.set_volume(0.3)
        
        self.attack_sound = pygame.mixer.Sound('assets/sound/swoosh.wav')
        self.attack_sound.set_volume(0.3)

        self.menu_running = True
        self.game_running = False
        self.paused = False
        self.options_running = False
        self.pregame_running = False
        
        self.color_menu = (40, 40, 40)
        self.color_dos = (77, 77, 77)
        self.color_select = (255, 77, 112)
        self.color_default = (245, 244, 228)

        self.attack_start = time.time()
        self.attack_start2 = time.time()
        
        self.attacking_start = time.time()
        self.attacking_start2 = time.time()
            
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

    def draw_text(self, text, color, size, x, y):
        font = pygame.font.Font("assets/fonts/ThaleahFat.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
            
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
                            self.options_menu()
                        elif(current_selection == "quit"):
                            pygame.mixer.Sound.play(self.select_sound)
                            self.menu_running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.menu_running = False
            
            self.screen.fill(self.color_menu)
            # create a surface object, image is drawn on it.
            title_img = pygame.image.load("assets/img/title.png")
            title_img = pygame.transform.scale(title_img,(C.SCREEN_WIDTH * 0.6, ((C.SCREEN_WIDTH* 0.6)/3)))
            self.screen.blit(title_img, (C.SCREEN_WIDTH/2 - ((C.SCREEN_WIDTH* 0.6)/2), 100))
            
            
            self.draw_text("START", start_text_color, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 150)
            self.draw_text("OPTIONS", settings_text_color, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 300)
            self.draw_text("QUIT", quit_text_color, 80, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 450)
            pygame.display.flip()

    def run_game(self):
        # Setup the level        
        self.game_running = True
        # Main loop
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
                    self.screen.blit(self.player.slash_right_image, (self.player.rect.x + self.player.image.get_width(), self.player.rect.y))
                elif not self.player.attackRight:
                    self.screen.blit(self.player.slash_left_image, (self.player.rect.x - self.player.slash_left_image.get_width(), self.player.rect.y))
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
                    self.screen.blit(self.player2.slash_right_image, (self.player2.rect.x + self.player2.image.get_width(), self.player2.rect.y))
                elif not self.player2.attackRight:
                    self.screen.blit(self.player2.slash_left_image, (self.player2.rect.x - self.player2.slash_left_image.get_width(), self.player2.rect.y))
                if time.time() - self.attacking_start2 > 0.1:
                    self.player2.attacking = False
                    self.attacking_start2 = time.time()
            else:
                if self.player2.facingRight:
                    self.screen.blit(self.player2.weapon.image, (self.player2.rect.x + 5, self.player2.rect.y - 30))
                else:
                    self.screen.blit(self.player2.weapon.image, (self.player2.rect.x + 30, self.player2.rect.y - 30))

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


            pygame.display.flip()
            
    def pause_menu(self):
        current_selection = "resume"
        
        self.paused = True
        while self.paused:
            # pause_background = pygame.Surface((C.SCREEN_WIDTH/4, C.SCREEN_HEIGHT/2))
            # pause_background.set_alpha(50)
            # pause_background.fill((34,39,63)) #(34,39,63)
            # self.screen.blit(pause_background, (C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2))
            
            background_image = pygame.image.load("assets/img/DefaultBackground.png").convert()
            background_image = pygame.transform.scale(background_image, (C.SCREEN_WIDTH/4, C.SCREEN_HEIGHT/2))
            background_image.set_alpha(50)
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
            
            self.screen.fill(self.color_dos)
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
            elif(current_selection == "quit"):
                start_text_color = self.color_default
                quit_text_color = self.color_select
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
                            current_selection = "play"
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "play"):
                            pygame.mixer.Sound.play(self.select_sound)
                            current_selection = "quit"
                    elif event.key == K_RETURN:
                        if(current_selection == "play"):
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
            self.draw_text("PRE GAME MENU", self.color_default, 90, C.SCREEN_WIDTH/2, 150)
            self.draw_text("PLAY", start_text_color, 50, C.SCREEN_WIDTH/2, 400)
            self.draw_text("PRACTICE", (130,130,130), 50, C.SCREEN_WIDTH/2, 500)
            self.draw_text("ARMORY", (130,130,130), 50, C.SCREEN_WIDTH/2, 600)
            self.draw_text("RETURN TO MENU", quit_text_color, 50, C.SCREEN_WIDTH/2, 700)
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
                            self.run_game()
            self.screen.fill(self.color_menu)
            self.draw_text("CONTROLS", self.color_default, 90, C.SCREEN_WIDTH/2, 150)
            self.draw_text("PLAYER ONE:", self.color_default, 50, C.SCREEN_WIDTH/2 - 400, 400)
            self.draw_text("PLAYER TWO:", self.color_default, 50, C.SCREEN_WIDTH/2 + 400, 400)
            
            player1_controls_image = pygame.image.load("assets/img/player1Controls.png")
            player1_controls_image = pygame.transform.scale(player1_controls_image, (C.SCREEN_WIDTH/9, (((C.SCREEN_WIDTH/9)/3)*2)))
            self.screen.blit(player1_controls_image, (C.SCREEN_WIDTH/2 - 500, 500))
    
            player2_controls_image = pygame.image.load("assets/img/player2Controls.png")
            player2_controls_image = pygame.transform.scale(player2_controls_image, (C.SCREEN_WIDTH/9, (((C.SCREEN_WIDTH/9)/3)*2)))
            self.screen.blit(player2_controls_image, (C.SCREEN_WIDTH/2 + 300, 500))
            
            player1_2_controls_image = pygame.image.load("assets/img/player1_2Controls.png")
            player1_2_controls_image = pygame.transform.scale(player1_2_controls_image, (C.SCREEN_WIDTH/9, (((C.SCREEN_WIDTH/9)/3)*2)))
            self.screen.blit(player1_2_controls_image, (C.SCREEN_WIDTH/2 - 500, 800))
    
            player2_2_controls_image = pygame.image.load("assets/img/player2_2Controls.png")
            player2_2_controls_image = pygame.transform.scale(player2_2_controls_image, (C.SCREEN_WIDTH/9, (((C.SCREEN_WIDTH/9)/3)*2)))
            self.screen.blit(player2_2_controls_image, (C.SCREEN_WIDTH/2 + 300, 800))

            pygame.display.flip()
            
    def check_collisions(self):
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
