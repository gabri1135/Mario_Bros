import pygame

from settings import tile_size, screen_width, player_speed
from tiles import Tile
from player import Player


class Level:
    def __init__(self, level_data, surface) -> None:
        self.display_surface = surface
        self.setup_level(level_data)
        self.screen_speed = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size

                if cell == 'X':
                    tile = Tile((x, y))
                    self.tiles.add(tile)
                elif cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x*player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0

    def x_scrool(self):
        player = self.player.sprite
        x_player = player.rect.centerx

        if x_player < screen_width/4 and player.direction.x<0:
            self.screen_speed = -8
            player.speed = 0
        elif x_player > 3*screen_width/4  and player.direction.x>0:
            self.screen_speed = 8
            player.speed = 0
        else:
            self.screen_speed = 0
            player.speed = player_speed

    def run(self):
        self.x_scrool()
        self.tiles.update(self.screen_speed)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
