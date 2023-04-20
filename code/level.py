import pygame
from enemies import *
from flagpole import Flag, FlagBase, FlagPole
from game_data import LevelData
from levels_data import levels
from player import Player
from settings import player_speed, screen_width, tile_size
from tiles import *
from utils import import_csv_layout, import_cut_graphics, import_folder


class Level:
    def __init__(self, level_id, surface, levelData: LevelData) -> None:
        self.level_id = level_id
        self.display_surface = surface
        self.screen_speed = 0
        level_data = levels[level_id]
        self.levelData = levelData
        self.win = False

        # map position
        self.pos_x = 0

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
        coin_layout = import_csv_layout(level_data['coin'])
        self.coin_sprites = self.create_tile_group('coin', coin_layout)

        goomba_layout = import_csv_layout(level_data['goomba'])
        self.goomba_sprites = self.create_tile_group('goomba', goomba_layout)

        goomba_constraints_layout = import_csv_layout(
            level_data['goomba_constraints'])
        self.goomba_constraints_sprites = self.create_tile_group(
            'goomba_constraints', goomba_constraints_layout)

        # block hit animations
        self.spawned_coins = pygame.sprite.Group()
        self.spawned_mushrooms = pygame.sprite.Group()
        self.broken_blocks = pygame.sprite.Group()

        # player setup
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player((50, 50))
        self.player.add(player_sprite)

        # flag setup
        self.flagbase = pygame.sprite.GroupSingle()
        self.flagpole = pygame.sprite.GroupSingle()
        self.flag = pygame.sprite.GroupSingle()

        player_data_layout = import_csv_layout(level_data['player_data'])
        self.create_tile_group('player_data', player_data_layout)

        self.flagpole.add(FlagPole(self.flagbase.sprite.rect))
        self.flag.add(Flag(self.flagpole.sprite.rect))

        # if not self.map_width:
        #    self.map_width = len(layout_data[0])*tile_size-screen_width

    def create_tile_group(self, type: str, layout: list[list[str]]):
        tile_group = pygame.sprite.Group()
        self.map_width = tile_size*200-1200
        for y, row in enumerate(layout):
            y+=1
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
                    elif type == 'goomba':
                        surfaces = import_folder('graphics/goomba/animation')
                        dead_surface = pygame.image.load(
                            'graphics/goomba/dead_goomba.png').convert_alpha()
                        tile = Goomba((x*tile_size, (y+1)*tile_size),
                                      surfaces, dead_surface, val == '0')
                        tile_group.add(tile)
                    elif type == 'goomba_constraints':
                        tile = Tile((x*tile_size, y*tile_size))
                        tile_group.add(tile)
                    elif type == 'player_data':
                        self.map_width = len(layout[0])*tile_size-screen_width
                        tile = FlagBase((x*tile_size, (y+1)*tile_size))
                        self.flagbase.add(tile)
        return tile_group

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x*player.speed

        player.on_left = False
        player.on_right = False

        for sprite in self.terrain_sprites.sprites()+self.block_sprites.sprites()+self.q_block_sprites.sprites()+[self.flagbase.sprite]:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    if isinstance(sprite, StaticTile):
                        player.on_left = True
                        player.x_accell = 0
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    if isinstance(sprite, StaticTile):
                        player.on_right = True
                        player.x_accell = 0

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites()+[self.flagbase.sprite]:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y < 0:  # jump
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > 0:  # fall
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player_on_ground = True
                    player.on_left = False
                    player.on_right = False

    def vertical_block_collision(self):
        player = self.player.sprite

        for sprite in self.block_sprites.sprites()+self.q_block_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y <= 0:  # jump
                    sprite.collide()
                    player.direction.y = 0
                    player.collision_rect.top = sprite.rect.bottom+4
                    if isinstance(sprite, BlockTile):
                        block_parts = import_folder('graphics/block/broken')
                        broken_tiles = [BrokenBlockTile(sprite.rect.center, block_parts[0], -0.75, -18),
                                        BrokenBlockTile(
                                            sprite.rect.center, block_parts[0], 0.8, -17),
                                        BrokenBlockTile(
                                            sprite.rect.center, block_parts[1], -0.65, -19),
                                        BrokenBlockTile(sprite.rect.center, block_parts[2], 0.75, -20)]
                        self.broken_blocks.add(broken_tiles)
                elif player.direction.y > 0:  # fall
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player_on_ground = True
                    player.on_left = False
                    player.on_right = False

    def x_scrool(self):
        player = self.player.sprite
        x_player = player.rect.centerx

        if x_player < screen_width/4 and player.direction.x < 0:
            if self.pos_x <= 0:
                player.speed = player.rect.left if player.rect.left <= player_speed else player_speed
                self.screen_speed = 0
            else:
                self.screen_speed = -player_speed
                player.speed = 0
        elif x_player > 3*screen_width/4 and player.direction.x > 0:
            if self.pos_x >= self.map_width:
                player.speed = (
                    screen_width-player.rect.right) if player.rect.right >= screen_width-player_speed else player_speed
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
            surprise = SpawnCoinTile(surfaces, block, self.levelData.increment_coin)
            self.spawned_coins.add(surprise)
        else:
            surface = pygame.image.load(
                'graphics/q_block/mushroom.png').convert_alpha()
            surprise = SpawnMushroomTile(block.rect.topleft, surface)
            self.spawned_mushrooms.add(surprise)

    def mushroom_movement(self):
        for mushroom in self.spawned_mushrooms.sprites():
            for sprite in self.terrain_sprites.sprites()+self.block_sprites.sprites()+self.q_block_sprites.sprites():
                if mushroom.rect.colliderect(sprite.rect):
                    if mushroom.direction.x < 0:
                        mushroom.rect.left = sprite.rect.right
                    elif mushroom.direction.x > 0:
                        mushroom.rect.right = sprite.rect.left
                    mushroom.reverse()

        for mushroom in self.spawned_mushrooms.sprites():
            mushroom.apply_gravity()
            for sprite in self.terrain_sprites.sprites()+self.block_sprites.sprites()+self.q_block_sprites.sprites():
                if mushroom.rect.colliderect(sprite.rect):
                    mushroom.rect.bottom = sprite.rect.top
                    mushroom.direction.y = 0

    def check_mushroom_collision(self):
        for _ in pygame.sprite.spritecollide(self.player.sprite, self.spawned_mushrooms, True):
            self.levelData.increment_health()

    def check_coin_collision(self):
        collided_coin = pygame.sprite.spritecollide(
            self.player.sprite, self.coin_sprites, True, collided=pygame.sprite.collide_mask)
        for coin in collided_coin:
            if coin.star == None:
                self.levelData.increment_coin(5)
            else:
                self.levelData.get_star(coin.star)

    def horizontal_goomba_movement(self):
        for goomba in self.goomba_sprites.sprites():
            for sprite in self.terrain_sprites.sprites()+self.goomba_constraints_sprites.sprites():
                if sprite.rect.colliderect(goomba.rect):
                    goomba.reverse()

    def check_goomba_collision(self):
        player = self.player.sprite

        for goomba in self.goomba_sprites.sprites():
            if not player.collision_rect.colliderect(goomba):continue

            if (collided_pos:=pygame.sprite.collide_mask(player,goomba)):
                if (collided_pos[1]>=47 and player.direction.y>=0) or player.invincible:
                    if goomba.is_alive:
                        goomba.hit()
                    else:
                        player.direction.y = -7
                elif goomba.is_alive:
                    self.levelData.get_damage()
                    player.get_damage()

    def check_dead(self):
        if self.player.sprite.collision_rect.top > screen_height+64:
            self.levelData.game_over()

    def check_win(self):
        player = self.player.sprite
        flagpole = self.flagpole.sprite
        if r := pygame.sprite.collide_mask(flagpole, player):
            if r[1] < 326:
                self.win = True
                self.screen_speed = 0
                player.speed = player_speed

                self.descent_frame = (
                    flagpole.rect.bottom-34-player.collision_rect.bottom)//4
                y_speed = player.initialize_win(
                    flagpole.rect, self.descent_frame)
                self.flag.sprite.initialize_win(flagpole.rect, y_speed)

    def run(self):
        if not self.win:
            self.check_win()
            self.check_dead()

        self.pos_x += self.screen_speed

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

        self.mushroom_movement()
        self.spawned_mushrooms.update(self.screen_speed)
        self.spawned_mushrooms.draw(self.display_surface)

        self.horizontal_goomba_movement()
        self.goomba_constraints_sprites.update(self.screen_speed)
        #self.goomba_constraints_sprites.draw(self.display_surface)
        self.goomba_sprites.update(self.screen_speed)
        self.goomba_sprites.draw(self.display_surface)

        if not self.win:
            self.player.update()
            self.x_scrool()

            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.vertical_block_collision()
            self.player.sprite.on_ground = self.player_on_ground

            self.check_goomba_collision()

            self.check_coin_collision()
            self.check_mushroom_collision()

            #pygame.draw.rect(self.display_surface,(255,0,0),self.player.sprite.collision_rect)

        self.flag.update(self.screen_speed)
        self.flag.draw(self.display_surface)

        self.flagpole.update(self.screen_speed)
        self.flagpole.draw(self.display_surface)

        self.player.draw(self.display_surface)

        self.flagbase.update(self.screen_speed)
        self.flagbase.draw(self.display_surface)

        if self.win and self.descent_frame > 0:
            self.player.sprite.down_flag()
            self.flag.sprite.up_flag()
            self.descent_frame -= 1
