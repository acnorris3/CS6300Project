class LawnMap:
    """An object to describe a lawn map.
    Intended to be the result of LawnFileParser and then used in the Lawn class"""
    def __init__(self, width, height):
        self.width = width
        self.height = height