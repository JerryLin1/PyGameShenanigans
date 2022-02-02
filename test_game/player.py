import math
import pygame
import random

from pygame import Vector2

from init import entities, init_entity
from test_game.draw_helpers import draw_circle_alpha
from test_game.entity import Entity
from test_game.particles import Particle, ParticleCircle
from test_game.unit import Unit


class Player(Unit):
    def __init__(self, position):
        Unit.__init__(self, position)
        self.keys = pygame.key.get_pressed()
        self.speed = 3

    def tick(self, tick_time: float, surface):
        self.keys = pygame.key.get_pressed()
        self.position[0] += (self.keys[pygame.K_d] - self.keys[
            pygame.K_a]) * self.speed * tick_time / 20
        self.position[1] += (self.keys[pygame.K_s] - self.keys[
            pygame.K_w]) * self.speed * tick_time / 20
        if self.keys[pygame.K_SPACE]:
            burst_particles(self.position)

        Unit.tick(self, tick_time, surface)

    def draw(self, surface):
        draw_circle_alpha(surface, (255, 255, 255), self.position, 2)


def burst_particles(position, amount=5, force=5):
    for _ in range(amount):
        x = position[0]
        y = position[1]
        angle = random.uniform(0, math.pi * 2)
        vector = Vector2(math.cos(angle), math.sin(angle))
        vector *= random.uniform(0, force)
        init_entity(ParticleCircle(position=(x, y),
                                   color=get_random_color(),
                                   lifespan=1000,
                                   vel=vector,
                                   accel=Vector2(0, 10),
                                   lights=[1, 2]))


def get_random_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return (r, g, b)
