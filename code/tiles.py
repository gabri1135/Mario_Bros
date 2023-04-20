
from typing import Optional
import pygame

from settings import tile_size, screen_height


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill('red')
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
        self.animation_speed = 0.2
        self.image = self.surfaces[self.surface_id]
        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):
        self.surface_id += self.animation_speed
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


class BrokenBlockTile(StaticTile):
    def __init__(self, pos, surface, acc_x, vel_y) -> None:
        self.real_image = surface
        self.angle = 0
        super().__init__(pos, surface)
        self.rect.center = pos
        self.direction = pygame.math.Vector2(0, vel_y)
        self.acceleration = pygame.math.Vector2(acc_x, 1.5)
        self.minmax = abs(acc_x)*8

    def animate(self):
        self.image = pygame.transform.rotate(self.real_image, self.angle)
        self.angle += 4
        self.rect = self.image.get_rect(center=self.rect.center)
        self.direction += self.acceleration
        self.direction.x = max(
            min(self.direction.x, self.minmax), -self.minmax)
        self.rect.center += self.direction

    def update(self, velocity):
        if self.rect.y > screen_height:
            self.kill()
        self.animate()
        super().update(velocity)


class SurpriseBlockTile(AnimatedTile):
    def __init__(self, pos, surfaces, times: int, type: str, spawn_surprise) -> None:
        super().__init__(pos, surfaces)
        self.times = times
        self.collided = 0
        self.type = type
        self.spawn_surprise = spawn_surprise

    def collide(self):
        if self.times > 0:
            self.times -= 1
            if self.collided >= 0:
                self.collided = -2
            self.spawn_surprise(self)

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
    def __init__(self, pos, surfaces, star: Optional[int] = None) -> None:
        self.star = star
        super().__init__(pos, surfaces)
        self.rect.bottomleft = (pos[0], pos[1]+tile_size)


class SpawnCoinTile(AnimatedTile):
    def __init__(self, surfaces, block, increment_coin) -> None:
        pos = block.rect.topleft
        super().__init__(pos, surfaces)
        self.rect.bottomleft = (pos[0], pos[1])
        self.animation_speed = 0.45
        self.y_direction = -8
        self.block = block
        self.increment_coin = increment_coin

    def update(self, velocity):
        if self.y_direction > 0 and self.rect.colliderect(self.block):
            self.increment_coin(5)
            self.kill()
        self.rect.y += self.y_direction
        self.y_direction = min(self.y_direction + 0.5, 4)
        super().update(velocity)


class SpawnMushroomTile(StaticTile):
    def __init__(self, pos, surface) -> None:
        super().__init__(pos, surface)
        self.rect.bottomleft = (pos[0], pos[1]-3)
        self.direction = pygame.math.Vector2(3, -6)

    def apply_gravity(self):
        self.direction.y = self.direction.y + 0.6
        self.rect.y += self.direction.y

    def reverse(self):
        self.direction.x = -self.direction.x

    def update(self, velocity):
        if self.rect.top > screen_height:
            self.kill()

        if -3 < self.direction.y < 2:
            self.rect.x += self.direction.x

        super().update(velocity)
