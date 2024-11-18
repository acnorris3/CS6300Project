import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from colors import colors
    from game_screen.abstract_game_screen import AbstractGameScreen
except ImportError:
    from simulation.colors import colors
    from simulation.game_screen.abstract_game_screen import AbstractGameScreen
import csv
from lawn.lawn import Lawn
from lawn.lawn_states import LawnState
from mower.metrics.Metrics import Metrics

# Initialize Pygame and set up asset paths
pygame.init()
ASSET_PATH = "./assets/"

class MowerSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, pos):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update_position(self, new_pos):
        self.rect.topleft = new_pos

class PIP_Example_Tiles(AbstractGameScreen):
    """The file /simulation/example_tiles.py, but modified to be compatible with the PIP version of the simulation."""
    def __init__(self, width=800, height=800):
        self.WIDTH = width
        self.HEIGHT = height
        self.metrics = Metrics()

        self.fLeftStart = False # Keep track if mower has left the base

        # Load the lawn from CSV file
        self.grid = Lawn()
        self.grid.load_from_file('./lawn/example_lawn_1.csv')
        self.rows = self.grid.height
        self.cols = self.grid.width

        # Set width and height of the cells in the grid
        self.cell_width = self.WIDTH // self.cols
        self.cell_height = self.HEIGHT // self.rows

        # Load sprites for lawn tiles and mower
        self.tile_sprites = {
            LawnState.UNMOWED: pygame.image.load(os.path.join(ASSET_PATH, "unmowed.png")).convert_alpha(),
            LawnState.MOWED: pygame.image.load(os.path.join(ASSET_PATH, "mowed.png")).convert_alpha(),
            LawnState.TREE: pygame.image.load(os.path.join(ASSET_PATH, "tree.png")).convert_alpha(),
            LawnState.ROCK: pygame.image.load(os.path.join(ASSET_PATH, "rock.png")).convert_alpha(),
            LawnState.CONCRETE: pygame.image.load(os.path.join(ASSET_PATH, "concrete.png")).convert_alpha(),
            LawnState.BASE: pygame.image.load(os.path.join(ASSET_PATH, "base.png")).convert_alpha(),
        }
        self.mower_sprite = MowerSprite(os.path.join(ASSET_PATH, "mower.png"), (0, 0))

        # Position of the mower
        self.pos = (0, 0)

    # Update position of the mower and update the status of the lawn
    def update_lawn(self, new_position):
        """
        Update the grid based on the current position of the mower.

        If the current position of the mower is on an unmowed lawn cell, 
        change the state of that cell to mowed.
        """
        row, col = new_position
        
        if self.grid.get_tile(col, row) == LawnState.UNMOWED:
            self.grid.update_tile(col, row, LawnState.MOWED)
            if (self.grid.get_tile(col, row) != LawnState.BASE):
                self.metrics.add_mowed()
        else:
            if (self.grid.get_tile(col, row) != LawnState.BASE):
                self.metrics.add_overlap()

            
    def check_collision(self, new_position):
        """
        Check if the mower has collided with an object on the lawn.

        :param new_position: The new position of the mower.
        :return: True if the mower has collided with an object, False otherwise.
        """
        
        row, col = new_position
        if self.grid.get_tile(col, row) in [LawnState.TREE, LawnState.ROCK]:
            print('Collision!')
            self.metrics.add_collision()
            return True
        return False
    
    def move_mower(self, direction):
        """
        Move the mower in the given direction, if a valid move.

        :param direction: The direction in which the mower should move."""
        new_position = self.pos 

        if direction == 'UP' and self.pos[0] > 0:
            new_position = (self.pos[0] - 1, self.pos[1])
        elif direction == 'DOWN' and self.pos[0] < self.rows - 1:
            new_position = (self.pos[0] + 1, self.pos[1])
        elif direction == 'LEFT' and self.pos[1] > 0:
            new_position = (self.pos[0], self.pos[1] - 1)
        elif direction == 'RIGHT' and self.pos[1] < self.cols - 1:
            new_position = (self.pos[0], self.pos[1] + 1)
        

        if new_position != self.pos and not self.check_collision(new_position):
            self.update_lawn(new_position)
            self.pos = new_position

    # Draw the lawn
    def draw_lawn(self, screen):
        """
        Draw the lawn onto the given screen.

        This function goes through each cell in the grid, and based on the state of the cell,
        draws a rectangle of the appropriate color onto the screen. The mower's position is
        drawn as red, unmowed lawn is drawn as dark green, mowed lawn is light green, trees
        are yellow, rocks are brown, concrete is grey, and the base is blue.

        :param screen: The surface to draw the lawn onto. At time of writing, this should be defined in a UnifiedUI object.
        """
        screen.fill(colors["white"])
        for row_index, row in enumerate(self.grid.raw):
            for col_index, cell in enumerate(row):
                if (row_index, col_index) == self.pos:
                    color = colors["red"]
                elif cell == LawnState.UNMOWED:
                    color = colors["dark_green"]
                elif cell == LawnState.MOWED:
                    color = colors["light_green"]
                elif cell == LawnState.TREE:
                    color = colors["yellow"]
                elif cell == LawnState.ROCK:
                    color = colors["brown"]
                elif cell == LawnState.CONCRETE:
                    color = colors["grey"]
                elif cell == LawnState.BASE:
                    color = colors["blue"]
                else:
                    color = colors["black"]

                pygame.draw.rect(screen, color, (col_index * self.cell_width, row_index * self.cell_height, self.cell_width, self.cell_height))

    def handle_keypress(self, event):
        """
        Handles keypress events.

        This function updates the position of the mower based on user input from the keyboard.
        The mower can move up, down, left, or right if the corresponding key is pressed.
        Checks for valid destination of the mower.

        If the mower has left the base, it keeps track of that fact.

        :param event: The event object passed in from the event loop.
        :return: None
        """
        if (event.key == pygame.K_UP or event.key == pygame.K_w):
            self.move_mower('UP')
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
            self.move_mower('DOWN')
        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (self.pos[1] > 0):
            self.move_mower('LEFT')
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (self.pos[1] < self.cols - 1):
            self.move_mower('RIGHT')

        if self.pos[0] > 0 or self.pos[1] > 0:
            # Mower has left the base
            self.fLeftStart = True

    
    
    def mower_has_returned_home(self) -> bool:
        """
        Returns True if the mower has previously left and is now back at the base, indicating the simulation should end;
        otherwise, it returns False.

        :return: A boolean indicating if the mower has returned to the base.
        """
        if self.fLeftStart and (self.pos == (0, 0)):
            # Mower has returned to the base, end the simulation
            print("\n\nMetrics")
            print("Battery remaining: {}%".format(self.metrics.get_battery()))
            print("# of tiles Mowed: ", self.metrics.metrics['mowed'])
            print("# of Collisions: ", self.metrics.metrics['collisions'])
            print("Percentage of overlap: {}%".format(round(self.metrics.calcualte_overlap_vs_seen() * 100)))
            print("Efficiency: {}%".format(round(self.metrics.calculate_efficiency_ratio() * 100)))
            return True
        else:
            return False