import pygame

from settings import tile_size, screen_width, player_speed
from tiles import *
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
        self.map_width = 100000
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

        # block hit animations
        self.spawned_coins = pygame.sprite.Group()
        self.spawned_mushrooms = pygame.sprite.Group()
        self.broken_blocks = pygame.sprite.Group()

        # if not self.map_width:
        #    self.map_width = len(layout_data[0])*tile_size-screen_width

    def create_tile_group(self, type: str, layout: list[list[str]]):
        tile_group = pygame.sprite.Group()
        self.map_width=tile_size*200-1200
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
                                (x*tile_size, y*tile_size), surfaces, 1 if val == '1' else 10, 'coin', self.spawn_surprise)
                        tile_group.add(tile)
                    elif type == 'q_block':
                        surfaces = import_folder('graphics/q_block/animation')
                        if val == '0':
                            tile = SurpriseBlockTile(
                                (x*tile_size, y*tile_size), surfaces, 1, 'mushroom', self.spawn_surprise)
                        else:
                            tile = SurpriseBlockTile(
                                (x*tile_size, y*tile_size), surfaces, 1, 'coin', self.spawn_surprise)
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
                                (x*tile_size, y*tile_size), surfaces, star=int(val)-1)
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
                if player.direction.y > 0:
                    self.player_on_ground = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:  # jump
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > 0:  # fall
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player_on_ground = True

    def vertical_block_collision(self):
        player = self.player.sprite

        for sprite in self.block_sprites.sprites()+self.q_block_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:  # jump
                    sprite.collide()
                    if isinstance(sprite, BlockTile):
                        player.direction.y = max(-6, player.direction.y)
                        block_parts = import_folder('graphics/block/broken')
                        broken_tiles = [BrokenBlockTile(sprite.rect.center, block_parts[0], -0.75, -18), 
                                        BrokenBlockTile(sprite.rect.center, block_parts[0], 0.8, -17), 
                                        BrokenBlockTile(sprite.rect.center, block_parts[1], -0.65, -19), 
                                        BrokenBlockTile(sprite.rect.center, block_parts[2], 0.75, -20)]
                        self.broken_blocks.add(broken_tiles)
                    else:
                        player.direction.y = 0
                        player.rect.top = sprite.rect.bottom
                elif player.direction.y > 0:  # fall
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player_on_ground = True

    def x_scrool(self):
        player = self.player.sprite
        x_player = player.rect.centerx
        position = self.position_surface.sprite.rect.x

        if x_player < screen_width/4 and player.direction.x < 0:
            if position >= 0:
                player.speed = 0 if player.rect.left <= 0 else player_speed
                self.screen_speed = 0
            else:
                self.screen_speed = -player_speed
                player.speed = 0
        elif x_player > 3*screen_width/4 and player.direction.x > 0:
            if position <= -self.map_width:
                player.speed = 0 if player.rect.right >= screen_width else player_speed
                self.screen_speed = 0
            else:
                self.screen_speed = player_speed
                player.speed = 0
        else:
            self.screen_speed = 0
            player.speed = player_speed

    def spawn_surprise(self, block):
        if block.type == 'coin':
            surfaces = import_folder('graphics/coin/animation')
            surprise = SpawnCoinTile(surfaces, block, self.increment_coin)
            self.spawned_coins.add(surprise)
        else:
            surface = pygame.image.load(
                'graphics/q_block/mushroom.png').convert_alpha()
            surprise = SpawnMushroomTile(block.rect.topleft, surface)
            self.spawned_mushrooms.add(surprise)

    def vertical_mushroom_collision(self):
        for mushroom in self.spawned_mushrooms.sprites():
            mushroom.apply_gravity()
            for sprite in self.terrain_sprites.sprites()+self.block_sprites.sprites()+self.q_block_sprites.sprites():

                if mushroom.rect.colliderect(sprite.rect):
                    mushroom.rect.bottom = sprite.rect.top
                    mushroom.y_direction = 0

    def check_mushroom_collision(self):
        for m in pygame.sprite.spritecollide(self.player.sprite, self.spawned_mushrooms, True):
            print('mushroom')

    def check_coin_collision(self):
        collided_coin = pygame.sprite.spritecollide(
            self.player.sprite, self.coin_sprites, True, collided=pygame.sprite.collide_mask)
        for coin in collided_coin:
            if coin.star == None:
                self.increment_coin(5)
            else:
                print('starcoin', coin.star)

    def run(self):
        self.player_on_ground = False
        self.terrain_sprites.update(self.screen_speed)
        self.terrain_sprites.draw(self.display_surface)

        self.block_sprites.update(self.screen_speed)
        self.block_sprites.draw(self.display_surface)

        self.q_block_sprites.update(self.screen_speed)
        self.q_block_sprites.draw(self.display_surface)

        self.broken_blocks.update(self.screen_speed)
        self.broken_blocks.draw(self.display_surface)

        self.spawned_coins.update(self.screen_speed)
        self.spawned_coins.draw(self.display_surface)

        self.coin_sprites.update(self.screen_speed)
        self.coin_sprites.draw(self.display_surface)

        self.vertical_mushroom_collision()
        self.spawned_mushrooms.update(self.screen_speed)
        self.spawned_mushrooms.draw(self.display_surface)

        self.player.update()
        self.position_surface.update(self.screen_speed)
        self.x_scrool()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.vertical_block_collision()
        self.player.sprite.on_ground = self.player_on_ground
        self.player.draw(self.display_surface)

        self.check_coin_collision()
        self.check_mushroom_collision()
