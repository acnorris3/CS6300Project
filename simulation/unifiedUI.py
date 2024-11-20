import os
import pygame
import pygame_gui
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
try:
    from menuScreen import menuScreen
    from pip_example_tiles import PIP_Example_Tiles
    from editorScreen import Editor
except ImportError:
    from simulation.menuScreen import menuScreen
    from simulation.pip_example_tiles import PIP_Example_Tiles
    from simulation.editorScreen import Editor
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
    def __init__(self, game_instance, menu_instance, screen_width=800, screen_height=600, width_ratio=0.75, height_ratio=0.8):
        # Component objects
        self.pip_example = PIP_Example_Tiles(screen_width * width_ratio, screen_height * height_ratio)
        self.editor = Editor(screen_width, screen_height, width_ratio, height_ratio)
        self.main_menu = menuScreen(screen_width, screen_height, width_ratio, height_ratio)

        self.game_screen = self.pip_example # THIS IS MODULAR, you may load different games here.
        self.menu_screen = self.main_menu

        # self.game_screen = game_instance(screen_width * width_ratio, screen_height * height_ratio) # THIS IS MODULAR, you may load different games here.
        # self.menu_screen = menu_instance(screen_width, screen_height, width_ratio, height_ratio)
        

        self.current_screen = 'game'


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

    def open_file_explorer(self):
        root = Tk()
        root.withdraw()
        root_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = askopenfilename(initialdir=root_directory, title="Select a file", filetypes=[("CSV files", "*.csv")])
        root.destroy()
        return file_path


    def start_move(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)
        time.sleep(0.25)

    def auto_move(self):
        print(self.game_screen.pos)
        if self.game_screen.check_lawn(self.game_screen.pos[0], self.game_screen.pos[1] + 1) and self.game_screen.pos[1] < self.game_screen.cols - 1:
            self.start_move(pygame.K_d)
        elif self.game_screen.check_lawn(self.game_screen.pos[0] + 1, self.game_screen.pos[1]) and self.game_screen.pos[0] < self.game_screen.rows - 1:
            self.start_move(pygame.K_s)
        elif self.game_screen.check_lawn(self.game_screen.pos[0], self.game_screen.pos[1] - 1) and self.game_screen.pos[1] > - 1:
            self.start_move(pygame.K_a)
        elif self.game_screen.check_lawn(self.game_screen.pos[0] - 1, self.game_screen.pos[1]) and self.game_screen.pos[0] > -1:
            self.start_move(pygame.K_w)
        # Optimization will go here
        # TODO: Have default movements be based on home position
        else:
            self.start_move(pygame.K_w)
            # This results in some weird movement
            if self.game_screen.pos[0] == 0:
                self.start_move(pygame.K_a)         



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
                    self.auto_move()
                    # self.game_screen.update_lawn()
                    if (self.current_screen == 'game') and self.game_screen.mower_has_returned_home():
                        running = False 
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.current_screen == 'game':
                        if event.ui_element == self.menu_screen.buttons_bottom[3]:  # Quit button was pressed
                            running = False
                        elif event.ui_element == self.menu_screen.buttons_right[0]: # Create new lawn button pressed
                            self.current_screen = 'editor'
                            self.game_screen = self.editor
                            self.menu_screen = self.editor
                        elif event.ui_element == self.menu_screen.buttons_right[4]: # Load user lawn
                            file_path = self.open_file_explorer()
                            if file_path:
                                print(file_path)
                    elif self.current_screen == 'editor':
                        if event.ui_element.text == "Main Menu":
                            self.current_screen = 'game'
                            self.game_screen = self.pip_example
                            self.menu_screen = self.main_menu

                    # HANDLE ALL OTHER SCENARIOS
                    else: self.menu_screen.handle_button_press(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == 'editor':
                        self.game_screen.handle_click(event.pos)

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