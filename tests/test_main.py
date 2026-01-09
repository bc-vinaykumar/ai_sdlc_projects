"""
Test suite for the main entry point of the Snake game.
"""
import unittest
from unittest.mock import patch
import pygame
import sys
import os

# Dynamically adjust sys.path to include the snake_game directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'snake_game')))
from main import main  # Import the main function
from game import Game  # Import the Game class

## TestMain
class TestMain(unittest.TestCase):
    """
    Test suite for the main function of the Snake game.
    """

    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('sys.exit')
    @patch('game.Game.run')
    def test_main_execution(self, mock_game_run, mock_sys_exit, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that main initializes Pygame, creates a Game instance, runs the game, and quits Pygame.
        """
        main()

        mock_pygame_init.assert_called_once()
        mock_game_run.assert_called_once()
        mock_pygame_quit.assert_called_once()
        mock_sys_exit.assert_called_once()

    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('sys.exit')
    @patch('game.Game.run')
    def test_main_game_instance_creation(self, mock_game_run, mock_sys_exit, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that the Game instance is created with the correct width and height.
        This test uses a side effect to capture the Game instance.
        """
        created_game_instance = None

        def side_effect(width: int, height: int):
            nonlocal created_game_instance
            created_game_instance = Game(width, height)
            return created_game_instance

        with patch('game.Game', side_effect=side_effect) as MockGame:
            main()

            MockGame.assert_called_once_with(600, 480)
            self.assertIsInstance(created_game_instance, Game) # Assert that an instance was created.

    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('sys.exit')
    @patch('game.Game.run')
    def test_main_pygame_initialization(self, mock_game_run, mock_sys_exit, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that pygame.init() is called.
        """
        main()
        mock_pygame_init.assert_called_once()

    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('sys.exit')
    @patch('game.Game.run')
    def test_main_pygame_quitting(self, mock_game_run, mock_sys_exit, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that pygame.quit() is called.
        """
        main()
        mock_pygame_quit.assert_called_once()

    @patch('pygame.init')
    @patch('pygame.quit')
    @patch('sys.exit')
    @patch('game.Game.run')
    def test_main_sys_exit(self, mock_game_run, mock_sys_exit, mock_pygame_quit, mock_pygame_init) -> None:
        """
        Test that sys.exit() is called.
        """
        main()
        mock_sys_exit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
