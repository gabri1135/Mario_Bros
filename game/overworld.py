import pygame

from .levels_settings import levels
from .ui import OverWorldUI


class Node(pygame.sprite.Sprite):
    def __init__(self, id, pos) -> None:
        super().__init__()
        self.image = pygame.image.load(f'graphics/overworld/{id}.png')
        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(
            self.rect.centerx-4, self.rect.bottom-4, 8, 8)


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.pos = pos

        self.image = pygame.Surface((32, 32))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class OverWorld:
    def __init__(self, current_level, unlocked, ui, surface, create_level) -> None:
        # set values
        self.unlocked = unlocked
        self.create_level = create_level
        self.current_level = current_level
        self.ui: OverWorldUI = ui
        self.display_surface = surface

        self.setup_nodes()
        self.setup_icon()

        self.moving = False
        self.direction = pygame.math.Vector2()

        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, level in enumerate(levels):
            node = Node(index, level['node_pos'])
            self.nodes.add(node)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        self.icon.add(Icon(self.nodes.sprites()[
                      self.current_level].rect.midbottom))

    def draw_line(self):
        if self.unlocked > 0:
            points = [level['node_pos']
                      for index, level in enumerate(levels) if index <= self.unlocked]
            pygame.draw.lines(self.display_surface,
                              '#a04f45', False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_LEFT] and self.current_level > 0:
                self.direction = self.calculate_direction('prec')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_RIGHT] and self.current_level < self.unlocked:
                self.direction = self.calculate_direction('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_RETURN]:
                self.create_level(self.current_level)

    def calculate_direction(self, target):
        start = pygame.math.Vector2(
            self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.direction:
            self.icon.sprite.pos += self.direction*8
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)
                self.ui.level_id = self.current_level

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    def run(self):
        self.input_timer()
        self.input()

        self.update_icon_pos()
        self.icon.update()

        self.draw_line()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
