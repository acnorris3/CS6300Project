from enum import Enum

class Command(Enum):
    TURN = 0
    FORWARD = 1
    CUT = 2

class Path:
    def __init__(self):
        self.path = []

    def add(self, command: Command, value: int):
        """append a command/value pair to the path

        Args:
            command (Command): command
                if TURN: accepts postive or negative multiples of 90, in degrees
                if FORWARD: accepts positive integers representing forward steps
                if CUT: accepts 0 (stop cutting) or 1 (start cutting). Intentionally idempotent.
            value (int): value
        """
        if command == Command.TURN:
            if value % 90 != 0:
                raise ValueError("Only multiples of 90 degrees are supported")
        elif command == Command.FORWARD:
            if value < 0:
                raise ValueError("Only positive integers are supported")
        elif command == Command.CUT:
            if value not in [0, 1]:
                raise ValueError("Only 0 and 1 are supported")
        self.path.append((command, value))

    def execute_next_command(self) -> (Command, int):
        """ if possible, pop the first command from the path and return it
        returns: 
            command (Command): the next command in the list
            value (int): the amplitude of the command
        """
        if len(self.path) == 0:
            raise IndexError("path is empty")
        return self.path.pop(0)

    def get_path_length(self) -> int:
        """return the current length of the path as an integer"""
        return len(self.path)


if __name__ == "__main__":
    test_path = Path()
    test_path.add(Command.TURN, 90)
    test_path.add(Command.FORWARD, 10)
    test_path.add(Command.CUT, 0)
    test_path.add(Command.CUT, 1)
    assert test_path.get_path_length() == 4
    assert test_path.execute_next_command() == (Command.TURN, 90)
    assert test_path.execute_next_command() == (Command.FORWARD, 10)
    assert test_path.execute_next_command() == (Command.CUT, 0)
    assert test_path.execute_next_command() == (Command.CUT, 1)
    assert test_path.get_path_length() == 0
    print("all Path class tests passed")