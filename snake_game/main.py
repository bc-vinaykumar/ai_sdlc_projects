"""
Main entry point for the Snake game.
"""
import pygame
import sys
from game import Game


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
