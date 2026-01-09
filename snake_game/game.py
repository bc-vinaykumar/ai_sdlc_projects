"""
game.py: Contains the Game class, which manages the game loop, handles user input,
updates game state, draws game elements, checks for collisions, and displays the score.
"""
import pygame
import sys
from snake import Snake
from food import Food

class Game:
    """
    Manages the game loop, user input, game state, drawing, and collision detection.

    Attributes:
        snake (Snake): The Snake object.
        food (Food): The Food object.
        screen (pygame.Surface): The Pygame surface to draw on.
        score (int): The player's score.
        game_over (bool): A flag indicating whether the game is over.
        clock (pygame.time.Clock): The Pygame clock for controlling the frame rate.
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
        block_size (int): The size of each block in the game.
    """

    def __init__(self, screen_width: int = 600, screen_height: int = 480, block_size: int = 20):
        """
        Initializes the Game object.

        Args:
            screen_width (int): The width of the game screen. Defaults to 600.
            screen_height (int): The height of the game screen. Defaults to 480.
            block_size (int): The size of each block in the game. Defaults to 20.
        """
        pygame.init()
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.block_size: int = block_size
        self.screen: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.snake: Snake = Snake(screen_width // 2, screen_height // 2, self.block_size)
        self.food: Food = Food(self.screen_width, self.screen_height, self.block_size)
        self.score: int = 0
        self.game_over: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.font: pygame.font.Font = pygame.font.Font(None, 36)  # Default font

    def run(self) -> None:
        """
        Runs the main game loop.
        """
        while not self.game_over:
            for event in pygame.event.get():
                self.handle_input(event)
            self.update()
            self.draw()
            self.clock.tick(15)  # Adjust the frame rate to control game speed

        self.wait_for_restart()

    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Handles user input events.

        Args:
            event (pygame.event.Event): A Pygame event object.
        """
        if event.type == pygame.QUIT:
            self.game_over = True
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                self.snake.set_direction((0, -1))
            elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                self.snake.set_direction((0, 1))
            elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                self.snake.set_direction((-1, 0))
            elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                self.snake.set_direction((1, 0))

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
        self.food.draw(self.screen)
        self.display_score()
        pygame.display.flip()

    def check_collision(self) -> None:
        """
        Checks for collisions with the screen boundaries, the snake itself, and the food.
        """
        head_x, head_y = self.snake.get_head_position()

        # Collision with screen boundaries
        if (head_x < 0 or head_x >= self.screen_width or
            head_y < 0 or head_y >= self.screen_height or
            self.snake.check_self_collision()):
            self.game_over = True

        # Collision with food
        if (head_x, head_y) == self.food.get_position():
            self.snake.grow()
            self.food.generate_food()
            self.score += 1

    def reset(self) -> None:
        """
        Resets the game state.
        """
        self.snake = Snake(self.screen_width // 2, self.screen_height // 2, self.block_size)
        self.food = Food(self.screen_width, self.screen_height, self.block_size)
        self.score = 0
        self.game_over = False

    def display_score(self) -> None:
        """
        Displays the player's score on the screen.
        """
        score_text: str = f"Score: {self.score}"
        score_surface: pygame.Surface = self.font.render(score_text, True, (255, 255, 255))  # White color
        score_rect: pygame.Rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_surface, score_rect)

    def wait_for_restart(self) -> None:
        """
        Displays game over message and waits for user to press a key to restart.
        """
        game_over_text: str = "Game Over! Press any key to restart."
        game_over_surface: pygame.Surface = self.font.render(game_over_text, True, (255, 255, 255))
        game_over_rect: pygame.Rect = game_over_surface.get_rect()
        game_over_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(game_over_surface, game_over_rect)

        score_text: str = f"Final Score: {self.score}"
        score_surface: pygame.Surface = self.font.render(score_text, True, (255, 255, 255))
        score_rect: pygame.Rect = score_surface.get_rect()
        score_rect.center = (self.screen_width // 2, self.screen_height // 2 + 50)  # Position below game over text
        self.screen.blit(score_surface, score_rect)

        pygame.display.flip()

        waiting: bool = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    self.reset()
                    self.run()  # Restart the game
