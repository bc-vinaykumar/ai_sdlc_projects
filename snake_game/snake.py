import pygame

class Snake:
    """
    Represents the snake in the game.

    Attributes:
        body (list[(int, int)]): A list of (x, y) coordinates representing the snake's body.  The head is the first element.
        direction ((int, int)): A tuple representing the snake's movement direction (dx, dy).
        color (tuple[int, int, int]): The color of the snake in RGB format.
        block_size (int): The size of each snake block in pixels.
    """

    def __init__(self, start_position: tuple[int, int], block_size: int, color: tuple[int, int, int] = (0, 255, 0)):
        """
        Initializes the snake at the given starting position with a default length of 3.

        Args:
            start_position ((int, int)): The (x, y) coordinates of the snake's initial position.
            block_size (int): The size of each snake block.
            color (tuple[int, int, int]): The color of the snake. Defaults to green.
        """
        self.body: list[tuple[int, int]] = [start_position, (start_position[0] - block_size, start_position[1]), (start_position[0] - 2 * block_size, start_position[1])]
        self.direction: tuple[int, int] = (block_size, 0)  # Initial direction: right
        self.color: tuple[int, int, int] = color
        self.block_size: int = block_size

    def move(self) -> None:
        """
        Moves the snake one step in its current direction.
        """
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head: tuple[int, int] = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()  # Remove the last segment to maintain the same length

    def grow(self) -> None:
        """
        Grows the snake by one block.
        """
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head: tuple[int, int] = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

    def change_direction(self, direction: tuple[int, int]) -> None:
        """
        Changes the snake's direction.  The snake cannot reverse direction.

        Args:
            direction ((int, int)): The new direction (dx, dy).
        """
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return  # Prevent reversing
        self.direction = direction

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the snake on the screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        for x, y in self.body:
            pygame.draw.rect(screen, self.color, (x, y, self.block_size, self.block_size))

    def check_self_collision(self) -> bool:
        """
        Checks if the snake has collided with itself.

        Returns:
            bool: True if the snake has collided with itself, False otherwise.
        """
        head_x, head_y = self.get_head_position()
        for i in range(1, len(self.body)):
            if self.body[i] == (head_x, head_y):
                return True
        return False

    def get_head_position(self) -> tuple[int, int]:
        """
        Returns the position of the snake's head.

        Returns:
            (int, int): The (x, y) coordinates of the head.
        """
        return self.body[0]
