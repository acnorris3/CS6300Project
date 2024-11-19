class AbstractGameScreen:
    def __init__(self, width=800, height=800):
        """
        Initialize the game screen. This should handle game logic and drawing.

        :param width: The width of the game screen in pixels, defaults to 800.
        :param height: The height of the game screen in pixels, defaults to 800.
        """
        pass

    def update_lawn(self, new_position) -> None:
        """
        Update the lawn based on the current position of the mower.

        If the current position of the mower is on an unmowed lawn cell, 
        change the state of that cell to mowed.
        """
        pass

    def check_collision(self, new_position) -> bool:
        """
        Check if the mower has collided with an object on the lawn.

        :param new_position: The new position of the mower.
        :return: True if the mower has collided with an object, False otherwise.
        """
        pass
    
    def move_mower(self, direction) -> None:
        """
        Move the mower in the given direction, if a valid move.

        :param direction: The direction in which the mower should move."""
        pass

    # Draw the lawn
    def draw_lawn(self, screen):
        """
        Draw the lawn onto the given screen.

        This function goes through each cell in the grid, and based on the state of the cell,
        draws a rectangle of the appropriate color onto the screen. The mower's position is
        drawn as red, unmowed lawn is drawn as dark green, mowed lawn is light green, trees
        are yellow, rocks are brown, concrete is grey, and the base is blue.

        :param screen: The surface to draw the lawn onto. At time of writing, this should be defined in a UnifiedUI object.
        """
        pass

    # def handle_keypress(self, event):
    # NEED NOT BE IMPLEMENTED FOR SELF-DRIVING MOWERS
    #     """
    #     Handles keypress events.

    #     This function updates the position of the mower based on user input from the keyboard.
    #     The mower can move up, down, left, or right if the corresponding key is pressed.
    #     Checks for valid destination of the mower.

    #     If the mower has left the base, it keeps track of that fact.

    #     :param event: The event object passed in from the event loop.
    #     :return: None
    #     """

    def mower_has_returned_home(self) -> bool:
        """
        Returns True if the mower has previously left and is now back at the base, indicating the simulation should end;
        otherwise, it returns False.

        :return: A boolean indicating if the mower has returned to the base.
        """
        pass
