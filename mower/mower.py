try:
    from mower.nav import path
except ImportError:
    from nav import path

class Mower:
    """an object to describe a lawn mower.
    This class may be a hub of other objects which make up a mower"""
    def __init__(self, x: int = 0, y: int = 0, direction: int = 0):
        self.x = x
        self.y = y
        self.direction = direction # 0 = north, 90 = east, 180 = south, 270 = west
        self.path = path.Path()
