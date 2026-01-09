import unittest
import pygame
from snake_game.snake import Snake

class TestSnake(unittest.TestCase):
    """
    Test suite for the Snake class.
    """

    def setUp(self) -> None:
        """
        Set up for the test methods.
        """
        pygame.init()
        self.block_size: int = 20
        self.snake: Snake = Snake(100, 100, self.block_size)
        self.screen_width: int = 640
        self.screen_height: int = 480
        self.screen: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))

    def tearDown(self) -> None:
        """
        Clean up after the test methods.
        """
        pygame.quit()

    ## Test Snake Initialization
    def test_snake_initialization(self) -> None:
        """
        Test that the snake is initialized correctly.
        """
        self.assertEqual(self.snake.body, [(100, 100)])
        self.assertEqual(self.snake.direction, (1, 0))
        self.assertEqual(self.snake.color, (0, 255, 0))
        self.assertEqual(self.snake.block_size, self.block_size)

    ## Test Snake Move
    def test_snake_move(self) -> None:
        """
        Test that the snake moves correctly.
        """
        initial_head: tuple[int, int] = self.snake.get_head_position()
        self.snake.move()
        new_head: tuple[int, int] = self.snake.get_head_position()
        self.assertEqual(new_head, (initial_head[0] + self.block_size, initial_head[1]))
        self.assertEqual(len(self.snake.body), 1)

        self.snake.direction = (0, 1)
        self.snake.move()
        new_head = self.snake.get_head_position()
        self.assertEqual(new_head, (initial_head[0] + self.block_size, initial_head[1] + self.block_size))
        self.assertEqual(len(self.snake.body), 1)

    ## Test Snake Grow
    def test_snake_grow(self) -> None:
        """
        Test that the snake grows correctly.
        """
        initial_length: int = len(self.snake.body)
        self.snake.grow()
        self.assertEqual(len(self.snake.body), initial_length + 1)
        head_x, head_y = self.snake.get_head_position()
        self.assertEqual((head_x, head_y), (100 + self.block_size, 100))

    ## Test Snake Draw
    def test_snake_draw(self) -> None:
        """
        Test that the snake draws without errors.  This mainly checks that the draw method executes without raising exceptions.
        Visual inspection would be needed for complete validation.
        """
        try:
            self.snake.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() raised an exception: {e}")

    ## Test Get Head Position
    def test_get_head_position(self) -> None:
        """
        Test that the get_head_position method returns the correct position.
        """
        self.assertEqual(self.snake.get_head_position(), (100, 100))

    ## Test Check Self Collision - No Collision
    def test_check_self_collision_no_collision(self) -> None:
        """
        Test that the check_self_collision method returns False when there is no collision.
        """
        self.assertFalse(self.snake.check_self_collision())

    ## Test Check Self Collision - Collision
    def test_check_self_collision_collision(self) -> None:
        """
        Test that the check_self_collision method returns True when there is a collision.
        """
        self.snake.grow()
        self.snake.direction = (-1, 0)
        self.snake.move()
        self.snake.move()
        self.assertTrue(self.snake.check_self_collision())

    ## Test Set Direction - Valid Direction Change
    def test_set_direction_valid_direction_change(self) -> None:
        """
        Test that the set_direction method correctly changes the direction.
        """
        self.snake.set_direction((0, 1))
        self.assertEqual(self.snake.direction, (0, 1))

    ## Test Set Direction - Invalid Direction Change (Reversal)
    def test_set_direction_invalid_direction_change(self) -> None:
        """
        Test that the set_direction method prevents the snake from reversing directly.
        """
        initial_direction: tuple[int, int] = self.snake.direction
        self.snake.set_direction((-1, 0))  # Attempt to reverse
        self.assertEqual(self.snake.direction, initial_direction)

    ## Test Move Multiple Times
    def test_move_multiple_times(self) -> None:
        """
        Test moving the snake multiple times and check the head position.
        """
        initial_x: int = self.snake.body[0][0]
        initial_y: int = self.snake.body[0][1]
        for _ in range(3):
            self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_x + 3 * self.block_size, initial_y))

    ## Test Grow and Move
    def test_grow_and_move(self) -> None:
        """
        Test growing the snake and then moving it.
        """
        initial_length: int = len(self.snake.body)
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.body), initial_length + 1)

    ## Test Snake Initialization with Zero Block Size
    def test_snake_initialization_zero_block_size(self) -> None:
        """
        Test that the snake is initialized correctly with zero block size.
        """
        zero_block_size: int = 0
        snake: Snake = Snake(100, 100, zero_block_size)
        self.assertEqual(snake.block_size, zero_block_size)
        self.assertEqual(snake.body, [(100, 100)])

    ## Test Snake Move with Zero Block Size
    def test_snake_move_with_zero_block_size(self) -> None:
        """
        Test that the snake moves correctly with zero block size.
        """
        zero_block_size: int = 0
        snake: Snake = Snake(100, 100, zero_block_size)
        initial_head: tuple[int, int] = snake.get_head_position()
        snake.move()
        new_head: tuple[int, int] = snake.get_head_position()
        self.assertEqual(new_head, (initial_head[0], initial_head[1]))
        self.assertEqual(len(snake.body), 1)

    ## Test Snake Grow with Zero Block Size
    def test_snake_grow_with_zero_block_size(self) -> None:
        """
        Test that the snake grows correctly with zero block size.
        """
        zero_block_size: int = 0
        snake: Snake = Snake(100, 100, zero_block_size)
        initial_length: int = len(snake.body)
        snake.grow()
        self.assertEqual(len(snake.body), initial_length + 1)
        head_x, head_y = snake.get_head_position()
        self.assertEqual((head_x, head_y), (100, 100))

    ## Test Set Direction with Zero Direction
    def test_set_direction_zero_direction(self) -> None:
        """
        Test setting direction to (0, 0). It should not change the direction.
        """
        initial_direction: tuple[int, int] = self.snake.direction
        self.snake.set_direction((0, 0))
        self.assertEqual(self.snake.direction, initial_direction)

if __name__ == '__main__':
    unittest.main()
