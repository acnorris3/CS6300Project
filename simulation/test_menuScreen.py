# simulation/test_menuScreen.py

import pygame
import pygame_gui
from menuScreen import menuScreen
from unittest import mock

def test_gui_elements():
    pygame.init()
    menu_screen = menuScreen()

    # Check that each button has the correct label
    button_labels_bottom = ["Start", "Pause", "Stop", "Quit"]
    for button, label in zip(menu_screen.buttons_bottom, button_labels_bottom):
        assert button.text == label, f"Expected bottom button label '{label}', but got '{button.text}'"

    button_labels_right = ["Create Lawn", "Load Lawn 1", "Load Lawn 2", "Load Lawn 3"]
    for button, label in zip(menu_screen.buttons_right, button_labels_right):
        assert button.text == label, f"Expected right button label '{label}', but got '{button.text}'"

    pygame.quit()