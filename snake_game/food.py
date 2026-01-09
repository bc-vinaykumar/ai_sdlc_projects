import pygame
import random

class Food:
    """
    Represents the food in the game.

    Attributes:
        position (tuple[int, int]): The (x, y) coordinates of the food.
        color (tuple[int, int, int]): The color of the food in RGB format.
        block_size (int): The size of the food in pixels.
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
    """

    def __init__(self, screen_width: int, screen_height: int, block_size: int):
        """
        Initializes the Food object.

        Args:
            screen_width (int): The width of the game screen.
            screen_height (int): The height of the game screen.
            block_size (int): The size of the food.
        """
        self.position: tuple[int, int] = (0, 0)
        self.color: tuple[int, int, int] = (255, 0, 0)  # Red
        self.block_size: int = block_size
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.generate_food()

    def generate_food(self) -> None:
        """
        Generates food at a random location on the screen, aligned to the grid.
        """
        self.position = (random.randrange(0, self.screen_width // self.block_size) * self.block_size,
                         random.randrange(0, self.screen_height // self.block_size) * self.block_size)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the food on the screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        pygame.draw.rect(screen, self.color,
                         (self.position[0], self.position[1], self.block_size, self.block_size))

    def get_position(self) -> tuple[int, int]:
        """
        Returns the position of the food.

        Returns:
            tuple[int, int]: The (x, y) coordinates of the food.
        """
        return self.position
