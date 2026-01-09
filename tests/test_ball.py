import unittest
import pygame
import random
from unittest.mock import patch
import sys
sys.path.append('/data/snake_game')
from ball import Ball

## TestBallClass
class TestBallClass(unittest.TestCase):
    """
    Test cases for the Ball class.
    """

    def setUp(self):
        """
        Set up for the test cases. Initializes Pygame and creates a Ball instance.
        """
        pygame.init()
        self.width: int = 600
        self.height: int = 400
        self.block_size: int = 20
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.ball: Ball = Ball(self.width, self.height, self.block_size)

    def tearDown(self):
        """
        Tear down for the test cases. Quits Pygame.
        """
        pygame.quit()

    ## TestBallInitialization
    def test_ball_initialization(self):
        """
        Test that the Ball object is initialized correctly.
        """
        self.assertEqual(self.ball.width, self.width)
        self.assertEqual(self.ball.height, self.height)
        self.assertEqual(self.ball.block_size, self.block_size)
        self.assertEqual(self.ball.color, (255, 0, 0))
        self.assertIsInstance(self.ball.position, tuple)
        self.assertEqual(len(self.ball.position), 2)
        self.assertIsInstance(self.ball.position[0], int)
        self.assertIsInstance(self.ball.position[1], int)

    ## TestBallInitializationWithCustomColor
    def test_ball_initialization_with_custom_color(self):
        """
        Test that the Ball object is initialized correctly with a custom color.
        """
        color: tuple[int, int, int] = (0, 255, 0)
        ball: Ball = Ball(self.width, self.height, self.block_size, color)
        self.assertEqual(ball.color, color)

    ## TestGenerateRandomPosition
    def test_generate_random_position(self):
        """
        Test that the generate_random_position method returns a valid position.
        """
        position: tuple[int, int] = self.ball.generate_random_position()
        self.assertIsInstance(position, tuple)
        self.assertEqual(len(position), 2)
        self.assertIsInstance(position[0], int)
        self.assertIsInstance(position[1], int)
        self.assertLessEqual(position[0], self.width - self.block_size)
        self.assertLessEqual(position[1], self.height - self.block_size)
        self.assertEqual(position[0] % self.block_size, 0)
        self.assertEqual(position[1] % self.block_size, 0)

    ## TestDrawMethod
    def test_draw_method(self):
        """
        Test that the draw method does not raise an error.  We can't directly test the drawing,
        but we can check that it executes without exceptions.
        """
        try:
            self.ball.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() raised an exception: {e}")

    ## TestMoveMethod
    def test_move_method(self):
        """
        Test that the move method changes the ball's position.
        """
        initial_position: tuple[int, int] = self.ball.get_position()
        self.ball.move()
        new_position: tuple[int, int] = self.ball.get_position()
        self.assertNotEqual(initial_position, new_position)

    ## TestGetPositionMethod
    def test_get_position_method(self):
        """
        Test that the get_position method returns the correct position.
        """
        position: tuple[int, int] = self.ball.position
        retrieved_position: tuple[int, int] = self.ball.get_position()
        self.assertEqual(position, retrieved_position)

    ## TestPositionWithinBounds
    def test_position_within_bounds(self):
        """
        Test that the ball's position is always within the screen bounds.
        """
        for _ in range(100):  # Test multiple times to increase confidence
            self.ball.move()
            position: tuple[int, int] = self.ball.get_position()
            self.assertGreaterEqual(position[0], 0)
            self.assertGreaterEqual(position[1], 0)
            self.assertLessEqual(position[0], self.width - self.block_size)
            self.assertLessEqual(position[1], self.height - self.block_size)

    ## TestBlockSizeIsPositive
    def test_block_size_is_positive(self):
        """
        Test that the block size is a positive integer.
        """
        with self.assertRaises(ValueError):
            Ball(self.width, self.height, -self.block_size)

    ## TestWidthAndHeightArePositive
    def test_width_and_height_are_positive(self):
        """
        Test that the width and height are positive integers.
        """
        with self.assertRaises(ValueError):
            Ball(-self.width, self.height, self.block_size)
        with self.assertRaises(ValueError):
            Ball(self.width, -self.height, self.block_size)

    ## TestColorType
    def test_color_type(self):
        """
        Test that the color is a tuple of three integers.
        """
        with self.assertRaises(TypeError):
            Ball(self.width, self.height, self.block_size, "red")
        with self.assertRaises(ValueError):
            Ball(self.width, self.height, self.block_size, (255, 0))
        with self.assertRaises(ValueError):
            Ball(self.width, self.height, self.block_size, (255, 0, 0, 0))
        with self.assertRaises(ValueError):
            Ball(self.width, self.height, self.block_size, (255.0, 0, 0))
        with self.assertRaises(ValueError):
            Ball(self.width, self.height, self.block_size, (255, 0, -1))
        with self.assertRaises(ValueError):
            Ball(self.width, self.height, self.block_size, (255, 0, 256))

    ## TestRandomnessOfPosition
    @patch('random.randrange')
    def test_randomness_of_position(self, mock_randrange):
        """
        Test that the ball's position is randomly generated.
        """
        mock_randrange.return_value = 5
        ball: Ball = Ball(self.width, self.height, self.block_size)
        self.assertEqual(ball.position, (self.block_size * 5, self.block_size * 5))
        mock_randrange.assert_called()

    ## TestZeroWidthHeight
    def test_zero_width_height(self):
        """
        Test that the ball can be initialized with zero width or height.
        """
        ball_zero_width: Ball = Ball(0, self.height, self.block_size)
        ball_zero_height: Ball = Ball(self.width, 0, self.block_size)
        self.assertEqual(ball_zero_width.width, 0)
        self.assertEqual(ball_zero_height.height, 0)

    ## TestLargeWidthHeight
    def test_large_width_height(self):
        """
        Test that the ball can be initialized with large width and height.
        """
        large_width: int = 10000
        large_height: int = 8000
        ball_large_width_height: Ball = Ball(large_width, large_height, self.block_size)
        self.assertEqual(ball_large_width_height.width, large_width)
        self.assertEqual(ball_large_width_height.height, large_height)

if __name__ == '__main__':
    unittest.main()
