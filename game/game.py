import pygame

from .game_data import LevelData
from .level import Level
from .overworld import OverWorld
from .pop_up import buildPopUp
from .ui import LevelUI


class Game:
    def __init__(self, surface) -> None:
        self.display_surface = surface

        self.max_level = 0
        self.create_overworld(0, 0)

    def create_level(self, level_id):
        self.currentGameData = LevelData()
        self.level = Level(level_id, self.display_surface,
                           self.currentGameData, self.create_overworld)
        self.levelUI = LevelUI(self.display_surface, self.currentGameData)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = OverWorld(
            current_level, self.max_level, self.display_surface, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.levelUI.run()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                if buildPopUp(self.display_surface) == 1:
                    self.create_overworld()
