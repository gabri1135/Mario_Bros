import pygame


class FlagPole(pygame.sprite.Sprite):
    def __init__(self, baseRect) -> None:
        super().__init__()
        self.image = pygame.image.load(
            'graphics/flagpole/flagpole.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=baseRect.midtop)
        self.base = pygame.Rect(self.rect.left, self.rect.top+326, 75, 43)

    def update(self, velocity):
        self.rect.x -= velocity


class FlagBase(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.image.load(
            'graphics/flagpole/flagbase.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft=pos)


    def update(self, velocity):
        self.rect.x -= velocity


class Flag(pygame.sprite.Sprite):
    def __init__(self, flagRect) -> None:
        super().__init__()
        self.image = pygame.image.load(
            'graphics/flagpole/black_flag.png').convert_alpha()
        self.rect = self.image.get_rect(
            topleft=(flagRect[0]+20, flagRect[1]+25))

    def initialize_win(self, flagRect, y_speed):
        self.image = pygame.image.load(
            'graphics/flagpole/red_flag.png').convert_alpha()
        self.rect.top = flagRect.top+26+247
        self.max_heigth=flagRect.top+26
        self.real_y = self.rect.y
        self.y_direction = y_speed

    def up_flag(self):
        if self.rect.top>=self.max_heigth:
            self.real_y -= self.y_direction
            self.rect.y = int(self.real_y)

    def update(self, velocity):
        self.rect.x -= velocity
