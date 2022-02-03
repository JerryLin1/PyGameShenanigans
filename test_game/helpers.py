import math
import random

import pygame

# https://stackoverflow.com/a/64630102
from test_game.entity import Entity


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color,
                        [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def random_vector2() -> pygame.Vector2:
    """
    Generates a normalized Vector2 pointing in a random direction
    :return: Randomized Vector2 with length 1
    """
    angle = random.uniform(0, math.pi * 2)
    vector = pygame.Vector2(math.cos(angle), math.sin(angle))
    return vector


def copy_vector2(vector: pygame.Vector2) -> pygame.Vector2:
    """
    Returns a copy of the Vector2
    :param vector: Vector2 to be copied
    :return: New Vector2 with same values
    """
    return pygame.Vector2(vector.x, vector.y)


def kill(entity: Entity):
    """
    Kills the entity to be removed from the global entities array
    :param entity: The entity to be killed
    """
    entity.killed = True


def get_random_color(rmin=0, rmax=255,
                     gmin=0, gmax=255,
                     bmin=0, bmax=255):
    """
    Returns a random color using RGB values
    :param rmin: Min red value
    :param rmax: Max red value
    :param gmin: Min green value
    :param gmax: Max green value
    :param bmin: Min blue value
    :param bmax: Max blue value
    :return: A tuple representing the random color
    """
    r = random.randint(rmin, rmax)
    g = random.randint(gmin, gmax)
    b = random.randint(bmin, bmax)
    return r, g, b


class Timer:
    def __init__(self, time, callback, is_active=True):
        self.time = time
        self.elapsed = 0
        self.callback = callback
        self.is_active = is_active

    def tick(self, tick_time):
        if not self.is_active:
            return
        self.elapsed += tick_time
        if self.elapsed >= self.time:
            self.elapsed = 0
            self.callback()
