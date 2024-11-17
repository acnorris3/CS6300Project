import csv
from typing import List
try: 
    from lawn_states import LawnState
except ImportError:
    from lawn.lawn_states import LawnState

class Lawn:
    """The numerical representation of the map over which a mower moves.
    Uses the LawnState class to describe the different available states of a lawn tile e.g. UNMOWED."""
    def __init__(self, raw_lawn: List[List[LawnState]] = None):
        self.raw = raw_lawn
        if raw_lawn is not None:
            self.width = len(raw_lawn[0])
            self.height = len(raw_lawn)
        
    def update_tile(self, x, y, value):
        """
        Update the state of a tile in the lawn.

        :param x: The x-coordinate of the tile to update.
        :param y: The y-coordinate of the tile to update.
        :param value: The new state of the tile.
        """
        self.raw[y][x] = value

    def get_tile(self, x, y) -> int:
        """
        Get the state of a tile in the lawn.

        :param x: The x-coordinate of the tile to get.
        :param y: The y-coordinate of the tile to get.
        :return: The state of the tile at the given coordinates.
        """
        return self.raw[y][x]

    def load_from_file(self, file_path, overwrite=False):
        """
        Load the lawn from a CSV file.

        :param file_path: The path to the file containing the lawn.
        :param overwrite: If True, overwrite any existing lawn. If False, raise an error if a lawn already exists.
        :raises ValueError: If this lawn already exists and overwrite is False
        """
        if self.raw is not None and not overwrite:
            raise ValueError("Attempting to overwrite existing lawn")
        self.raw = [] # Clear existing lawn
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.raw.append([LawnState(int(cell)) for cell in row])
        self.width = len(self.raw[0])
        self.height = len(self.raw)

    def write_to_file(self, file_path):
        """
        Writes the current lawn state to a CSV file.

        Each tile's state in the lawn is written as a separate entry in the CSV file. 
        The file is overwritten if it already exists.

        :param file_path: The path to the file where the lawn state should be saved.
        """
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            # convert from LawnsState to int
            outlist = []
            for row in self.raw:
                writer.writerow([str(cell.value) for cell in row])