import pygame
import pygame_gui

class AbstractMenuScreen:
    def __init__(self, screen_width=800, screen_height=600, width_ratio=0.75, height_ratio=0.8):
        """
        Initializes a menu screen with the specified screen dimensions and layout configuration.

        This constructor sets up the Pygame display window and initializes the GUI manager. It also
        defines the layout for any buttons, creating buttons with specified
        labels and adding them to their respective lists for later access by downstream consumers.
        This author recommends adding buttons here via pygame_gui such that they can be accessed in the main loop

        :param screen_width: The width of the screen in pixels.
        :param screen_height: The height of the screen in pixels.
        :param width_ratio: The fraction of the screen width allocated to the main display area.
        :param height_ratio: The fraction of the screen height allocated to the main display area.
        """
        pass


    def draw_menu(self, gui_surface):
        """
        Draws the menu onto the given surface, which should be a Pygame Surface created with the SRCALPHA flag (allowing transparency).

        The method first clears the surface with a transparent fill, then draws any backgrounds for the bottom and right buttons.
        Finally, it updates the Pygame GUI manager and draws the buttons onto the surface.

        :param gui_surface: A Pygame Surface (with the SRCALPHA flag set).
        """
        
