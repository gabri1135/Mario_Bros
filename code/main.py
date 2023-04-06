import pygame,sys

from settings import screen_width,screen_height,screen_fps
from game import Game

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock=pygame.time.Clock()

game=Game(screen)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(screen_fps)