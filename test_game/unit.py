import pygame

from test_game.entity import Entity


# Active game objects with basic physics
class Unit(Entity):
    def __init__(self, position: pygame.Vector2):
        Entity.__init__(self)
        self.speed = 3
        self.position = position

        self.accel = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.friction = 0.8

    def tick(self, tick_time: float, surface):
        Entity.tick(self, tick_time)
        # Physics
        self.vel += self.accel * tick_time / 1000
        # "friction"
        self.vel *= self.friction
        if self.accel == pygame.Vector2(0, 0):
            # Prevent floating point weirdness
            if self.vel.magnitude() < 0.1:
                self.vel = pygame.Vector2(0, 0)
        self.position += self.vel

        self.update(tick_time, surface)
        self.draw(surface)

    def update(self, tick_time, surface):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError
