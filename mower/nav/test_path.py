from path import Path, Command
def test_path():
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