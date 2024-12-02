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

        # variables for tracking state
        self.paused = False

    def open_file_explorer(self):
        root = Tk()
        root.withdraw()
        root_directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(root_directory, '..', 'lawns', 'custom')
        file_path = askopenfilename(initialdir=directory, title="Select a file", filetypes=[("CSV files", "*.csv")])
        root.destroy()
        return file_path

    
    def start_move(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)
        time.sleep(0.25)

    def find_unmowed_lawn(self, pos, lawn_list):
        reduced_list = []
        for lawn in lawn_list:
            if pos[0] == lawn[0] or pos[1] == lawn[1]:
                reduced_list.append(lawn)
        tar_pos = pos
        if reduced_list:
            target = 100000            
            for lawn in reduced_list:
                y = pos[0] - lawn[0]
                x = pos[1] - lawn[1]
                if y + x < target:
                    target = y + x
                    tar_pos = lawn
        if not reduced_list:
            target = 100000            
            for lawn in lawn_list:
                y = pos[0] - lawn[0]
                x = pos[1] - lawn[1]
                if y + x < target:
                    target = y + x
                    tar_pos = lawn
        if not lawn_list: 
            tar_pos = (0,0)
        print(lawn_list)
        if tar_pos[0] < pos[0] and self.game_screen.avoid_collision(pos[0] - 1, pos[1]):
            return "w"      
        if tar_pos[0] > pos[0] and self.game_screen.avoid_collision(pos[0] + 1, pos[1]):
            return "s"
        if tar_pos[1] > pos[1] and self.game_screen.avoid_collision(pos[0], pos[1] + 1):
            return "d"        
        if tar_pos[1] < pos[1] and self.game_screen.avoid_collision(pos[0], pos[1] - 1):
            return "a"
        if self.game_screen.avoid_collision(pos[0] - 1, pos[1]) and self.game_screen.valid_move(pos[0] - 1, pos[1]):
            return "w"
        if self.game_screen.avoid_collision(pos[0], pos[1] + 1) and self.game_screen.valid_move(pos[0], pos[1] + 1):
            return "d"     
        if self.game_screen.avoid_collision(pos[0], pos[1] - 1) and self.game_screen.valid_move(pos[0], pos[1] - 1):
            return "a"
        if self.game_screen.avoid_collision(pos[0] + 1, pos[1]) and self.game_screen.valid_move(pos[0] + 1, pos[1]):
            return "s"
         
    
    def check_neighbor_squares(self, pos):
        if self.game_screen.check_lawn(pos[0], pos[1] + 1) and self.game_screen.avoid_collision(pos[0], pos[1] + 1):
            return "d"
        if self.game_screen.check_lawn(pos[0] + 1, pos[1]) and self.game_screen.avoid_collision(pos[0] + 1, pos[1]):
            return "s"
        if self.game_screen.check_lawn(pos[0], pos[1] - 1) and self.game_screen.avoid_collision(pos[0], pos[1] - 1):
            return "a"
        if self.game_screen.check_lawn(pos[0] - 1, pos[1]) and self.game_screen.avoid_collision(pos[0] - 1, pos[1]):
            return "w"        
        
        lawn = self.game_screen.check_entire_lawn()
        return self.find_unmowed_lawn(self.game_screen.pos, lawn)
            


    def auto_move(self):        
        if self.check_neighbor_squares(self.game_screen.pos) == 'd':
            self.start_move(pygame.K_d)
            
        if self.check_neighbor_squares(self.game_screen.pos) == 's':
            self.start_move(pygame.K_s)
        
        if self.check_neighbor_squares(self.game_screen.pos) == 'a':
            self.start_move(pygame.K_a)
            
        if self.check_neighbor_squares(self.game_screen.pos) == 'w':
            self.start_move(pygame.K_w)

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
                if event.type == pygame.KEYDOWN and not self.paused:                                  
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
                        elif event.ui_element == self.menu_screen.buttons_right[1]: # Load lawn 1
                            self.game_screen = PIP_Example_Tiles(self.WIDTH * self.WIDTH_RATIO, self.HEIGHT * self.HEIGHT_RATIO, 'lawns/preset/lawn1.csv')
                            self.menu_screen = menuScreen(self.WIDTH, self.HEIGHT, self.WIDTH_RATIO, self.HEIGHT_RATIO)  # Reinitialize menuScreen
                            self.display_success_message("Lawn 1 loaded successfully!")
                        elif event.ui_element == self.menu_screen.buttons_right[2]: # Load lawn 2
                            self.game_screen = PIP_Example_Tiles(self.WIDTH * self.WIDTH_RATIO, self.HEIGHT * self.HEIGHT_RATIO, 'lawns/preset/lawn2.csv')
                            self.menu_screen = menuScreen(self.WIDTH, self.HEIGHT, self.WIDTH_RATIO, self.HEIGHT_RATIO)  # Reinitialize menuScreen
                            self.display_success_message("Lawn 2 loaded successfully!")
                        elif event.ui_element == self.menu_screen.buttons_right[3]: # Load lawn 3
                            self.game_screen = PIP_Example_Tiles(self.WIDTH * self.WIDTH_RATIO, self.HEIGHT * self.HEIGHT_RATIO, 'lawns/preset/lawn3.csv')
                            self.menu_screen = menuScreen(self.WIDTH, self.HEIGHT, self.WIDTH_RATIO, self.HEIGHT_RATIO)  # Reinitialize menuScreen
                            self.display_success_message("Lawn 3 loaded successfully!")
                        elif event.ui_element == self.menu_screen.buttons_right[4]: # Load user lawn
                            file_path = self.open_file_explorer()
                            if file_path:
                                self.game_screen = PIP_Example_Tiles(self.WIDTH * self.WIDTH_RATIO, self.HEIGHT * self.HEIGHT_RATIO, file_path)
                                self.menu_screen = menuScreen(self.WIDTH, self.HEIGHT, self.WIDTH_RATIO, self.HEIGHT_RATIO)  # Reinitialize menuScreen
                                self.display_success_message("User lawn loaded successfully!")
                        else:
                            self.handle_button_press(event)
                                
                    elif self.current_screen == 'editor':
                        if event.ui_element.text == "Main Menu":
                            self.current_screen = 'game'
                            self.game_screen = self.pip_example
                            self.menu_screen = self.main_menu
                        else: 
                            self.menu_screen.handle_button_press(event)

                    # HANDLE ALL OTHER SCENARIOS
                    else: self.menu_screen.handle_button_press(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == 'editor':
                        self.game_screen.handle_click(event.pos)

            if event.type == pygame.USEREVENT:
                if hasattr(self, 'success_message'):
                    self.success_message.kill()
                    del self.success_message

            # Pass events to Pygame GUI manager
            self.menu_screen.ui_manager.process_events(event)

            # --- Rendering ---
            
            self.gui_surface.fill((0, 0, 0, 0))  # Clear with transparency
            self.menu_screen.draw_menu(self.gui_surface) # Draw the menu
            self.game_screen.draw_lawn(self.game_surface)

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
        if event.ui_element == self.menu_screen.buttons_bottom[0]:  # Start button was pressed
            self.paused = False
            self.auto_move()
        if event.ui_element == self.menu_screen.buttons_bottom[1]:  # Pause button was pressed
            self.paused = True  # Close the program
        if event.ui_element == self.menu_screen.buttons_bottom[2]:  # Stop button was pressed
            pygame.quit()
            UnifiedUI(game_instance=PIP_Example_Tiles, menu_instance=menuScreen).main_loop()
        if event.ui_element == self.menu_screen.buttons_bottom[3]:  # Quit button was pressed
            raise NotImplementedError("The `quit` button shouldn't be handled by the function `handle_button_press`.")

    def display_success_message(self, message):
        # Create a pop-up message using pygame_gui
        self.success_message = pygame_gui.elements.ui_text_box.UITextBox(
            html_text=message,
            relative_rect=pygame.Rect((self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50), (200, 100)),
            manager=self.menu_screen.ui_manager
        )
        # Display the message for a short duration
        pygame.time.set_timer(pygame.USEREVENT, 2000)