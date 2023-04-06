import pygame

from settings import player_speed


class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 30))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = player_speed
        self.gravity = 0.8
        self.jump_speed = -16

        self.on_ground=False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]and not keys[pygame.K_LEFT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y=self.jump_speed

    def update(self):
        self.input()
