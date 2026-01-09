import pygame
import sys
from snake import Snake
from ball import Ball

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
