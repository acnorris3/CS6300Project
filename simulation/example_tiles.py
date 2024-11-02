import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from colors import colors
from lawn.lawn_states import LawnState
import csv

# Constants
WIDTH, HEIGHT = 800, 800


# Initialize Pygame
pygame.init()



# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mower Simulation")


# Load the lawn from CSV file
grid = []
with open('./lawn/example_lawn_1.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        grid.append([LawnState(int(cell)) for cell in row])
rows = len(grid)
cols = len(grid[0])


# Set width and height of the cells in the grid
cell_width = WIDTH // cols
cell_height = HEIGHT // rows


# Position of the mower
pos = (0, 0)


# Update position of the mower and update the status of the lawn
def update_grid():
    if grid[pos[0]][pos[1]] == LawnState.UNMOWED:
        grid[pos[0]][pos[1]] = LawnState.MOWED
        

# Draw the lawn
def draw_lawn():
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) == pos:
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

            pygame.draw.rect(screen, color, (col_index * cell_width, row_index * cell_height, cell_width, cell_height))

# Game Loop
running = True
fLeftStart = False # Keep track if mower has left the base
while running:
    screen.fill(colors["white"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and (pos[0] > 0):
                # Move mower up if not at the top edge
                pos = (pos[0] - 1, pos[1])
            
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (pos[0] < rows - 1):
                # Move mower down if not at the bottom edge
                pos = (pos[0] + 1, pos[1])

            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (pos[1] > 0):
                # Move mower left if not at the left edge
                pos = (pos[0], pos[1] - 1)
            
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (pos[1] < cols - 1):
                # Move mower right if not at the right edge
                pos = (pos[0], pos[1] + 1)

            
    if pos[0] > 0 or pos[1] > 0:
        # Mower has left the base
        fLeftStart = True

    if fLeftStart and (pos == (0, 0)):
        # Mower has returned to the base, end the simulation
        running = False
    
    update_grid()
    draw_lawn()
    pygame.display.update()

pygame.quit()