import pygame
from time import time


class Goomba(pygame.sprite.Sprite):
    def __init__(self, pos, surfaces, dead_surface, to_left: bool) -> None:
        super().__init__()
        self.surfaces = surfaces
        self.dead_surface = dead_surface
        self.max = len(self.surfaces)
        self.surface_id = 0
        self.animation_speed = 0.3
        self.image = self.surfaces[self.surface_id]
        self.rect = self.image.get_rect(bottomleft=pos)
        self.real_x = self.rect.x
        self.x_direction = -1.5 if to_left else 1.5
        self.is_alive = True

    def reverse(self):
        self.x_direction = -self.x_direction
        self.real_x += self.x_direction*2

    def hit(self):
        self.x_direction = 0
        self.is_alive = False
        self.image = self.dead_surface
        self.rect = self.image.get_rect(bottom=self.rect.bottom)
        self.hitted_time = time()

    def animate(self):
        self.surface_id += self.animation_speed
        if self.surface_id >= self.max:
            self.surface_id -= self.max
        image = self.surfaces[int(self.surface_id)]
        if self.x_direction > 0:
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.rect = self.image.get_rect(bottom=self.rect.bottom)

    def update(self, velocity):
        if self.is_alive:
            self.real_x += self.x_direction
            self.animate()
        else:
            if time()-self.hitted_time >= 0.15:
                self.kill()
        self.real_x -= velocity
        self.rect.x = int(self.real_x)
