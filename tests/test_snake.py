import unittest
import pygame
from snake_game.snake import Snake

class TestSnake(unittest.TestCase):
    """
    Test suite for the Snake class.
    """

    def setUp(self) -> None:
        """
        Set up for the test cases.  Initializes a Snake object with default values.
        """
        pygame.init()
        self.block_size: int = 20
        self.start_position: tuple[int, int] = (100, 100)
        self.snake: Snake = Snake(self.start_position, self.block_size)
        self.screen_width: int = 600
        self.screen_height: int = 480
        self.screen: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))

    def tearDown(self) -> None:
        """
        Clean up after the test cases.
        """
        pygame.quit()

    ## Initialization Tests
    def test_snake_initialization(self) -> None:
        """
        Test that the snake is initialized correctly.
        """
        self.assertEqual(self.snake.body, [(100, 100), (80, 100), (60, 100)])
        self.assertEqual(self.snake.direction, (20, 0))
        self.assertEqual(self.snake.color, (0, 255, 0))
        self.assertEqual(self.snake.block_size, 20)

    def test_snake_initialization_custom_color(self) -> None:
        """
        Test that the snake is initialized correctly with a custom color.
        """
        custom_color: tuple[int, int, int] = (255, 0, 0)
        snake: Snake = Snake(self.start_position, self.block_size, custom_color)
        self.assertEqual(snake.color, custom_color)

    ## Move Tests
    def test_move(self) -> None:
        """
        Test that the snake moves correctly.
        """
        self.snake.move()
        self.assertEqual(self.snake.body, [(120, 100), (100, 100), (80, 100)])

    ## Grow Tests
    def test_grow(self) -> None:
        """
        Test that the snake grows correctly.
        """
        self.snake.grow()
        self.assertEqual(self.snake.body, [(120, 100), (100, 100), (80, 100), (60, 100)])

    ## Change Direction Tests
    def test_change_direction(self) -> None:
        """
        Test that the snake changes direction correctly.
        """
        new_direction: tuple[int, int] = (0, 20)
        self.snake.change_direction(new_direction)
        self.assertEqual(self.snake.direction, (0, 20))

    def test_change_direction_prevent_reverse(self) -> None:
        """
        Test that the snake cannot reverse direction.
        """
        initial_direction: tuple[int, int] = self.snake.direction
        self.snake.change_direction((-self.block_size, 0))  # Attempt to reverse
        self.assertEqual(self.snake.direction, initial_direction)

        self.snake.change_direction((0, self.block_size))
        self.snake.change_direction((0, -self.block_size))
        self.assertEqual(self.snake.direction, (0, -self.block_size))
        self.snake.change_direction((0, self.block_size))
        self.assertEqual(self.snake.direction, (0, -self.block_size))

    ## Draw Tests
    def test_draw(self) -> None:
        """
        Test that the snake is drawn correctly (basic test to see if it runs without errors).
        """
        try:
            self.snake.draw(self.screen)
            pygame.display.flip()
        except Exception as e:
            self.fail(f"Draw method raised an exception: {e}")

    ## Collision Tests
    def test_check_self_collision_no_collision(self) -> None:
        """
        Test that the snake does not collide with itself when it hasn't.
        """
        self.assertFalse(self.snake.check_self_collision())

    def test_check_self_collision_collision(self) -> None:
        """
        Test that the snake collides with itself when it has.
        """
        # Manually create a collision scenario
        self.snake.body = [(0, 0), (20, 0), (20, 20), (0, 20), (0, 0)]
        self.assertTrue(self.snake.check_self_collision())

    ## Get Head Position Tests
    def test_get_head_position(self) -> None:
        """
        Test that the snake's head position is returned correctly.
        """
        self.assertEqual(self.snake.get_head_position(), (100, 100))

    def test_move_negative_coordinates(self) -> None:
        """
        Test that the snake moves correctly with negative coordinates.
        """
        snake: Snake = Snake((-20, -20), self.block_size)
        snake.move()
        self.assertEqual(snake.body[0], (0, -20))

    def test_change_direction_zero_block_size(self) -> None:
        """
        Test that the snake handles zero block size correctly.
        """
        snake: Snake = Snake((0, 0), 0)
        snake.change_direction((0, 0))
        self.assertEqual(snake.direction, (0, 0))

    def test_grow_multiple_times(self) -> None:
        """
        Test that the snake grows correctly multiple times.
        """
        self.snake.grow()
        self.snake.grow()
        self.assertEqual(len(self.snake.body), 5)

    def test_move_after_grow(self) -> None:
        """
        Test that the snake moves correctly after growing.
        """
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.body), 4)

if __name__ == '__main__':
    unittest.main()
