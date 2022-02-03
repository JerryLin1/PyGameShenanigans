import pygame

from test_game.entity import Entity


class Unit(Entity):
    def __init__(self, position):
        Entity.__init__(self)
        self.speed = 3
        self.position = position
        self.timers = {}

    def tick(self, tick_time: float, surface):
        self.draw(surface)
        for timer in self.timers.values():
            timer.tick(tick_time)

    def draw(self, surface):
        raise NotImplementedError
