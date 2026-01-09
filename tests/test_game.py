import unittest
import pygame
import sys
from unittest.mock import patch
from snake_game.game import Game
from snake_game.snake import Snake
from snake_game.ball import Ball

## TestGameInitialization
class TestGameInitialization(unittest.TestCase):
    """
    Test cases for the Game class initialization.
    """

    def test_game_initialization_default(self) -> None:
        """
        Test that the game initializes with default width and height.
        """
        game: Game = Game()
        self.assertEqual(game.width, 600)
        self.assertEqual(game.height, 480)
        self.assertEqual(game.score, 0)
        self.assertFalse(game.game_over)
        self.assertEqual(game.block_size, 20)
        self.assertIsInstance(game.snake, Snake)
        self.assertIsInstance(game.ball, Ball)
        pygame.quit()

    def test_game_initialization_custom(self) -> None:
        """
        Test that the game initializes with custom width and height.
        """
        width: int = 800
        height: int = 600
        game: Game = Game(width, height)
        self.assertEqual(game.width, width)
        self.assertEqual(game.height, height)
        self.assertEqual(game.score, 0)
        self.assertFalse(game.game_over)
        self.assertEqual(game.block_size, 20)
        self.assertIsInstance(game.snake, Snake)
        self.assertIsInstance(game.ball, Ball)
        pygame.quit()

## TestGameHandleInput
class TestGameHandleInput(unittest.TestCase):
    """
    Test cases for the Game class's handle_input method.
    """

    def setUp(self) -> None:
        """
        Set up the game instance for each test.
        """
        pygame.init()
        self.game: Game = Game()

    def tearDown(self) -> None:
        """
        Clean up after each test.
        """
        pygame.quit()

    def test_handle_input_up(self) -> None:
        """
        Test handling of the up arrow key.
        """
        initial_direction: tuple[int, int] = self.game.snake.direction
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        self.game.handle_input(event)
        if initial_direction != (0, self.game.block_size):
            self.assertEqual(self.game.snake.direction, (0, -self.game.block_size))
        else:
            self.assertEqual(self.game.snake.direction, initial_direction)

    def test_handle_input_down(self) -> None:
        """
        Test handling of the down arrow key.
        """
        initial_direction: tuple[int, int] = self.game.snake.direction
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
        self.game.handle_input(event)
        if initial_direction != (0, -self.game.block_size):
            self.assertEqual(self.game.snake.direction, (0, self.game.block_size))
        else:
            self.assertEqual(self.game.snake.direction, initial_direction)

    def test_handle_input_left(self) -> None:
        """
        Test handling of the left arrow key.
        """
        initial_direction: tuple[int, int] = self.game.snake.direction
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        self.game.handle_input(event)
        if initial_direction != (self.game.block_size, 0):
            self.assertEqual(self.game.snake.direction, (-self.game.block_size, 0))
        else:
            self.assertEqual(self.game.snake.direction, initial_direction)

    def test_handle_input_right(self) -> None:
        """
        Test handling of the right arrow key.
        """
        initial_direction: tuple[int, int] = self.game.snake.direction
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        self.game.handle_input(event)
        if initial_direction != (-self.game.block_size, 0):
            self.assertEqual(self.game.snake.direction, (self.game.block_size, 0))
        else:
            self.assertEqual(self.game.snake.direction, initial_direction)

    def test_handle_input_other_key(self) -> None:
        """
        Test handling of a key that is not an arrow key.
        """
        initial_direction: tuple[int, int] = self.game.snake.direction
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, initial_direction)

    def test_handle_input_quit(self) -> None:
        """
        Test handling of the quit event.
        """
        event: pygame.event.Event = pygame.event.Event(pygame.QUIT)
        with self.assertRaises(SystemExit):
            self.game.handle_input(event)

## TestGameUpdate
class TestGameUpdate(unittest.TestCase):
    """
    Test cases for the Game class's update method.
    """

    def setUp(self) -> None:
        """
        Set up the game instance for each test.
        """
        pygame.init()
        self.game: Game = Game()

    def tearDown(self) -> None:
        """
        Clean up after each test.
        """
        pygame.quit()

    def test_update_game_not_over(self) -> None:
        """
        Test that the update method moves the snake and checks for collisions when the game is not over.
        """
        initial_position: tuple[int, int] = self.game.snake.segments[0]
        self.game.update()
        current_position: tuple[int, int] = self.game.snake.segments[0]
        self.assertNotEqual(initial_position, current_position)
        self.assertFalse(self.game.game_over)

    def test_update_game_over(self) -> None:
        """
        Test that the update method does not move the snake when the game is over.
        """
        self.game.game_over = True
        initial_position: tuple[int, int] = self.game.snake.segments[0]
        self.game.update()
        current_position: tuple[int, int] = self.game.snake.segments[0]
        self.assertEqual(initial_position, current_position)

## TestGameCheckCollision
class TestGameCheckCollision(unittest.TestCase):
    """
    Test cases for the Game class's check_collision method.
    """

    def setUp(self) -> None:
        """
        Set up the game instance for each test.
        """
        pygame.init()
        self.game: Game = Game()

    def tearDown(self) -> None:
        """
        Clean up after each test.
        """
        pygame.quit()

    def test_check_collision_with_ball(self) -> None:
        """
        Test collision with the ball.
        """
        self.game.snake.segments[0] = (self.game.ball.x, self.game.ball.y)
        initial_score: int = self.game.score
        initial_snake_length: int = len(self.game.snake.segments)
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score + 1)
        self.assertEqual(len(self.game.snake.segments), initial_snake_length + 1)

    def test_check_collision_with_walls(self) -> None:
        """
        Test collision with the walls.
        """
        self.game.snake.segments[0] = (-1, -1)
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

        self.game.game_over = False
        self.game.snake.segments[0] = (self.game.width, self.game.height)
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

    def test_check_collision_with_self(self) -> None:
        """
        Test collision with itself.
        """
        self.game.snake.segments = [(100, 100), (100, 100)]
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

    def test_no_collision(self) -> None:
        """
        Test when there is no collision.
        """
        initial_score: int = self.game.score
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score)
        self.assertFalse(self.game.game_over)

## TestGameOverScreen
class TestGameOverScreen(unittest.TestCase):
    """
    Test cases for the Game class's game_over_screen method.
    """

    def setUp(self) -> None:
        """
        Set up the game instance for each test.
        """
        pygame.init()
        self.game: Game = Game()
        self.game.game_over = True

    def tearDown(self) -> None:
        """
        Clean up after each test.
        """
        pygame.quit()

    @patch('pygame.event.get')
    @patch('sys.exit')
    def test_game_over_screen_quit(self, mock_exit, mock_event_get) -> None:
        """
        Test that the game over screen handles the quit event.
        """
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        with self.assertRaises(SystemExit):
            self.game.game_over_screen()
        mock_exit.assert_called_once()

    @patch('pygame.event.get')
    @patch('sys.exit')
    def test_game_over_screen_restart(self, mock_exit, mock_event_get) -> None:
         """
         Test that the game over screen handles the restart event (SPACE key).
         This test is complex because it involves restarting the game,
         which would normally lead to an infinite loop. To prevent this,
         we mock the run() method to do nothing.
         """
         mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})]

         # Mock the run method to prevent infinite recursion
         with patch.object(Game, 'run') as mock_run:
             mock_run.return_value = None  # Make the mocked run method do nothing
             self.game.game_over_screen()
             # Assert that the run method was called, indicating a restart attempt
             mock_run.assert_called_once()

    @patch('pygame.event.get')
    @patch('sys.exit')
    def test_game_over_screen_escape(self, mock_exit, mock_event_get) -> None:
        """
        Test that the game over screen handles the escape event.
        """
        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})]
        with self.assertRaises(SystemExit):
            self.game.game_over_screen()
        mock_exit.assert_called_once()

    @patch('pygame.event.get')
    def test_game_over_screen_other_key(self, mock_event_get) -> None:
        """
        Test that the game over screen ignores other key events.
        """
        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})]
        # Check that the game doesn't exit or restart
        try:
            self.game.game_over_screen()
        except SystemExit:
            self.fail("SystemExit should not be raised")
        # Additional check to ensure the game_over_screen loop continues
        self.assertTrue(self.game.game_over)

if __name__ == '__main__':
    unittest.main()
