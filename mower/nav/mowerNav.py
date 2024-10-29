from enum import Enum

class CutPattern(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGLEFT = 2
    DIAGRIGHT = 3
    CHECKERS = 4
    DIAGCHECKERS = 5

class MowerNav:
    """A class to handle navigation for the mower.
    Will likely act as an interface between a Path object and a Mower object."""
    def __init__(self):
        pass