# Import the pygame module
from select import select
from tkinter import Menu
import pygame
import CONSTANTS as C
from Player import Player
from Level import Level
from Weapons import *

# create a dictionary to store key presses for player 1 and player 2
key_presses_1 = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
}

key_presses_2 = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
}

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_RETURN,
    K_ESCAPE,
    K_SPACE,
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
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.RESIZABLE)
        
        # Instantiate player. Right now, this is just a rectangle.
        self.player = Player(key_presses_1, "assets/img/character.png", (200, 100), self.screen)
        self.player2 = Player(key_presses_2, "assets/img/character2.png", (C.SCREEN_WIDTH - 300, 100), self.screen)
        
        pygame.mouse.set_visible(False)

        pygame.display.set_caption("SWOASE ON SWOASE")
        icon = pygame.image.load("assets/img/capy.png")
        pygame.display.set_icon(icon)
        
        self.level = Level(C.LEVEL_MAP, self.screen, "assets/img/DefaultBackground.png")

        self.select_sound = pygame.mixer.Sound("assets/sound/Select.wav")
        self.select_sound.set_volume(0.3)

        self.menu_running = True
        self.game_running = False
        self.paused = False
        self.options_running = False
        self.pregame_running = False
        
        self.color_menu = (40, 40, 40)
        self.color_dos = (77, 77, 77)
        self.color_select = (255, 77, 112)
        self.color_default = (245, 244, 228)

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
            title_img = pygame.transform.scale(title_img,(700,200))
            self.screen.blit(title_img, (C.SCREEN_WIDTH/2-350, 100))
            
            
            self.draw_text("START", start_text_color, 50, C.SCREEN_WIDTH/2, 450)
            self.draw_text("OPTIONS", settings_text_color, 50, C.SCREEN_WIDTH/2, 550)
            self.draw_text("QUIT", quit_text_color, 50, C.SCREEN_WIDTH/2, 650)
            pygame.display.flip()

    def run_game(self):
        # Setup the level        
        self.game_running = True
        # Main loop
        while self.game_running:
            
            clock.tick(60) # limit fps to 60
            pressed_keys = pygame.key.get_pressed()
            self.player.move(pressed_keys)
            self.player2.move(pressed_keys)
            self.player.updatePos()
            self.player2.updatePos()
            
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
                    elif event.key == K_RETURN:
                        self.player2.dash(pressed_keys)
                    elif event.key == K_SPACE:
                        self.player.dash(pressed_keys)

            # Run the Level
            self.level.run()
            
            self.check_collisions()

            # Draw the player on the screen
            self.screen.blit(self.player.image, self.player.pos)
            self.screen.blit(self.player2.image, self.player2.pos)
            
            
            self.draw_text("IN LIFE EVEN WHEN TOLD NOT TO, SWOASE.", (255, 255, 255), 30, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)

            # Update the display
            pygame.display.flip()
            
    def pause_menu(self):
        current_selection = "resume"
        
        self.paused = True
        while self.paused:
            pygame.draw.rect(self.screen, self.color_dos, pygame.Rect(C.SCREEN_WIDTH/2 - 250, C.SCREEN_HEIGHT/2 - 250, 500, 500))
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
                        
            self.draw_text("RESUME", resume_text_color, 35, C.SCREEN_WIDTH/2, 250)
            self.draw_text("SETTINGS", settings_text_color, 35, C.SCREEN_WIDTH/2, 400)
            self.draw_text("RETURN TO MENU", quit_text_color, 35, C.SCREEN_WIDTH/2, 550)
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
            self.draw_text("Nathan Wand occasionally smells like cheese.", self.color_default, 40, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)
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
                            self.run_game()
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
            
    def check_collisions(self):
        #if pygame.sprite.spritecollide(self.player, self.level.tile_group, False, pygame.sprite.collide_mask):
        if self.player.mask.overlap(self.player2.mask, (self.player.pos[0] - self.player2.pos[0], self.player.pos[1] - self.player2.pos[1])):
            pygame.display.set_caption("COLLISION DETECTED")
        else:
            pygame.display.set_caption("COLLISION NOT")
