from csv import reader
from os import walk

import pygame

from settings import tile_size


def import_folder(path: str):
    surfaces = []
    for _, __, files in walk(path):
        sorted_files = sorted(files, key=lambda x: int(x[:-4]))
        for name in sorted_files:
            surfaces.append(pygame.image.load(
                f'{path}/{name}').convert_alpha())
        return surfaces


def import_csv_layout(path: str):
    tiles_map = []
    with open(path, 'r') as file:
        data = reader(file, delimiter=',')
        for row in data:
            tiles_map.append(row)
        return tiles_map


def import_cut_graphics(id: int, path: str, size: int = tile_size):
    image = pygame.image.load(path).convert_alpha()
    image_width = image.get_width()//size
    x, y = id % image_width, id//image_width
    surface = pygame.Surface((size, size), flags=pygame.SRCALPHA)
    surface.blit(image, (0, 0), (x*size, y*size, size, size))
    return surface
