import pygame

from .level import Level
from .overworld import OverWorld
from .pop_up import buildPopUp
from .ui import LevelUI, OverWorldUI
from .user_data import UserData


class Game:
    def __init__(self, surface) -> None:
        self.display_surface = surface

        # import userData
        self.userData: UserData = UserData.read()

        self.create_overworld(0, 0)

    def create_level(self, level_id):
        self.currentLevelData = self.userData.start_level(level_id)
        self.level = Level(level_id, self.display_surface,
                           self.currentLevelData, self.create_overworld)
        self.levelUI = LevelUI(self.display_surface, self.currentLevelData)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level, save: bool = False):
        if new_max_level > self.userData.max_level:
            self.userData.new_max_level(new_max_level)

        if save:
            self.userData.save_progress(self.currentLevelData)
            if self.userData.health == 0:
                self.userData = UserData.reset()
                self.userData.save()
                current_level = 0

        self.overworldUI = OverWorldUI(
            self.display_surface, self.userData, current_level)
        self.overworld = OverWorld(
            current_level, self.userData.max_level, self.overworldUI, self.display_surface, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
            self.overworldUI.run()
        else:
            self.level.run()
            self.levelUI.run()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                if buildPopUp(self.display_surface) == 1:
                    self.create_overworld(self.level.level_id, 0)
