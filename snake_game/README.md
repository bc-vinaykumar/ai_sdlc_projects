"""
README.md
"""
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


import sys

class Game:
    """
    Manages the snake game, handling game logic, user input, and drawing.

    Attributes:
        snake (Snake): The snake object.
        ball (Ball): The ball object.
        width (int): The width of the game screen.
        height (int): The height of the game screen.
        score (int): The player's score.
        screen (pygame.Surface): The Pygame surface to draw on.
        game_over (bool): A flag indicating whether the game is over.
        block_size (int): The size of each block in the game.
    """

    def __init__(self, width: int = 600, height: int = 480) -> None:
        """
        Initializes the game with the given width and height.

        Args:
            width (int): The width of the game screen. Defaults to 600.
            height (int): The height of the game screen. Defaults to 480.
        """
        pygame.init()
        self.width: int = width
        self.height: int = height
        self.block_size: int = 20
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.snake: Snake = Snake((width // 2, height // 2), self.block_size)
        self.ball: Ball = Ball(width, height, self.block_size)
        self.score: int = 0
        self.game_over: bool = False
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.frame_rate: int = 10  # Adjust for difficulty

    def run(self) -> None:
        """
        Runs the main game loop.
        """
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                    sys.exit()
                self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(self.frame_rate)

        self.game_over_screen()

    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Handles user input events.

        Args:
            event (pygame.event.Event): The Pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != (0, self.block_size):
                self.snake.change_direction((0, -self.block_size))
            elif event.key == pygame.K_DOWN and self.snake.direction != (0, -self.block_size):
                self.snake.change_direction((0, self.block_size))
            elif event.key == pygame.K_LEFT and self.snake.direction != (self.block_size, 0):
                self.snake.change_direction((-self.block_size, 0))
            elif event.key == pygame.K_RIGHT and self.snake.direction != (-self.block_size, 0):
                self.snake.change_direction((self.block_size, 0))

    def update(self) -> None:
        """
        Updates the game state.
        """
        if not self.game_over:
            self.snake.move()
            self.check_collision()

    def draw(self) -> None:
        """
        Draws the game elements on the screen.
        """
        self.screen.fill((0, 0, 0))  # Black background
        self.snake.draw(self.screen)
        self.ball.draw(self.screen)

        # Display score
        score_text: pygame.Surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))

        pygame.display.flip()

    def check_collision(self) -> None:
        """
        Checks for collisions between the snake, the ball, and the walls.
        """
        head_x, head_y = self.snake.get_head_position()
        ball_x, ball_y = self.ball.get_position()

        # Collision with ball
        if head_x == ball_x and head_y == ball_y:
            self.snake.grow()
            self.ball.move()
            self.score += 1

        # Collision with walls
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.game_over = True

        # Collision with self
        if self.snake.check_self_collision():
            self.game_over = True

    def game_over_screen(self) -> None:
        """
        Displays the game over screen.
        """
        self.screen.fill((0, 0, 0))  # Black background
        game_over_text: pygame.Surface = self.font.render("Game Over", True, (255, 255, 255))
        score_text: pygame.Surface = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text: pygame.Surface = self.font.render("Press SPACE to restart, ESC to quit", True, (255, 255, 255))

        game_over_rect: pygame.Rect = game_over_text.get_rect(center=(self.width // 2, self.height // 3))
        score_rect: pygame.Rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        restart_rect: pygame.Rect = restart_text.get_rect(center=(self.width // 2, self.height * 2 // 3))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

        waiting_for_input: bool = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_input = False
                        self.__init__(self.width, self.height)  # Restart the game
                        self.run()
                    elif event.key == pygame.K_ESCAPE:
                        waiting_for_input = False
                        pygame.quit()
                        sys.exit()


"""
Main entry point for the Snake game.
"""
import sys


def main() -> None:
    """
    Initializes Pygame and the Snake game, then runs the game loop.
    """
    pygame.init()
    width: int = 600  # Default width
    height: int = 480  # Default height

    game: Game = Game(width, height)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
