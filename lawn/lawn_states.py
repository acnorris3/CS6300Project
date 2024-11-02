from enum import Enum

class LawnState(Enum):
    MOWER = -1
    BASE = 0
    UNMOWED = 1
    MOWED = 2
    ROCK = 3
    TREE = 4
    CONCRETE = 5