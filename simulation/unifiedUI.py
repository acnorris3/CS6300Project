import pygame
import pygame_gui
try:
    from menuScreen import menuScreen
    from pip_example_tiles import PIP_Example_Tiles
except ImportError:
    from simulation.menuScreen import menuScreen
    from simulation.pip_example_tiles import PIP_Example_Tiles
# Define colors (stub)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()
class UnifiedUI:
    """
    UnifiedUI is a class that wraps together the game and GUI components.
    Creates a window with a game screen on the top left and a menu along the bottom and right.
    The game screen currently contains a lawn and a mower.
    :param screen_width: The width of the window in pixels.
    :param screen_height: The height of the window in pixels.
    :param width_ratio: The fraction of the window width allocated to the game screen.
    :param height_ratio: The fraction of the window height allocated to the game screen.
    """
    def __init__(self, screen_width=800, screen_height=600, width_ratio=0.75, height_ratio=0.8):
        # Component objects
        self.game_screen = PIP_Example_Tiles(screen_width * width_ratio, screen_height * height_ratio) # THIS IS MODULAR, you may load different games here.
        self.menu_screen = menuScreen(screen_width, screen_height)

        # Screen dimensions
        self.WIDTH = screen_width
        self.HEIGHT = screen_height
        self.WIDTH_RATIO = width_ratio
        self.HEIGHT_RATIO = height_ratio

        # Set up the display
        window_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Lawn Mower Simulation")

        # Define the game and GUI surfaces (subcomponents of the main window)
        game_surface_width = int(self.WIDTH * self.WIDTH_RATIO)  # 75% of the screen width
        game_surface_height = int(self.HEIGHT * self.HEIGHT_RATIO) # 80% of the screen height
        self.game_surface = pygame.Surface((game_surface_width, game_surface_height))
        self.gui_surface = pygame.Surface(window_size, pygame.SRCALPHA)  # Supports transparency


    def main_loop(self): # Main game loop
        """
        Main game loop that handles events, updates, and rendering for the lawn mower simulation.

        The loop continuously processes user inputs, updates the game state, and renders the 
        game and GUI surfaces to the display until a quit event is detected or the mower 
        returns to the home position.

        Event Handling:
        - Exits the loop if a quit event is received from the window or the 'Quit' button is pressed.
        - Processes keyboard inputs to control the mower, and checks if the mower has returned home.
        - Handles button presses from the GUI, delegating specific actions to other methods.

        Rendering:
        - Updates the game surface by drawing the current state of the lawn.
        - Clears and redraws the GUI surface.
        - Combines the game and GUI surfaces onto the main screen.
        - Refreshes the display with updated content using pygame.display.flip().

        This function will terminate the program by calling pygame.quit() once the loop ends.
        """
        running = True
        while running:
            # Event handling (stub)
            for event in pygame.event.get():
                # CHECK FOR QUIT
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.game_screen.handle_keypress(event)
                    self.game_screen.update_grid()
                    if self.game_screen.mower_has_returned_home():
                        running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.menu_screen.buttons_bottom[3]:  # Quit button was pressed
                        running = False
                    # HANDLE ALL OTHER SCENARIOS
                    else: self.handle_button_press(event)

            # Pass events to Pygame GUI manager
            self.menu_screen.ui_manager.process_events(event)

            # --- Rendering ---
            self.game_screen.draw_lawn(self.game_surface)
            self.gui_surface.fill((0, 0, 0, 0))  # Clear with transparency
            self.menu_screen.draw_menu(self.gui_surface) # Draw the menu

            # Combine surfaces
            self.screen.fill(BLACK)  # Clear the screen
            self.screen.blit(self.game_surface)  # Load game in the GUI frame
            self.screen.blit(self.gui_surface)  # Overlay GUI

            # Update display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()

    def handle_button_press(self, event):
        """Currently just a stub, but as we add functionality to buttons not requiring access to the `running` variable, we can add it here."""
        if event.ui_element == self.menu_screen.buttons_bottom[3]:  # Quit button was pressed
                running = False  # Close the program
                # ^ This doesn't work because we're not in the main loop.