import math
import pygame
import random

from pygame import Vector2

from init import entities, init_entity
from test_game.helpers import draw_circle_alpha, kill, copy_vector2, \
    get_random_color
from test_game.entity import Entity
from test_game.helpers import random_vector2, Timer
from test_game.particles import Particle, ParticleCircle
from test_game.unit import Unit


class Player(Unit):
    def __init__(self, position: pygame.Vector2):
        Unit.__init__(self, position)
        self.keys = pygame.key.get_pressed()
        self.prev_keys = self.keys
        self.speed = 2
        self.timers = {
            "trail": Timer(10, self.trail_particle)
        }
        self.light = Particle(position=self.position,
                              color=get_random_color(),
                              lifespan=-1,
                              lights=[5])
        init_entity(self.light)

    def tick(self, tick_time: float, surface):
        self.keys = pygame.key.get_pressed()

        # If moving
        if (self.key_down(pygame.K_d)
                or self.key_down(pygame.K_a)
                or self.key_down(pygame.K_s)
                or self.key_down(pygame.K_w)):
            self.accel[0] = (self.key_down(pygame.K_d) - self.key_down(
                pygame.K_a)) * self.speed * tick_time
            self.accel[1] = (self.key_down(pygame.K_s) - self.key_down(
                pygame.K_w)) * self.speed * tick_time
            self.timers["trail"].is_active = True

        # If not moving
        else:
            self.accel = Vector2(0, 0)
            self.timers["trail"].is_active = False
            if self.vel.magnitude() < 0.1:
                self.vel = pygame.Vector2(0, 0)

        if self.key_up(pygame.K_SPACE):
            # kill(self)
            burst_particles(self.position, 5)

        self.prev_keys = self.keys
        Unit.tick(self, tick_time, surface)

        self.light.lights[0] = 0.2 * math.sin(0.005 * self.time_since_spawn) + 5
        self.light.position = copy_vector2(self.position)

    def trail_particle(self, number=1):
        for i in range(number):
            vector = random_vector2()
            vector *= random.uniform(0, 1)
            init_entity(Particle(position=copy_vector2(self.position),
                                 color=get_random_color(100, 255, 0, 50, 0, 50),
                                 lifespan=500,
                                 vel=vector,
                                 flags=[
                                     Particle.SCALE_ALPHA_LIFETIME
                                 ]))

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
        flags = [
            Particle.SCALE_SIZE_LIFETIME,
            Particle.SCALE_ALPHA_LIFETIME
        ]
        init_entity(ParticleCircle(position=(x, y),
                                   color=get_random_color(50, 255, 50, 255, 50,
                                                          255),
                                   lifespan=1000,
                                   vel=vector,
                                   # accel=Vector2(0, 10),
                                   lights=[2],
                                   flags=flags))
