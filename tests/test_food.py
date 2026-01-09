import unittest
import pygame
import random
from unittest.mock import patch
import sys
sys.path.append('/data/snake_game')
from food import Food

class TestFood(unittest.TestCase):
    """
    Test cases for the Food class.
    """

    def setUp(self):
        """
        Set up for the test cases.
        """
        self.screen_width: int = 600
        self.screen_height: int = 400
        self.block_size: int = 20
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.food: Food = Food(self.screen_width, self.screen_height, self.block_size)

    def tearDown(self):
        """
        Tear down for the test cases.
        """
        pygame.quit()

    ## Initialization Tests
    def test_food_initialization(self):
        """
        Test that the Food object is initialized correctly.
        """
        self.assertEqual(self.food.color, (255, 0, 0))
        self.assertEqual(self.food.block_size, self.block_size)
        self.assertEqual(self.food.screen_width, self.screen_width)
        self.assertEqual(self.food.screen_height, self.screen_height)

    ## generate_food Tests
    def test_generate_food_position_within_screen(self):
        """
        Test that the generated food position is within the screen boundaries.
        """
        for _ in range(100):  # Run multiple times to ensure randomness is covered
            self.food.generate_food()
            x: int = self.food.position[0]
            y: int = self.food.position[1]
            self.assertTrue(0 <= x < self.screen_width)
            self.assertTrue(0 <= y < self.screen_height)

    def test_generate_food_position_aligned_to_grid(self):
        """
        Test that the generated food position is aligned to the grid.
        """
        for _ in range(100):  # Run multiple times to ensure randomness is covered
            self.food.generate_food()
            x: int = self.food.position[0]
            y: int = self.food.position[1]
            self.assertEqual(x % self.block_size, 0)
            self.assertEqual(y % self.block_size, 0)

    @patch('random.randrange')
    def test_generate_food_randomness(self, mock_randrange):
        """
        Test that generate_food uses random.randrange.
        """
        mock_randrange.return_value = 5
        self.food.generate_food()
        expected_x: int = 5 * self.block_size
        expected_y: int = 5 * self.block_size
        self.assertEqual(self.food.position, (expected_x, expected_y))
        mock_randrange.assert_called()

    ## draw Tests
    def test_draw_food(self):
        """
        Test that the draw method draws the food on the screen.
        This test primarily checks that the draw method executes without errors,
        as directly verifying the pixel output of pygame is complex.
        """
        try:
            self.food.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() raised an exception: {e}")

    ## get_position Tests
    def test_get_position(self):
        """
        Test that the get_position method returns the correct position.
        """
        self.food.position: tuple[int, int] = (100, 50)
        self.assertEqual(self.food.get_position(), (100, 50))

    ## Edge Cases and Error Handling
    def test_zero_screen_dimensions(self):
        """
        Test that the Food object handles zero screen dimensions gracefully.
        """
        with self.assertRaises(ValueError):
            food: Food = Food(0, 0, self.block_size)

    def test_zero_block_size(self):
        """
        Test that the Food object handles zero block size gracefully.
        """
        with self.assertRaises(ZeroDivisionError):
            food: Food = Food(self.screen_width, self.screen_height, 0)

    def test_negative_screen_dimensions(self):
        """
        Test that the Food object handles negative screen dimensions gracefully.
        """
        with self.assertRaises(ValueError):
            food: Food = Food(-100, -50, self.block_size)

    def test_negative_block_size(self):
        """
        Test that the Food object handles negative block size gracefully.
        """
        with self.assertRaises(ValueError):
            food: Food = Food(self.screen_width, self.screen_height, -10)

    def test_large_screen_dimensions(self):
        """
        Test that the Food object handles large screen dimensions without errors.
        """
        large_screen_width: int = 2000
        large_screen_height: int = 1500
        try:
            food: Food = Food(large_screen_width, large_screen_height, self.block_size)
            self.assertTrue(0 <= food.position[0] < large_screen_width)
            self.assertTrue(0 <= food.position[1] < large_screen_height)
        except Exception as e:
            self.fail(f"Food initialization with large screen dimensions raised an exception: {e}")

    def test_large_block_size(self):
        """
        Test that the Food object handles large block size without errors.
        """
        large_block_size: int = 100
        try:
            food: Food = Food(self.screen_width, self.screen_height, large_block_size)
            self.assertTrue(0 <= food.position[0] < self.screen_width)
            self.assertTrue(0 <= food.position[1] < self.screen_height)
        except Exception as e:
            self.fail(f"Food initialization with large block size raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
