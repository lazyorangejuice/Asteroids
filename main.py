import pygame
import sys
from constants import *
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from logger import log_event


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group() 
    pygame.sprite.Group()  # Create a sprite group for updatable and drawable objects
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  # Create an asteroid field and add it to the group
    asteroidfield = AsteroidField()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Create a player instance at the center of the screen
    while True:
        
        screen.fill("black")   # Clear the screen with black
        for object in drawable:
            object.draw(screen)  # Draw the objects on the screen
        updatable.update(dt)  # Update the objects state based on input
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print ("game over")
                sys.exit()
        pygame.display.flip()  # Update the display
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Handle events here
        pygame.time.Clock().tick(60)  # Limit to 60 FPS
        dt = pygame.time.Clock().tick(60) / 1000  # Get delta time in seconds
        
        
    
    
    
    

if __name__ == "__main__":
    main()

