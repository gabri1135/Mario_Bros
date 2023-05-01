from math import sqrt

import pygame


def outlined_surface(surface, pos, size, display: pygame.Surface):
    mask = pygame.mask.from_surface(surface)
    mask_surf = mask.to_surface(
        setcolor='black', unsetcolor=(255, 255, 255, 0))
    for a in range(size+1):
        b = int(sqrt(size**2-a**2))
        display.blit(mask_surf, mask_surf.get_rect(
            center=(pos[0]+a, pos[1]+b)))
        display.blit(mask_surf, mask_surf.get_rect(
            center=(pos[0]-a, pos[1]+b)))
        display.blit(mask_surf, mask_surf.get_rect(
            center=(pos[0]+a, pos[1]-b)))
        display.blit(mask_surf, mask_surf.get_rect(
            center=(pos[0]-a, pos[1]-b)))


def outlined_text(text,  size=25, color='white', **kwargs):
    font = pygame.font.Font('graphics/font.ttf', size)
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect(topleft=(5, 5))

    surface = pygame.Surface(
        (text_surf.get_width()+10, text_surf.get_height()+10), pygame.SRCALPHA)

    outlined_surface(text_surf, text_rect.center,
                     int((size-17.5)//7.5), surface)
    surface.blit(text_surf, text_rect)
    return surface, surface.get_rect(**kwargs)
