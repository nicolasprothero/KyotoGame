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
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
level = Level(C.LEVEL_MAP, screen, "src/DefaultBackground.webp")

pygame.display.set_caption("game")
icon = pygame.image.load("src/capy.jpeg")
pygame.display.set_icon(icon)

def draw_text(text, color, size, x, y):
    text_font = pygame.font.get_default_font()
    font = pygame.font.Font(text_font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    
def run_menu():
    start_text_color = (170, 255, 0)
    settings_text_color = (255, 255, 255)
    quit_text_color = (255, 255, 255)
    
    current_selection = "start"
    
    menu_running = True
    
    while menu_running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    menu_running = False
                elif event.key == K_w or event.key == K_UP:
                    if(current_selection == "settings"):
                        current_selection = "start"
                        start_text_color = (170, 255, 0)
                        settings_text_color = (255, 255, 255)
                    elif(current_selection == "quit"):
                        current_selection = "settings"
                        settings_text_color = (170, 255, 0)
                        quit_text_color = (255, 255, 255)
                elif event.key == K_s or event.key == K_DOWN:
                    if(current_selection == "start"):
                        current_selection = "settings"
                        settings_text_color = (170, 255, 0)
                        start_text_color = (255, 255, 255)
                    elif(current_selection == "settings"):
                        current_selection = "quit"
                        quit_text_color = (170, 255, 0)
                        settings_text_color = (255, 255, 255)
                elif event.key == K_RETURN:
                    if(current_selection == "start"):
                        run_game()
                    elif(current_selection == "quit"):
                         menu_running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                menu_running = False
        
        screen.fill((0, 0, 0))
        draw_text(" GAME", (255, 255, 255), 50, C.SCREEN_WIDTH/2, 50)
        draw_text("START", start_text_color, 50, C.SCREEN_WIDTH/2, 400)
        draw_text("SETTINGS", settings_text_color, 50, C.SCREEN_WIDTH/2, 550)
        draw_text("QUIT", quit_text_color, 50, C.SCREEN_WIDTH/2, 700)
        pygame.display.flip()

def run_game():
    # Instantiate player. Right now, this is just a rectangle.
    player = Player(key_presses_1)
    player2 = Player(key_presses_2)

    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
        
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    pause_menu()
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        clock = pygame.time.Clock()
        dt = clock.tick(60) # limit fps to 60
        pressed_keys = pygame.key.get_pressed()
        player.gravity()
        player.update(pressed_keys, dt)
        
        player2.gravity()
        player2.update(pressed_keys, dt)

        # Run the Level
        level.run()

        # Draw the player on the screen
        screen.blit(player.surf, player.rect)
        screen.blit(player2.surf, player2.rect)
        
        draw_text("IN LIFE EVEN WHEN TOLD NOT TO, SWOASE.", (255, 255, 255), 30, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2)

        # Update the display
        pygame.display.flip()
        
def pause_menu():
    paused = True
    
    while paused:
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(C.SCREEN_WIDTH/2 - 250, C.SCREEN_HEIGHT/2 - 250, 500, 500))
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    paused = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False
        pygame.display.flip()

run_menu()