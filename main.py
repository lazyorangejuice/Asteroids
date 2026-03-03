from tokenize import group

import pygame
import pygame_menu
import sys
from constants import *
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from logger import log_event
from shot import Shot

print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")
pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.time.Clock()
pygame.display.set_caption("Asteroids")
pygame.font.init()
font = pygame.font.SysFont("Arial", 24)   
score = 0  
dt = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

def game_loop(updatable, drawable, asteroids, shots, player):
    global score, dt
    score = 0
    while True:
        screen.fill("black")   # Clear the screen with black
        text_surface = font.render(f"{score}", True, (255, 255, 255)) 
        screen.blit(text_surface, (10, 10))  # Draw the score on the screen
        for object in drawable:
            object.draw(screen)  # Draw the objects on the screen
        updatable.update(dt)  # Update the objects state based on input
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print ("game over")
                game_over_menu.enable()
                game_over_menu.mainloop(screen)
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += 10  # Increase score based on asteroid kind
                    asteroid.split()  # Remove the asteroid from the game and split it into smaller pieces
                    shot.kill()  # Remove the shot from the game
        pygame.display.flip()  # Update the display
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Handle events here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu.enable()  # Enable the pause menu
                    pause_menu.mainloop(screen)
                    pygame.event.clear()  # Show the pause menu when ESC is pressed
        pygame.time.Clock().tick(60)  # Limit to 60 FPS
        dt = pygame.time.Clock().tick(60) / 1000  # Get delta time in seconds

def main():
    Shot.containers = (shots, updatable, drawable)
    pygame.sprite.Group()  # Create a sprite group for updatable and drawable objects
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  # Create an asteroid field and add it to the group
    asteroidfield = AsteroidField()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Create a player instance at the center of the screen
    game_loop(updatable, drawable, asteroids, shots, player)  # Start the main game loop

def start_the_game():
    try:
        main()
    except StopIteration:
        # This catches our 'quit' and just returns to the menu loop
        pass

def restart_game():
    global score
    score = 0
    # Clear all active sprites so they don't carry over
    for group in [updatable, drawable, asteroids, shots]:
        group.empty()
    
    # Close the pause menu and start fresh
    pause_menu.disable()
    game_over_menu.disable()
    main() 

def quit_to_main():
    pause_menu.disable()  # Stop the pause menu
    game_over_menu.disable()  # Stop the game over menu
    for group in [updatable, drawable, asteroids, shots]:
        group.empty()
    raise StopIteration ("Returning to Main Menu") 



# 1. Initialize the menu
menu = pygame_menu.Menu("Asteroids", 400, 300, theme=pygame_menu.themes.THEME_DARK)

# 2. Add buttons (NOTICE: no parentheses after start_the_game)
menu.add.button("Start Game", start_the_game)
menu.add.button("Quit", pygame_menu.events.EXIT)

# 4. pause the game loop and show the menu
pause_menu = pygame_menu.Menu('Paused', 300, 250, theme=pygame_menu.themes.THEME_DARK)
pause_menu.add.button('Resume', pause_menu.disable)
pause_menu.add.button('Restart', restart_game)  # New Restart button
pause_menu.add.button('Quit to Main', quit_to_main)  # Go back to the main menu

#5. game over menu 
game_over_menu = pygame_menu.Menu('Game Over', 300, 250, theme=pygame_menu.themes.THEME_DARK)
game_over_menu.add.button('Restart', restart_game)  # New Restart button
game_over_menu.add.button('Quit to Main', quit_to_main)  # Go back to the main menu

# 3. Run the menu (this replaces your manual while loop)
if __name__ == "__main__":
    menu.mainloop(surface)