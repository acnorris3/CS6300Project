import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from colors import colors
except ImportError:
    from simulation.colors import colors
from lawn.lawn_states import LawnState
import csv

class PIP_Example_Tiles:
    """The file /simulation/example_tiles.py, but modified to be compatible with the PIP version of the simulation."""
    def __init__(self, width=800, height=800):
        self.WIDTH = width
        self.HEIGHT = height

        self.fLeftStart = False # Keep track if mower has left the base

        # Load the lawn from CSV file
        self.grid = []
        with open('./lawn/example_lawn_1.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.grid.append([LawnState(int(cell)) for cell in row])
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        # Set width and height of the cells in the grid
        self.cell_width = self.WIDTH // self.cols
        self.cell_height = self.HEIGHT // self.rows

        # Position of the mower
        self.pos = (0, 0)

    # Update position of the mower and update the status of the lawn
    def update_grid(self):
        if self.grid[self.pos[0]][self.pos[1]] == LawnState.UNMOWED:
            self.grid[self.pos[0]][self.pos[1]] = LawnState.MOWED
            

    # Draw the lawn
    def draw_lawn(self, screen):
        screen.fill(colors["white"])
        for row_index, row in enumerate(self.grid):
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
        if (event.key == pygame.K_UP or event.key == pygame.K_w) and (self.pos[0] > 0):
            # Move mower up if not at the top edge
            self.pos = (self.pos[0] - 1, self.pos[1])
        
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (self.pos[0] < self.rows - 1):
            # Move mower down if not at the bottom edge
            self.pos = (self.pos[0] + 1, self.pos[1])

        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (self.pos[1] > 0):
            # Move mower left if not at the left edge
            self.pos = (self.pos[0], self.pos[1] - 1)
        
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (self.pos[1] < self.cols - 1):
            # Move mower right if not at the right edge
            self.pos = (self.pos[0], self.pos[1] + 1)
                
        if self.pos[0] > 0 or self.pos[1] > 0:
            # Mower has left the base
            self.fLeftStart = True

    def mower_has_returned_home(self) -> bool:
        if self.fLeftStart and (self.pos == (0, 0)):
            # Mower has returned to the base, end the simulation
            return True
        else:
            return False