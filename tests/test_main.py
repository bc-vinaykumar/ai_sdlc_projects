"""
test_main.py: Contains the test cases for the main.py file.
"""
import unittest
import pygame
from unittest.mock import patch
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from snake_game.main import Main
from snake_game.game import Game  # Import Game class

## TestMainClass
class TestMainClass(unittest.TestCase):
    """
    Test cases for the Main class.
    """

    ## TestMainInitialization
    def test_main_initialization(self) -> None:
        """
        Test that the Main class can be instantiated.
        """
        main_instance: Main = Main()
        self.assertIsInstance(main_instance, Main)

    ## TestMainMethodInitialization
    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('game.Game.run')
    def test_main_method_initialization(self, mock_game_run, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that the main method initializes Pygame, creates a Game object, and quits Pygame.
        """
        Main.main()
        mock_pygame_init.assert_called_once()
        mock_game_run.assert_called_once()
        mock_pygame_quit.assert_called_once()

    ## TestMainMethodScreenSize
    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('game.Game.run')
    def test_main_method_screen_size(self, mock_game_run, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that the main method initializes the Game object with the correct screen size and block size.
        """
        with patch('game.Game') as MockGame:
            Main.main()
            MockGame.assert_called_once_with(600, 480, 20)

    ## TestGameRunCalled
    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('game.Game.run')
    def test_game_run_called(self, mock_game_run, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that the game.run() method is called within Main.main().
        """
        Main.main()
        mock_game_run.assert_called_once()

    ## TestPygameQuitCalled
    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('game.Game.run')
    def test_pygame_quit_called(self, mock_game_run, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that pygame.quit() is called within Main.main().
        """
        Main.main()
        mock_pygame_quit.assert_called_once()

    ## TestGameInstanceType
    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('game.Game.run')
    def test_game_instance_type(self, mock_game_run, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that a Game instance is created within Main.main().
        """
        with patch('game.Game') as MockGame:
            Main.main()
            MockGame.assert_called_once_with(600, 480, 20)
            game_instance = MockGame.return_value
            self.assertIsInstance(game_instance, MockGame)

if __name__ == '__main__':
    unittest.main()
