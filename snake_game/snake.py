import pygame

class Snake:
    """
    Represents the snake in the game.

    Attributes:
        body (list[(int, int)]): A list of (x, y) coordinates representing the snake's body segments.
        direction (tuple[int, int]): A tuple representing the snake's direction (dx, dy).
        color (tuple[int, int, int]): The color of the snake in RGB format.
        block_size (int): The size of each snake segment in pixels.
    """

    def __init__(self, x: int, y: int, block_size: int):
        """
        Initializes the Snake object.

        Args:
            x (int): The initial x-coordinate of the snake's head.
            y (int): The initial y-coordinate of the snake's head.
            block_size (int): The size of each snake segment.
        """
        self.body: list[tuple[int, int]] = [(x, y)]
        self.direction: tuple[int, int] = (1, 0)  # Initial direction: right
        self.color: tuple[int, int, int] = (0, 255, 0)  # Green
        self.block_size: int = block_size

    def move(self) -> None:
        """
        Moves the snake by adding a new head segment in the current direction
        and removing the tail segment.  If the snake grows, the tail is not removed.
        """
        head_x, head_y = self.get_head_position()
        new_head: tuple[int, int] = (head_x + self.direction[0] * self.block_size,
                               head_y + self.direction[1] * self.block_size)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self) -> None:
        """
        Grows the snake by adding a new segment to the head, without removing the tail.
        """
        head_x, head_y = self.get_head_position()
        new_head: tuple[int, int] = (head_x + self.direction[0] * self.block_size,
                               head_y + self.direction[1] * self.block_size)
        self.body.insert(0, new_head)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the snake on the screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        for segment in self.body:
            pygame.draw.rect(screen, self.color,
                             (segment[0], segment[1], self.block_size, self.block_size))

    def get_head_position(self) -> tuple[int, int]:
        """
        Returns the position of the snake's head.

        Returns:
            tuple[int, int]: The (x, y) coordinates of the head.
        """
        return self.body[0]

    def check_self_collision(self) -> bool:
        """
        Checks if the snake has collided with itself.

        Returns:
            bool: True if the snake has collided with itself, False otherwise.
        """
        head_x, head_y = self.get_head_position()
        for segment in self.body[1:]:  # Exclude the head
            if (head_x, head_y) == segment:
                return True
        return False

    def set_direction(self, direction: tuple[int, int]) -> None:
        """
        Sets the direction of the snake, preventing it from reversing directly.

        Args:
            direction (tuple[int, int]): The new direction (dx, dy).
        """
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
