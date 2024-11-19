from enum import Enum

class LawnState(Enum):
    MOWER = -1
    BASE = 0
    UNMOWED = 1
    MOWED = 2
    ROCK = 3
    TREE = 4
    CONCRETE = 5

    def color(self):
        colors = {
            LawnState.MOWER: (255, 0, 0), # Red
            LawnState.BASE: (0, 0, 255), # Blue
            LawnState.UNMOWED: (0, 128, 0), # Dark Green
            LawnState.MOWED: (144, 238, 144), # Light Green
            LawnState.ROCK: (139, 69, 19), # Brown
            LawnState.TREE: (154, 205, 50), # Yellow Green
            LawnState.CONCRETE: (169, 169, 169) # Dark Gray
        }
        return colors[self]

