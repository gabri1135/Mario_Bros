import sys

import pygame

from .graphic_utils import outlined_text
from .settings import screen_fps, screen_height, screen_width


class PopUp:
    def __init__(self, texts, surface: pygame.Surface) -> None:
        self.display_surface = surface

        self.base_surf = pygame.image.load(
            'graphics/pop_up/base.png').convert_alpha()
        self.base_rect = self.base_surf.get_rect(
            center=(screen_width//2, screen_height//2))

        self.button_surf = pygame.image.load(
            'graphics/pop_up/button.png').convert_alpha()
        self.buttons_rect = [self.button_surf.get_rect(
            center=(screen_width//2, screen_height//2-50)), self.button_surf.get_rect(
            center=(screen_width//2, screen_height//2+50))]

        self.texts_surf = []
        self.texts_rect = []
        for idx, text in enumerate(texts):
            surf, rect = outlined_text(
                text, 40, 'yellow', center=self.buttons_rect[idx].center)
            self.texts_surf.append(surf)
            self.texts_rect.append(rect)

        self.selected = 0
        self.selected_surf = pygame.image.load(
            'graphics/pop_up/selected.png').convert_alpha()
        self.selected_rect = self.selected_surf.get_rect(
            center=self.buttons_rect[self.selected].center)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.selected == 1:
            self.selected = 0
            self.selected_rect = self.selected_surf.get_rect(
                center=self.buttons_rect[self.selected].center)
        elif keys[pygame.K_DOWN] and self.selected == 0:
            self.selected = 1
            self.selected_rect = self.selected_surf.get_rect(
                center=self.buttons_rect[self.selected].center)
        elif keys[pygame.K_RETURN]:
            return True
        return False

    def run(self):
        if self.input():
            return self.selected

        self.display_surface.blit(self.base_surf, self.base_rect)

        for button_rect in self.buttons_rect:
            self.display_surface.blit(self.button_surf, button_rect)

        for text_surf, text_rect in zip(self.texts_surf, self.texts_rect):
            self.display_surface.blit(text_surf, text_rect)

        self.display_surface.blit(self.selected_surf, self.selected_rect)

        return None


def buildPopUp(surface):
    clock = pygame.time.Clock()
    popUp = PopUp(['Continua', 'Scelta livelli'], surface)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (r := popUp.run()) != None:
            return r
        pygame.display.update()
        clock.tick(screen_fps)
