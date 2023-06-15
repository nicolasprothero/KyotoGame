# Import the pygame module
from select import select
from tkinter import Menu
import pygame
import CONSTANTS as C
from Player import Player
from Level import Level

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

        pygame.display.set_caption("game")
        icon = pygame.image.load("assets/img/capy.jpeg")
        pygame.display.set_icon(icon)

        self.menu_running = True
        self.game_running = False
        self.paused = False
        self.options_running = False
        self.pregame_running = False

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
                start_text_color = (170, 255, 0)
                settings_text_color = (255, 255, 255)
                quit_text_color = (255, 255, 255)
            elif(current_selection == "settings"):
                start_text_color = (255, 255, 255)
                settings_text_color = (170, 255, 0)
                quit_text_color = (255, 255, 255)
            elif(current_selection == "quit"):
                start_text_color = (255, 255, 255)
                settings_text_color = (255, 255, 255)
                quit_text_color = (170, 255, 0)
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
                        elif(current_selection == "quit"):
                            current_selection = "settings"
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "start"):
                            current_selection = "settings"
                        elif(current_selection == "settings"):
                            current_selection = "quit"
                    elif event.key == K_RETURN:
                        if(current_selection == "start"):
                            self.menu_running = False
                            self.pregame_menu()
                        if(current_selection == "settings"):
                            self.options_menu()
                        elif(current_selection == "quit"):
                            self.menu_running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.menu_running = False
            
            self.screen.fill((0, 0, 0))
            self.draw_text("SWOASE ESAOWS", (255, 255, 255), 90, C.SCREEN_WIDTH/2, 150)
            self.draw_text("START", start_text_color, 50, C.SCREEN_WIDTH/2, 450)
            self.draw_text("OPTIONS", settings_text_color, 50, C.SCREEN_WIDTH/2, 550)
            self.draw_text("QUIT", quit_text_color, 50, C.SCREEN_WIDTH/2, 650)
            pygame.display.flip()

    def run_game(self):
        # Instantiate player. Right now, this is just a rectangle.
        player = Player(key_presses_1, (0, 0), self.screen)
        player2 = Player(key_presses_2, (C.SCREEN_WIDTH - 50, 0), self.screen)

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.w, event.h
                scaling_factor_width = current_width / C.SCREEN_WIDTH
                scaling_factor_width = current_height / C.SCREEN_HEIGHT

        scaled_screen = pygame.transform.scale(self.screen, (current))

        # Setup the level
        level = Level(C.LEVEL_MAP, self.screen, "assets/img/DefaultBackground.webp")
        
        self.game_running = True
        # Main loop
        while self.game_running:
            
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.pause_menu()

            clock.tick(60) # limit fps to 60
            pressed_keys = pygame.key.get_pressed()
            player.move(pressed_keys)
            player2.move(pressed_keys)
            player.updatePos()
            player2.updatePos()
        
            # Run the Level
            level.run()

            # Draw the player on the screen
            self.screen.blit(player.image, player.pos)
            self.screen.blit(player2.image, player2.pos)
            
            self.draw_text("IN LIFE EVEN WHEN TOLD NOT TO, SWOASE.", (255, 255, 255), 30, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)

            # Update the display
            pygame.display.flip()
            
    def pause_menu(self):
        current_selection = "resume"
        
        self.paused = True
        
        while self.paused:
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(C.SCREEN_WIDTH/2 - 250, C.SCREEN_HEIGHT/2 - 250, 500, 500))
            # Check for QUIT event. If QUIT, then set running to false.    
            if(current_selection == "resume"):
                resume_text_color = (170, 255, 0)
                settings_text_color = (255, 255, 255)
                quit_text_color = (255, 255, 255)
            elif(current_selection == "settings"):
                resume_text_color = (255, 255, 255)
                settings_text_color = (170, 255, 0)
                quit_text_color = (255, 255, 255)
            elif(current_selection == "quit"):
                resume_text_color = (255, 255, 255)
                settings_text_color = (255, 255, 255)
                quit_text_color = (170, 255, 0)
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.paused = False
                    elif event.key == K_w or event.key == K_UP:
                        if(current_selection == "settings"):
                            current_selection = "resume"
                        elif(current_selection == "quit"):
                            current_selection = "settings"
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "resume"):
                            current_selection = "settings"
                        elif(current_selection == "settings"):
                            current_selection = "quit"
                    elif event.key == K_RETURN:
                        if(current_selection == "resume"):
                            self.paused = False
                        if(current_selection == "quit"):
                            self.game_running = False
                            self.paused = False
                            self.menu_running = True
                        
            self.draw_text("RESUME", resume_text_color, 25, C.SCREEN_WIDTH/2, 250)
            self.draw_text("SETTINGS", settings_text_color, 25, C.SCREEN_WIDTH/2, 400)
            self.draw_text("RETURN TO MENU", quit_text_color, 25, C.SCREEN_WIDTH/2, 550)
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
            
            self.screen.fill((100, 100, 100))
            self.draw_text("OPTIONS", (255, 255, 255), 75, C.SCREEN_WIDTH/2, 100)
            self.draw_text("Nathan Wand occasionally smells like cheese.", (255, 255, 255), 40, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)
            pygame.display.flip()
            
    def pregame_menu(self):
        current_selection = "play"
        
        self.pregame_running = True
        
        while self.pregame_running:
            if(current_selection == "play"):
                start_text_color = (170, 255, 0)
                settings_text_color = (255, 255, 255)
                quit_text_color = (255, 255, 255)
            elif(current_selection == "practice"):
                start_text_color = (255, 255, 255)
                settings_text_color = (170, 255, 0)
                quit_text_color = (255, 255, 255)
            elif(current_selection == "quit"):
                start_text_color = (255, 255, 255)
                settings_text_color = (255, 255, 255)
                quit_text_color = (170, 255, 0)
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
                            current_selection = "play"
                    elif event.key == K_s or event.key == K_DOWN:
                        if(current_selection == "play"):
                            current_selection = "quit"
                    elif event.key == K_RETURN:
                        if(current_selection == "play"):
                            self.pregame_running = False
                            self.run_game()
                        # elif(current_selection == "practice"):
                            # self.menu_running = False
                        elif(current_selection == "quit"):
                            self.pregame_running = False
                            self.run_menu()
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.pregame_running = False
                    self.run_menu()
            
            self.screen.fill((0, 0, 0))
            self.draw_text("PRE GAME MENU", (255, 255, 255), 90, C.SCREEN_WIDTH/2, 150)
            self.draw_text("PLAY", start_text_color, 50, C.SCREEN_WIDTH/2, 450)
            self.draw_text("PRACTICE", (130,130,130), 50, C.SCREEN_WIDTH/2, 550)
            self.draw_text("RETURN TO MENU", quit_text_color, 50, C.SCREEN_WIDTH/2, 650)
            pygame.display.flip()