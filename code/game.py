from game_data import LevelData
from level import Level
from ui import LevelUI


class Game:
    def __init__(self, surface) -> None:
        self.display_surface = surface
        #self.gameData = GameData()
        self.start_level(2)

    def start_level(self, level_id):
        self.currentGameData = LevelData()
        self.level = Level(level_id, self.display_surface,
                           self.currentGameData)
        self.levelUI = LevelUI(self.display_surface, self.currentGameData)

    def game_over(self):
        print('gameover')
        quit()
        #self.level = Level(level_id, self.display_surface, self.gameData)
        pass

    def run(self):
        self.level.run()
        self.levelUI.run()

        if self.currentGameData.health == 0:
            self.game_over()
