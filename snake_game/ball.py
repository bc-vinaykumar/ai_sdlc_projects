import pygame
import random

class Ball:
    """
    Represents the ball in the game.

    Attributes:
        position (tuple[int, int]): The (x, y) coordinates of the ball's position.
        color (tuple[int, int, int]): The color of the ball in RGB format.
        block_size (int): The size of the ball in pixels.
        width (int): The width of the game screen.
        height (int): The height of the game screen.
    """

    def __init__(self, width: int, height: int, block_size: int, color: tuple[int, int, int] = (255, 0, 0)):
        """
        Initializes the ball at a random position on the screen.

        Args:
            width (int): The width of the game screen.
            height (int): The height of the game screen.
            block_size (int): The size of the ball.
            color (tuple[int, int, int]): The color of the ball. Defaults to red.
        """
        self.width: int = width
        self.height: int = height
        self.block_size: int = block_size
        self.color: tuple[int, int, int] = color
        self.position: tuple[int, int] = self.generate_random_position()

    def generate_random_position(self) -> tuple[int, int]:
        """
        Generates a random position for the ball within the screen boundaries,
        aligned to the block size.

        Returns:
            (int, int): The (x, y) coordinates of the new position.
        """
        x: int = random.randrange(0, self.width // self.block_size) * self.block_size
        y: int = random.randrange(0, self.height // self.block_size) * self.block_size
        return (x, y)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the ball on the screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.block_size, self.block_size))

    def move(self) -> None:
        """
        Moves the ball to a new random position on the screen.
        """
        self.position: tuple[int, int] = self.generate_random_position()

    def get_position(self) -> tuple[int, int]:
        """
        Returns the current position of the ball.

        Returns:
            (int, int): The (x, y) coordinates of the ball.
        """
        return self.position
