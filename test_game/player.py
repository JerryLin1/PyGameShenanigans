import math
import pygame
import random

from pygame import Vector2

from init import init_entity
from test_game import init
from test_game.helpers import draw_circle, kill, copy_vector2, \
    get_random_color, get_mouse_pos_global
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
            # This will call trail_particle ever 5 ms when moving
            "trail": Timer(5, self.trail_particle, is_active=False),
            "shoot": Timer(250, self.shoot_particle, is_active=False)
        }
        self.light = Particle(position=self.position,
                              color=(20, 20, 20),
                              lifespan=-1,
                              lights=[10],
                              flags=[Particle.LIGHT_FLICKER,
                                     Particle.MAIN_DRAW_DISABLED])
        init_entity(self.light)

    def update(self, tick_time: float, surface):
        init.camera_pos.update(self.position[0] - init.WIDTH // 2,
                               self.position[1] - init.HEIGHT // 2)
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
            burst_particles(self.position)

        for event in init.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot_particle()
                self.timers["shoot"].is_active = True
                self.timers["shoot"].reset()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.timers["shoot"].is_active = False

        self.prev_keys = self.keys

        self.light.position = copy_vector2(self.position)

    def trail_particle(self, number=5):
        for i in range(number):
            vector = random_vector2()
            vector *= random.uniform(0, 1)
            init_entity(Particle(position=copy_vector2(self.position),
                                 color=get_random_color(100, 255, 0, 100, 0,
                                                        100),
                                 lifespan=1000,
                                 vel=vector,
                                 lights=[2],
                                 flags=[
                                     Particle.SCALE_ALPHA_LIFETIME,
                                     Particle.SCALE_SIZE_LIFETIME,
                                     Particle.MAIN_DRAW_DISABLED
                                 ]))

    def shoot_particle(self):
        shoot_force = 8
        mouse_pos = get_mouse_pos_global()
        diff_vec = mouse_pos - self.position
        diff_vec = diff_vec.normalize() * shoot_force
        init_entity(ParticleCircle(position=copy_vector2(self.position),
                                   color=(255, 255, 255),
                                   radius=1,
                                   lifespan=5000,
                                   vel=diff_vec))

    def draw(self, surface):
        draw_circle(surface, (219, 0, 44), self.position, 3)
        draw_circle(surface, (255, 255, 255), self.position, 2)

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
                                   color=get_random_color(50, 255,
                                                          50, 255,
                                                          50, 255),
                                   lifespan=1000,
                                   vel=vector,
                                   # accel=Vector2(0, 10),
                                   lights=[10],
                                   flags=[
                                       Particle.SCALE_SIZE_LIFETIME,
                                       Particle.SCALE_ALPHA_LIFETIME
                                   ]
                                   ))
