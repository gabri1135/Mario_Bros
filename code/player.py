import pygame
from math import sin

from settings import player_speed
from utils import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        # player animation
        self.import_character_assets()
        self.frame_index = 4
        self.animation_speed = 0.28
        self.image = self.animations['jump'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = player_speed
        self.gravity = 0.8
        self.jump_speed = -17.5
        self.x_accell = 0

        self.collision_rect = pygame.Rect(
            self.rect.topleft, (10, self.rect.height))

        # player status
        self.status = 'jump'
        self.facing_left = False
        self.on_ground = False
        self.on_left = False
        self.on_right = False

        # player collision
        self.invincible = False
        self.collision_time = None
        self.invincible_duration = 1500

    def import_character_assets(self):
        self.animations = {
            'idle': [pygame.image.load('graphics/lapo/idle.png').convert_alpha()],
            'run': import_folder('graphics/lapo/run/'),
            'jump': import_folder('graphics/lapo/jump/'),
            'climb': [pygame.image.load('graphics/lapo/climb.png').convert_alpha()]
        }

    def animate(self):
        animation = self.animations[self.status]

        if self.status != 'jump':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
        else:
            self.frame_index += 0.3
            if self.direction.y < 10:
                if self.frame_index >= 5 or (self.direction.y > 0 and self.frame_index != 4):
                    self.frame_index = 4
            else:
                if self.frame_index >= 9:
                    self.frame_index = 8
                elif self.frame_index <= 4:
                    self.frame_index = 5

        image = animation[int(self.frame_index)]

        if self.facing_left:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomleft = [
                self.collision_rect.bottomleft[0]-5, self.collision_rect.bottomleft[1]]
        else:
            self.image = image
            self.rect.bottomright = [
                self.collision_rect.bottomright[0]+5, self.collision_rect.bottomright[1]]

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not (self.on_left or self.on_right):
            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.direction.x = -1
            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.direction.x = 1
            else:
                self.direction.x = 0
        elif self.on_left:
            self.direction.x = -1
        else:
            self.direction.x = 1

        if keys[pygame.K_SPACE] and (self.on_ground or self.on_left or self. on_right):
            self.jump()

    def get_status(self):
        if self.on_left or self. on_right:
            self.status = 'climb'
        elif not 0 <= self.direction.y <= 1:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'

            else:
                self.status = 'idle'
        if self.direction.x > 0:
            self.facing_left = False
        elif self.direction.x < 0:
            self.facing_left = True

    def apply_gravity(self):
        if not (self.on_left or self.on_right):
            self.direction.y += self.gravity
        else:
            self.direction.y = 4
        self.collision_rect.y += self.direction.y

    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_speed
            self.frame_index = 0
        else:
            self.direction.y = self.jump_speed+5
            if self.on_left:
                self.direction.x = 1
                self.x_accell = -0.03
            else:
                self.direction.x = -1
                self.x_accell = 0.03
            self.on_left, self.on_right = False, False
            self.frame_index = 4

    # win setup
    def initialize_win(self, flagRect, frames):
        self.rect.right = flagRect.left+33
        self.real_y = self.collision_rect.y
        self.direction.y = (flagRect.bottom+10 -
                            self.collision_rect.bottom)/frames
        self.image = pygame.image.load(
            'graphics/lapo/flagpole.png').convert_alpha()
        self.rect = self.image.get_rect(
            center=(self.rect.midright[0]-23, self.rect.midright[1]))
        return self.direction.y

    def down_flag(self):
        self.real_y += self.direction.y
        self.rect.y = int(self.real_y)

    # mushroom collision
    def get_damage(self):
        self.invincible = True
        self.collision_time = pygame.time.get_ticks()

    def invincible_animation(self):
        if self.invincible:
            delay_time = pygame.time.get_ticks()-self.collision_time
            if delay_time > self.invincible_duration:
                self.invincible = False

    def wave_value(self):
        delay_time = (pygame.time.get_ticks()-self.collision_time)/30
        if sin(delay_time) > 0:
            return 255
        return 0

    def update(self):
        if self.x_accell == 0:
            self.get_input()
        else:
            self.direction.x += self.x_accell
            if -0.1 < self.direction.x < 0.1:
                self.x_accell = 0

        self.get_status()
        self.animate()
        self.invincible_animation()
