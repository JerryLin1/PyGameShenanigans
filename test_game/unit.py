import math

import pygame

from test_game.entity import Entity


# Active game objects with basic physics
from test_game.init import FIXED_DT


class Unit(Entity):
    def __init__(self, position: pygame.Vector2):
        Entity.__init__(self)
        self.position = position

        self.accel = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.friction = 0.9

    def tick_physics(self):
        Entity.tick_physics(self)
        # Physics
        self.vel += self.accel * (FIXED_DT / 1000)

        # "friction"
        self.vel *= self.friction * math.pow(math.e, -(FIXED_DT / 1000))
        if self.accel == pygame.Vector2(0, 0):
            # Prevent floating point weirdness
            if self.vel.magnitude() < 0.1:
                self.vel = pygame.Vector2(0, 0)
        self.position += self.vel * (FIXED_DT / 1000)

    def draw(self, surface):
        raise NotImplementedError
