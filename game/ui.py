import pygame

from .game_data import LevelData
from .graphic_utils import outlined_text
from .utils import import_folder


class LevelUI():
    def __init__(self, surface: pygame.Surface, levelData: LevelData) -> None:
        self.display_surface = surface
        self.levelData = levelData

        self.coin_bag = pygame.image.load(
            'graphics/ui/coin_bag.png').convert_alpha()
        self.health_surfaces = import_folder('graphics/ui/health')

        self.no_starcoin_surf = pygame.image.load(
            'graphics/ui/starcoin/no.png')
        self.starcoin_surf = pygame.image.load(
            'graphics/ui/starcoin/catch.png')

    def run(self):
        # health ui
        self.display_surface.blit(
            self.health_surfaces[self.levelData.health], (20, 20))

        # coins ui
        self.display_surface.blit(self.coin_bag, (20, 70))
        self.display_surface.blit(
            *outlined_text(self.levelData.coin_amount, topleft=(45, 78)))

        for i in range(3):
            x = 100+40*i
            if self.levelData.stars[i]:
                self.display_surface.blit(self.starcoin_surf, (x, 70))
            else:
                self.display_surface.blit(self.no_starcoin_surf, (x, 70))
