"""
Unit tests for the Game class, handling potential missing pygame dependency.
"""
import unittest
import sys
from unittest.mock import patch

# Try importing pygame, if it fails, set a flag to skip tests
try:
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False
    print("Pygame is not installed. Skipping tests that require pygame.")

# Import game modules only if pygame is available, otherwise define dummy classes
if pygame_available:
    from snake_game.game import Game
    from snake_game.snake import Snake
    from snake_game.food import Food
else:
    # Define dummy classes to avoid NameErrors when pygame is not available
    class Game:
        pass
    class Snake:
        pass
    class Food:
        pass


## TestGameInitialization
@unittest.skipUnless(pygame_available, "Pygame is not installed")
class TestGameInitialization(unittest.TestCase):
    """
    Test cases for the Game class initialization.
    """

    def test_game_initialization_default(self) -> None:
        """
        Test the default initialization of the Game class.
        """
        game: Game = Game()
        self.assertEqual(game.screen_width, 600)
        self.assertEqual(game.screen_height, 480)
        self.assertEqual(game.block_size, 20)
        self.assertIsInstance(game.screen, pygame.Surface)
        self.assertIsInstance(game.snake, Snake)
        self.assertIsInstance(game.food, Food)
        self.assertEqual(game.score, 0)
        self.assertFalse(game.game_over)
        self.assertIsInstance(game.clock, pygame.time.Clock)

    def test_game_initialization_custom(self) -> None:
        """
        Test the initialization of the Game class with custom parameters.
        """
        screen_width: int = 800
        screen_height: int = 600
        block_size: int = 30
        game: Game = Game(screen_width, screen_height, block_size)
        self.assertEqual(game.screen_width, screen_width)
        self.assertEqual(game.screen_height, screen_height)
        self.assertEqual(game.block_size, block_size)
        self.assertIsInstance(game.screen, pygame.Surface)
        self.assertIsInstance(game.snake, Snake)
        self.assertIsInstance(game.food, Food)
        self.assertEqual(game.score, 0)
        self.assertFalse(game.game_over)
        self.assertIsInstance(game.clock, pygame.time.Clock)

## TestGameHandleInput
@unittest.skipUnless(pygame_available, "Pygame is not installed")
class TestGameHandleInput(unittest.TestCase):
    """
    Test cases for the handle_input method of the Game class.
    """

    def setUp(self) -> None:
        """
        Set up a Game instance for testing.
        """
        self.game: Game = Game()

    @patch('pygame.quit')
    @patch('sys.exit')
    def test_handle_input_quit(self, mock_sys_exit, mock_pygame_quit) -> None:
        """
        Test handling of the QUIT event.
        """
        event: pygame.event.Event = pygame.event.Event(pygame.QUIT, {})
        self.game.handle_input(event)
        self.assertTrue(self.game.game_over)
        mock_pygame_quit.assert_called_once()
        mock_sys_exit.assert_called_once()

    def test_handle_input_key_up(self) -> None:
        """
        Test handling of the K_UP key event.
        """
        self.game.snake.direction = (0, 0)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (0, -1))

        self.game.snake.direction = (0, 1)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (0, 1))

    def test_handle_input_key_down(self) -> None:
        """
        Test handling of the K_DOWN key event.
        """
        self.game.snake.direction = (0, 0)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (0, 1))

        self.game.snake.direction = (0, -1)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (0, -1))

    def test_handle_input_key_left(self) -> None:
        """
        Test handling of the K_LEFT key event.
        """
        self.game.snake.direction = (0, 0)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (-1, 0))

        self.game.snake.direction = (1, 0)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (1, 0))

    def test_handle_input_key_right(self) -> None:
        """
        Test handling of the K_RIGHT key event.
        """
        self.game.snake.direction = (0, 0)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (1, 0))

        self.game.snake.direction = (-1, 0)
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        self.game.handle_input(event)
        self.assertEqual(self.game.snake.direction, (-1, 0))

## TestGameUpdate
@unittest.skipUnless(pygame_available, "Pygame is not installed")
class TestGameUpdate(unittest.TestCase):
    """
    Test cases for the update method of the Game class.
    """

    def setUp(self) -> None:
        """
        Set up a Game instance for testing.
        """
        self.game: Game = Game()

    @patch('snake_game.snake.Snake.move')
    @patch('snake_game.game.Game.check_collision')
    def test_update_not_game_over(self, mock_check_collision, mock_snake_move) -> None:
        """
        Test the update method when the game is not over.
        """
        self.game.game_over = False
        self.game.update()
        mock_snake_move.assert_called_once()
        mock_check_collision.assert_called_once()

    @patch('snake_game.snake.Snake.move')
    @patch('snake_game.game.Game.check_collision')
    def test_update_game_over(self, mock_check_collision, mock_snake_move) -> None:
        """
        Test the update method when the game is over.
        """
        self.game.game_over = True
        self.game.update()
        mock_snake_move.assert_not_called()
        mock_check_collision.assert_not_called()

## TestGameCheckCollision
@unittest.skipUnless(pygame_available, "Pygame is not installed")
class TestGameCheckCollision(unittest.TestCase):
    """
    Test cases for the check_collision method of the Game class.
    """

    def setUp(self) -> None:
        """
        Set up a Game instance for testing.
        """
        self.game: Game = Game()

    def test_check_collision_screen_boundaries(self) -> None:
        """
        Test collision with screen boundaries.
        """
        self.game.snake.get_head_position = lambda: (-1, 0)
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

        self.game.reset()
        self.game.snake.get_head_position = lambda: (self.game.screen_width, 0)
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

        self.game.reset()
        self.game.snake.get_head_position = lambda: (0, -1)
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

        self.game.reset()
        self.game.snake.get_head_position = lambda: (0, self.game.screen_height)
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

    def test_check_collision_self_collision(self) -> None:
        """
        Test collision with the snake itself.
        """
        self.game.snake.check_self_collision = lambda: True
        self.game.check_collision()
        self.assertTrue(self.game.game_over)

    def test_check_collision_food_collision(self) -> None:
        """
        Test collision with food.
        """
        self.game.snake.get_head_position = lambda: self.game.food.get_position()
        initial_score: int = self.game.score
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score + 1)

## TestGameReset
@unittest.skipUnless(pygame_available, "Pygame is not installed")
class TestGameReset(unittest.TestCase):
    """
    Test cases for the reset method of the Game class.
    """

    def setUp(self) -> None:
        """
        Set up a Game instance for testing.
        """
        self.game: Game = Game()
        self.game.score = 10
        self.game.game_over = True

    def test_reset(self) -> None:
        """
        Test the reset method.
        """
        self.game.reset()
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertIsInstance(self.game.snake, Snake)
        self.assertIsInstance(self.game.food, Food)

if __name__ == '__main__':
    unittest.main()
