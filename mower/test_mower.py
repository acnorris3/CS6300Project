from mower import Mower
def test_mower():
    test_mower = Mower(y=3, direction=180)
    assert test_mower.x == 0
    assert test_mower.y == 3
    assert test_mower.direction == 180
    assert test_mower.path.get_path_length() == 0