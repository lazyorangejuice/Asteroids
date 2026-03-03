import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

def start_the_game():
    # This function is called when the "Play" button is clicked
    # Add your game logic here
    print("Game Started!")

def game_loop():
    # Your main game loop will run here when the menu is not active
    pass

menu = pygame_menu.Menu('Welcome', 600, 400,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Play', start_the_game)
menu.add.button('Exit', pygame_menu.events.EXIT) # Built-in exit event

# The main loop of the application
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            break

    if menu.is_enabled():
        menu.update(events)
        menu.draw(surface)

    # You would typically have a game state check here to switch to game_loop()
    # For a simple escape menu, the menu itself handles events.
    
    pygame.display.update()

pygame.quit()
