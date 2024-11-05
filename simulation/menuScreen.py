# menu_screen.py

import pygame
import pygame_gui

class menuScreen:
    def __init__(self, screen_width=800, screen_height=600):
        """Sets up the Pygame GUI elements but does not start the main loop."""

        # Declare GUI elements - can be called by downstream consumers
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.ui_manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.buttons_bottom = []
        self.buttons_right = []

        # Define GUI layout
        main_screen_width = int(self.screen_width * 0.75)
        main_screen_height = int(self.screen_height * 0.8)
        main_screen_rect = pygame.Rect(0, 0, main_screen_width, main_screen_height)

        # Bottom button area
        button_width = 80
        button_height = 40
        button_spacing = 20

        button_y = self.screen_height - button_height - 10
        button_labels = ["Start", "Pause", "Stop", "Quit"]
        for i, label in enumerate(button_labels):
            button_x = 10 + i * (button_width + button_spacing)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(button_x, button_y, button_width, button_height),
                text=label,
                manager=self.ui_manager
            )
            self.buttons_bottom.append(button)

        # Right buttons
        right_button_width = 150
        right_button_height = 40
        right_button_x = self.screen_width - right_button_width - 10
        right_button_labels = ["Create Lawn", "Load Lawn 1", "Load Lawn 2", "Load Lawn 3"]
        self.buttons_right = [
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(right_button_x, 10 + i * (right_button_height + 20), 
                                        right_button_width, right_button_height),
                text=label,
                manager=self.ui_manager
            )
            for i, label in enumerate(right_button_labels)
        ]


    def run_menu_screen_loop(self):
        """Runs the main event loop for the menu self.screen."""
        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check if a button is pressed
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.buttons_bottom[3]:  # Quit button was pressed
                        running = False  # Close the program

                # Pass events to Pygame GUI manager
                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.screen.fill((100, 100, 100))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(0, 0, int(self.screen.get_width() * 0.75), int(self.screen.get_height() * 0.8)))
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()
