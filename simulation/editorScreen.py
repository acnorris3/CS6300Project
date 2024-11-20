import os
import csv
import sys
import pygame
import pygame_gui
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
try:
    from colors import colors
except ImportError:
    from simulation.colors import colors
from lawn.lawn_states import LawnState
from typing import List, Optional


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Editor:
    """
        This class creates a screen where a lawn can be created and saved.
        It handles changing the lawn to an editable lawn as well as the menu buttons on the bottom and right of the screen.
        The edited lawn can be saved at the end. The lawn is saved with the name including the current date and time.

    """
    def __init__(self, screen_width: int =800, screen_height:int=600, width_ratio:float=0.75, height_ratio:float=0.8, rows=6, cols=9):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.rows = rows
        self.cols = cols
        
        # Establishes cell sizing based the size of the screen 
        # and how many rows and cols given to constructor
        self.cell_width = int(self.screen_width * self.width_ratio // self.cols)
        self.cell_height = int(self.screen_height * self.height_ratio // self.rows)

        # Starts a grid where all cells are UNMOWED
        self.grid = [[LawnState.UNMOWED.value for _ in range(cols)] for _ in range(rows)]

        self.selected_tile: Optional[LawnState] = None # Used to tell what button the user selected (i.e. base, unmowed grass, rock, tree, etc.)

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.ui_manager = pygame_gui.UIManager((self.screen_width, self.screen_height))

        # Creates buttons for bottom and right side nav
        bottom_button_labels = ["Base", "Unmowed", "Mowed", "Tree", "Rock", "Concrete"]
        right_button_labels  = ["Save", "Main Menu"]
        self.buttons_bottom = self.create_buttons(bottom_button_labels, position='bottom')
        self.buttons_right = self.create_buttons(right_button_labels, position='right')
        

    def create_buttons(self, labels: List[str], position: str) -> List[pygame_gui.elements.UIButton]:
        """
        Creates buttons for the bottom and right navigation.
        :param labels: A list of strings representing the labels for the buttons.
        :param position: A string indicating the position of the buttons ('bottom' or 'right').
        :return: A list of UIButton objects created based on the provided labels and position.
        """
        
        
        buttons = []
        if position == 'bottom':
            button_width   = 80
            button_height  = 40
            button_spacing = 20
            button_y = self.screen_height - button_height - 10

            for i, label in enumerate(labels):
                button_x = 10 + i * (button_width + button_spacing)
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(button_x, button_y, button_width, button_height),
                    text=label,
                    manager=self.ui_manager
                )
                buttons.append(button)
        elif position=='right':
            button_width  = 150
            button_height = 40
            button_spacing      = 20
            button_x = self.screen_width - button_width - 10
            for i, label in enumerate(labels):
                button_y = 10 + i * (button_height + button_spacing)
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(button_x, button_y, button_width, button_height),
                    text=label,
                    manager=self.ui_manager
                )
                buttons.append(button)
            
        return buttons



    def draw_menu(self, gui_surface):
        """
        Draws the menu on the given GUI surface.
        This method fills the GUI surface with a transparent color, then draws two
        rectangular areas with a specified color. The first rectangle is drawn at the
        bottom of the screen, and the second rectangle is drawn on the right side of
        the screen. After drawing the rectangles, the UI manager is updated and the
        UI elements are drawn on the GUI surface. Finally, the display is updated
        to reflect the changes.
        Args:
            gui_surface (pygame.Surface): The surface on which the menu will be drawn.
        """
        gui_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(gui_surface, (150, 150, 150), (0,
                                                        self.screen_height * self.height_ratio,
                                                        self.screen_width,
                                                        self.screen_height * (1 - self.height_ratio)))
        pygame.draw.rect(gui_surface, (150, 150, 150), (self.screen_width * self.width_ratio,
                                                        0,
                                                        self.screen_width * (1 - self.width_ratio),
                                                        self.screen_height))
        
        self.ui_manager.update(0.01)
        self.ui_manager.draw_ui(gui_surface)
        pygame.display.flip()

    def handle_button_press(self, event):
        """
        Handles button press events and delegates the event to the appropriate handler
        based on the button's location.

        Args:
            event: The event object containing information about the button press,
                   including the UI element that was pressed.

        """
        if event.ui_element in self.buttons_bottom:
            self._handle_buttons_bottom(event)
        elif event.ui_element in self.buttons_right:
            self._handle_buttons_right(event)

    def _handle_buttons_bottom(self, event):
        """
        Handles the button click events at the bottom of the editor screen.

        This method maps the text of the clicked button to a corresponding LawnState
        and updates the selected tile state accordingly.

        Args:
            event: The event object containing information about the UI element that was clicked.

        Attributes:
            selected_tile: The state of the tile selected based on the button text.
        """
        button_text = event.ui_element.text
        text_to_state = {
            "Base": LawnState.BASE,
            "Unmowed": LawnState.UNMOWED,
            "Mowed": LawnState.MOWED,
            "Tree": LawnState.TREE,
            "Rock": LawnState.ROCK,
            "Concrete": LawnState.CONCRETE
        }
        self.selected_tile = text_to_state.get(button_text, None)
    
    def _handle_buttons_right(self, event):
        """
        Handles the right-side button click events in the editor screen.

        Args:
            event: The event object containing information about the UI element interaction.

        Actions:
            - If the button text is 'Save', it triggers the save method.
        """
        button_text = event.ui_element.text
        if button_text == 'Save':
            self.save()

    def handle_click(self, pos):
        """
        Handles a click event on the grid.
        Parameters:
        pos (tuple): A tuple containing the x and y coordinates of the click position.
        This method calculates the column and row in the grid based on the click position.
        If the click is within the bounds of the grid and a tile is selected, it updates
        the grid at the calculated position with the value of the selected tile.
        """
        col = round(pos[0] // self.cell_width)
        row = round(pos[1] // self.cell_height)

        if 0 <= col < self.cols and 0 <= row < self.rows and self.selected_tile:
            self.grid[row][col] = self.selected_tile.value

    def draw_lawn(self, screen):
        """
        Draws the lawn grid on the given screen.
        This method fills the screen with a white background and then iterates over
        the lawn grid to draw each cell with its corresponding color based on its state.
        Args:
            screen (pygame.Surface): The surface on which to draw the lawn grid.
        The lawn grid is represented by a 2D list (self.grid) where each cell has a value
        corresponding to a specific LawnState. The method maps these values to their respective
        LawnState and uses the state's color to draw the cell. If a cell's value does not match
        any LawnState, it is drawn in black.
        """
        screen.fill(colors["white"])

        value_to_state = {
            LawnState.UNMOWED.value: LawnState.UNMOWED,
            LawnState.MOWED.value: LawnState.MOWED,
            LawnState.TREE.value: LawnState.TREE,
            LawnState.ROCK.value: LawnState.ROCK,
            LawnState.CONCRETE.value: LawnState.CONCRETE,
            LawnState.BASE.value: LawnState.BASE
        }
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                state = value_to_state.get(cell, None)
                if state: 
                    color = state.color()
                else:
                    color = colors["black"]

                pygame.draw.rect(screen, color, (col_index * self.cell_width, row_index * self.cell_height, self.cell_width, self.cell_height))

    def save(self):
        """
        Saves the current grid to a CSV file in the 'lawns' directory.
        User is prompted to select the file name and location.
        Raises:
            Exception: If an error occurs while saving the grid.
        Prints:
            A message indicating the file path where the grid was saved or an error message if saving fails.
        """
        try:
            root = Tk()
            root.withdraw()

            directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lawns')
            file_path = asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")], initialdir=directory)
            root.destroy()

            if not file_path:
                print("Save operation cancelled.")
                self.display_success_message("Save cancelled.")
                return
            
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in self.grid:
                    writer.writerow(row)

            self.display_success_message("Grid saved successfully.")
            print(f"Grid saved to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            self.display_success_message("Error saving file. Please try again.")
            return
        
    
    def display_success_message(self, message):
        # Create a pop-up message using pygame_gui
        self.success_message = pygame_gui.elements.ui_text_box.UITextBox(
            html_text=message,
            relative_rect=pygame.Rect((self.screen_width // 2 - 100, self.screen_height // 2 - 50), (200, 100)),
            manager=self.ui_manager
        )
        # Display the message for a short duration
        pygame.time.set_timer(pygame.USEREVENT, 2000)

    def handle_keypress(self, event):
        pass    # Placeholder for now