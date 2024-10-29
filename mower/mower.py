from nav import path

class Mower:
    """an object to describe a lawn mower.
    This class may be a hub of other objects which make up a mower"""
    def __init__(self, x: int = 0, y: int = 0, direction: int = 0):
        self.x = x
        self.y = y
        self.direction = direction # 0 = north, 90 = east, 180 = south, 270 = west
        self.path = path.Path()

if __name__ == "__main__":
    test_mower = Mower(y=3, direction=180)
    assert test_mower.x == 0
    assert test_mower.y == 3
    assert test_mower.direction == 180
    assert test_mower.path.get_path_length() == 0
    print("all Mower class tests passed")