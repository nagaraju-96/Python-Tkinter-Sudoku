import unittest
import pygame
from sudoko_game import main
class TestSudokuGame(unittest.TestCase):

    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def simulate_difficulty_selection(self, difficulty_button_pos):
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': difficulty_button_pos}))
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': difficulty_button_pos}))

    def simulate_key_press(self, key):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': key}))

    def simulate_mouse_click(self, cell_pos):
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': cell_pos}))
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': cell_pos}))

    def simulate_space_key_press(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))

    def simulate_delete_key_press(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DELETE}))

    def test_easy_difficulty(self):
        self.simulate_difficulty_selection((300, 300))

        # Simulate user playing the game (filling in numbers)
        self.simulate_mouse_click((320, 320))  # Click on a cell
        self.simulate_key_press(pygame.K_1)     # Enter the number 1

        # Add assertions based on expected behavior
        # For example, check if the number 1 is displayed in the selected cell

        # Simulate user closing the window
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Call the main function
        main()

    def test_medium_difficulty(self):
        self.simulate_difficulty_selection((600 // 2, 650 // 2))

        # Simulate user playing the game (filling in numbers)
        # ...

        # Simulate user closing the window
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        main()

    def test_hard_difficulty(self):
        self.simulate_difficulty_selection((3 * 600 // 4, 650 // 2))

        # Simulate user playing the game (filling in numbers)
        # ...

        # Simulate user closing the window
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        main()

    def test_reset_puzzle(self):
        self.simulate_difficulty_selection((600 // 2, 650 // 2))
        self.simulate_space_key_press()

        # Add assertions to check if the puzzle has reset
        # For example, check if the displayed numbers are back to the original puzzle

        pygame.event.post(pygame.event.Event(pygame.QUIT))
        main()

    def test_remove_number(self):
        self.simulate_difficulty_selection((600 // 2, 650 // 2))
        self.simulate_mouse_click((320, 320))  # Click on a cell
        self.simulate_key_press(pygame.K_1)     # Enter the number 1

        self.simulate_mouse_click((320, 320))  # Click on the same cell
        self.simulate_delete_key_press()       # Delete the number

        # Add assertions to check if the number has been removed
        # For example, check if the selected cell is now empty

        pygame.event.post(pygame.event.Event(pygame.QUIT))
        main()

    def test_invalid_move(self):
        self.simulate_difficulty_selection((600 // 2, 650 // 2))
        self.simulate_mouse_click((320, 320))  # Click on a cell
        self.simulate_key_press(pygame.K_1)     # Enter the number 1

        # Try to enter the same number in the same cell, which is an invalid move
        self.simulate_key_press(pygame.K_1)

        # Add assertions to check if an error message is displayed
        # For example, check if the error message is not None

        pygame.event.post(pygame.event.Event(pygame.QUIT))
        main()

if __name__ == '__main__':
    unittest.main()