import pygame

from settings import tile_size, screen_width, player_speed
from tiles import Tile, StaticTile, AnimatedTile, CoinTile, BlockTile, SurpriseBlockTile
from player import Player
from levels_data import levels
from utils import import_csv_layout, import_cut_graphics, import_folder


class Level:
    def __init__(self, level_id, surface, increment_coin) -> None:
        self.display_surface = surface
        self.screen_speed = 0
        level_data = levels[level_id]

        # map position
        pos_tile = Tile((0, 0))
        # todo: to set
        self.map_width = 6000
        self.position_surface = pygame.sprite.GroupSingle()
        self.position_surface.add(pos_tile)

        # player setup
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player((50, 50))
        self.player.add(player_sprite)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(
            'terrain', terrain_layout)

        # block setup
        block_layout = import_csv_layout(level_data['block'])
        self.block_sprites = self.create_tile_group('block', block_layout)

        # q_block setup
        q_block_layout = import_csv_layout(level_data['q_block'])
        self.q_block_sprites = self.create_tile_group(
            'q_block', q_block_layout)

        # q_block setup
        q_block_layout = import_csv_layout(level_data['q_block'])
        self.q_block_sprites = self.create_tile_group(
            'q_block', q_block_layout)

        # coin setup
        self.increment_coin = increment_coin
        coin_layout = import_csv_layout(level_data['coin'])
        self.coin_sprites = self.create_tile_group('coin', coin_layout)

        # if not self.map_width:
        #    self.map_width = len(layout_data[0])*tile_size-screen_width
    def create_tile_group(self, type: str, layout: list[list[str]]):
        tile_group = pygame.sprite.Group()
        for y, row in enumerate(layout):
            for x, val in enumerate(row):
                if val != '-1':
                    if type == 'terrain':
                        surface = import_cut_graphics(
                            int(val), 'graphics/terrain/terrain_tiles.png')
                        tile = StaticTile((x*tile_size, y*tile_size), surface)
                        tile_group.add(tile)
                    elif type == 'block':
                        surfaces = import_folder('graphics/block/animation')
                        if val == '0':
                            tile = BlockTile(
                                (x*tile_size, y*tile_size), surfaces)
                        else:
                            tile = SurpriseBlockTile(
                                (x*tile_size, y*tile_size), surfaces, 1 if val == '1' else 10)
                        tile_group.add(tile)
                    elif type == 'q_block':
                        surfaces = import_folder('graphics/q_block/animation')
                        tile = SurpriseBlockTile(
                            (x*tile_size, y*tile_size), surfaces, 1)
                        tile_group.add(tile)
                    elif type == 'coin':
                        if val == '0':
                            surfaces = import_folder('graphics/coin/animation')
                            tile = CoinTile(
                                (x*tile_size, y*tile_size), surfaces)
                        else:
                            surfaces = import_folder(
                                'graphics/starcoin/animation')
                            tile = CoinTile(
                                (x*tile_size, y*tile_size), surfaces, star=True)
                        tile_group.add(tile)
        return tile_group

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x*player.speed

        for sprite in self.terrain_sprites.sprites()+self.block_sprites.sprites()+self.q_block_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 0.8:
	        player.on_ground = False

    def x_scrool(self):
        player = self.player.sprite
        x_player = player.rect.centerx
        position = self.position_surface.sprite.rect.x

        if x_player < screen_width/4 and player.direction.x < 0:
            if position >= 0:
                player.speed = 0 if player.rect.x <= 50 else player_speed
                self.screen_speed = 0
            else:
                self.screen_speed = -player_speed
                player.speed = 0
        elif x_player > 5*screen_width/8 and player.direction.x > 0:
            if position <= -self.map_width:
                player.speed = 0 if player.rect.x >= screen_width-100 else player_speed
                self.screen_speed = 0
            else:
                self.screen_speed = player_speed
                player.speed = 0
        else:
            self.screen_speed = 0
            player.speed = player_speed

    def check_coin_collision(self):
        collided_coin = pygame.sprite.spritecollide(
            self.player.sprite, self.coin_sprites, True, collided=pygame.sprite.collide_mask)
        for coin in collided_coin:
            if not coin.star:
                self.increment_coin(5)
            else:
                print('starcoin')

    def vertical_block_collision(self):
        player = self.player.sprite

        for sprite in self.block_sprites.sprites()+self.q_block_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:  # jump
                    sprite.collide()
                    #todo: max(-6, player.direction.y)
                    player.direction.y =1
                elif player.direction.y > 0:  # fall
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0

    def run(self):
        self.terrain_sprites.update(self.screen_speed)
        self.terrain_sprites.draw(self.display_surface)

        self.block_sprites.update(self.screen_speed)
        self.block_sprites.draw(self.display_surface)

        self.q_block_sprites.update(self.screen_speed)
        self.q_block_sprites.draw(self.display_surface)

        self.coin_sprites.update(self.screen_speed)
        self.coin_sprites.draw(self.display_surface)

        self.player.update()
        self.position_surface.update(self.screen_speed)
        self.x_scrool()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.vertical_block_collision()
        self.player.draw(self.display_surface)

        self.check_coin_collision()
