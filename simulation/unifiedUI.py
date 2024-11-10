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
        running = True
        while running:
            # Event handling (stub)
            for event in pygame.event.get():
                # CHECK FOR QUIT
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.game_screen.handle_keypress(event)
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