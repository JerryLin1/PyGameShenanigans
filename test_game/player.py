import math
import pygame
import random

from pygame import Vector2

from init import entities, init_entity
from test_game.helpers import draw_circle_alpha
from test_game.entity import Entity
from test_game.helpers import random_vector2, Timer
from test_game.particles import Particle, ParticleCircle
from test_game.unit import Unit


class Player(Unit):
    def __init__(self, position):
        Unit.__init__(self, position)
        self.keys = pygame.key.get_pressed()
        self.prev_keys = self.keys
        self.speed = 3
        self.timers = {
            "trail": Timer(50, self.trail_particle)
        }

    def tick(self, tick_time: float, surface):
        self.keys = pygame.key.get_pressed()
        self.position[0] += (self.key_down(pygame.K_d) - self.key_down(
            pygame.K_a)) * self.speed * tick_time / 20
        self.position[1] += (self.key_down(pygame.K_s) - self.key_down(
            pygame.K_w)) * self.speed * tick_time / 20

        if self.key_up(pygame.K_SPACE):
            burst_particles(self.position)

        self.prev_keys = self.keys
        Unit.tick(self, tick_time, surface)

    def trail_particle(self):
        vector = random_vector2()
        vector *= random.uniform(0, 0.5)
        init_entity(Particle(position=self.position,
                             color=(255, 255, 255),
                             lifespan=2000,
                             vel=vector))

    def draw(self, surface):
        draw_circle_alpha(surface, (255, 255, 255), self.position, 2)

    def key_down(self, key):
        return self.keys[key]

    def key_click(self, key):
        return not self.prev_keys[key] and self.keys[key]

    def key_up(self, key):
        return self.prev_keys[key] and not self.keys[key]


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
                                   # accel=Vector2(0, 10),
                                   lights=[2]))


def get_random_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return (r, g, b)

