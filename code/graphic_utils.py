import pygame


def outlined_surface(surface, pos, display: pygame.Surface):
    mask = pygame.mask.from_surface(surface)
    mask_surf = mask.to_surface(setcolor=(0, 0, 0), unsetcolor=(255, 255, 255))
    mask_surf.set_colorkey((255, 255, 255))
    display.blit(mask_surf, mask_surf.get_rect(center=(pos[0]-1, pos[1])))
    display.blit(mask_surf, mask_surf.get_rect(center=(pos[0]+1, pos[1])))
    display.blit(mask_surf, mask_surf.get_rect(center=(pos[0], pos[1]-1)))
    display.blit(mask_surf, mask_surf.get_rect(center=(pos[0], pos[1]+1)))
