
import pygame

from settings import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, velocity):
        self.rect.x -= velocity


class StaticTile(Tile):
    def __init__(self, pos, surface) -> None:
        super().__init__(pos)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)


class AnimatedTile(Tile):
    def __init__(self, pos, surfaces) -> None:
        super().__init__(pos)
        self.surfaces = surfaces
        self.max = len(self.surfaces)
        self.surface_id = 0
        self.image = self.surfaces[self.surface_id]
        self.rect = self.image.get_rect(topleft=pos)

    def animate(self, speed=0.2):
        self.surface_id += speed
        if self.surface_id >= self.max:
            self.surface_id -= self.max
        self.image = self.surfaces[int(self.surface_id)]

    def update(self, velocity):
        self.animate()
        super().update(velocity)


class BlockTile(AnimatedTile):
    def __init__(self, pos, surfaces) -> None:
        super().__init__(pos, surfaces)

    def collide(self):
        self.kill()


class SurpriseBlockTile(AnimatedTile):
    def __init__(self, pos, surfaces, times) -> None:
        super().__init__(pos, surfaces)
        self.times = times
        self.collided = 0

    def collide(self):
        if self.times > 0 and self.collided == 0:
            self.times -= 1
            self.collided = -2

    def collide_animation(self):
        self.rect.y += self.collided
        if self.rect.y % tile_size == 34:
            self.collided = -self.collided
        elif self.rect.y % tile_size == 0:
            self.collided = 0
            if self.times == 0:
                self.image = pygame.image.load('graphics/q_block/used.png')

    def update(self, velocity):
        if self.times > 0:
            self.animate()

        if self.collided != 0:
            self.collide_animation()

        self.rect.x -= velocity


class CoinTile(AnimatedTile):
    def __init__(self, pos, surfaces, star=False) -> None:
        self.star = star
        super().__init__(pos, surfaces)
        self.rect.bottomleft = (pos[0], pos[1]+tile_size)
