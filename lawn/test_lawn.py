import os
from lawn import Lawn
from lawn_states import LawnState

def test_lawn():
    csv_lawn = Lawn()
    literal_lawn = Lawn([[LawnState.BASE,LawnState.UNMOWED,LawnState.UNMOWED],
                         [LawnState.UNMOWED,LawnState.UNMOWED,LawnState.UNMOWED],
                         [LawnState.UNMOWED,LawnState.UNMOWED,LawnState.UNMOWED]])
    csv_lawn.load_from_file('./lawn/example_lawn_1.csv')

    # Check that the width and height are correct
    assert literal_lawn.width == 3
    assert literal_lawn.height == 3
    assert csv_lawn.width == 9
    assert csv_lawn.height == 6

    # Check that individual tiles can be accessed correctly
    assert csv_lawn.get_tile(0,0) == LawnState.BASE
    assert csv_lawn.get_tile(1,1) == LawnState.UNMOWED

    # Check that the lawn can be updated
    csv_lawn.update_tile(1,1, LawnState.MOWED)
    assert csv_lawn.get_tile(1,1) == LawnState.MOWED

    # Check that a filepath doesn't yet exist, write to it, and check that it exists
    assert not os.path.exists('./lawn/test_destination.csv')
    csv_lawn.write_to_file('./lawn/test_destination.csv')
    assert os.path.exists('./lawn/test_destination.csv')

    # cleanup
    os.remove('./lawn/test_destination.csv')