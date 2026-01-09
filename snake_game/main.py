"""
main.py: Contains the main function that initializes Pygame, creates a Game object,
and starts the game loop.
"""
import pygame
from game import Game

class Main:
    """
    Main class to run the Snake game.
    """
    @staticmethod
    def main() -> None:
        """
        Main function to initialize Pygame, create a Game object, and start the game loop.
        """
        pygame.init()
        screen_width: int = 600  # Default screen width
        screen_height: int = 480 # Default screen height
        block_size: int = 20      # Default block size

        game: Game = Game(screen_width, screen_height, block_size)
        game.run()
        pygame.quit()

if __name__ == "__main__":
    Main.main()
