from csv import reader
from os import walk

import pygame

from .settings import tile_size


def import_folder(path: str):
    surfaces = []
    for _, __, files in walk(path):
        sorted_files = sorted(files, key=lambda x: int(x[:-4]))
        for name in sorted_files:
            surfaces.append(pygame.image.load(
                f'{path}/{name}').convert_alpha())
        return surfaces


def import_csv_layout(path: str):
    with open(path, 'r') as file:
        data = reader(file, delimiter=',')
        for row in data:
            yield row


def import_cut_graphics(path: str, size: int = tile_size):
    surfaces = []
    image = pygame.image.load(path).convert_alpha()
    image_width = image.get_width()//size
    image_height = image.get_height()//size
    for y in range(image_height):
        for x in range(image_width):
            surface = pygame.Surface((size, size), flags=pygame.SRCALPHA)
            surface.blit(image, (0, 0), (x*size, y*size, size, size))
            surfaces.append(surface)
    return surfaces
