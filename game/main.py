import pygame
import sys

from .settings import screen_width, screen_height, screen_fps
from .game import Game


def main():
    pygame.init()
    pygame.display.set_caption('Super Mario')
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('grey')
        game.run()

        pygame.display.update()
        clock.tick(screen_fps)


if __name__ == '__main__':
    main()
