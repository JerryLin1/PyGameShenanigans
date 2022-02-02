import pygame

from test_game.entity import Entity


class Unit(Entity):
    def __init__(self, position):
        Entity.__init__(self)
        self.speed = 3
        self.position = position

    def tick(self, tick_time: float, surface):
        self.draw(surface)

    def draw(self, surface):
        raise NotImplementedError
