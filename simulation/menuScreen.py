# This page lifted directly from https://pygame-menu.readthedocs.io/en/4.1.3/index.html
###
### WIP
###

import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((900, 600))

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    print("The game has now started!")
    # Do the job here !
    pass

menu = pygame_menu.Menu('Lawn Mower - Team Best', 900, 600,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :') #, default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
