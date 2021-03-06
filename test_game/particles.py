import math

import pygame
from pygame.math import Vector2
from pygame import draw
from pygame.color import Color

from test_game.helpers import draw_circle, draw_rect, kill
from test_game.entity import Entity
from test_game.init import FIXED_DT


class Particle(Entity):
    SCALE_ALPHA_LIFETIME = 0
    SCALE_SIZE_LIFETIME = 1
    LIGHT_FLICKER = 2
    MAIN_DRAW_DISABLED = 3

    def __init__(self, position: Vector2, color: Color = (255, 255, 255),
                 lifespan: float = 5000, vel: Vector2 = Vector2(0, 0),
                 accel: Vector2 = Vector2(0, 0), lights=[], flags: list = []):
        Entity.__init__(self)
        self.position = position
        self.lifespan = lifespan
        self.lights = lights
        self.color = color
        if len(self.color) == 3:
            self.color = color + (255,)
        self.vel = vel
        self.accel = accel
        self.flags = flags
        self.lf = 1

    def tick_physics(self):
        self.vel += self.accel * (FIXED_DT / 1000)
        self.position += self.vel * (FIXED_DT / 1000)

    def update(self, tick_time: float):
        if self.lifespan >= 0:
            if self.time_since_spawn >= self.lifespan:
                kill(self)
        self.lf = (1 - self.time_since_spawn / self.lifespan)
        if self.lf < 0:
            self.lf = 0

    def draw(self, surface):
        if Particle.MAIN_DRAW_DISABLED not in self.flags:
            if Particle.SCALE_ALPHA_LIFETIME in self.flags:
                c = self.color
                ucol = (c[0], c[1], c[2], c[3] * self.lf)
            else:
                ucol = self.color
            upos = (round(self.position[0] - 1), round(self.position[1] - 1))
            draw_rect(surface, ucol, upos + (1, 1))
        self.draw_light(surface)

    def draw_light(self, surface):
        for light in self.lights:
            if Particle.SCALE_SIZE_LIFETIME in self.flags:
                urad = self.lf * light.radius
            else:
                urad = light.radius
            if Particle.LIGHT_FLICKER in self.flags:
                urad = 0.2 * math.sin(0.005 * self.time_since_spawn) + urad
                if urad < 0:
                    urad = 0

            # Handles when particle size is very small.
            # TODO: Change to make it draw a pixel instead
            if urad < 1:
                urad = 1

            if light.color is None:
                c = self.color
            else:
                c = light.color
            if Particle.SCALE_ALPHA_LIFETIME in self.flags:
                ucol = (c[0] * self.lf * light.strength,
                        c[1] * self.lf * light.strength,
                        c[2] * self.lf * light.strength)
            else:
                ucol = (c[0] * light.strength,
                        c[1] * light.strength,
                        c[2] * light.strength)

            draw_circle(surface, ucol, self.position, urad,
                        light=True)


class ParticleCircle(Particle):
    def __init__(self, position: Vector2, color: Color = (255, 255, 255),
                 lifespan: float = 5000, vel: Vector2 = Vector2(0, 0),
                 accel: Vector2 = Vector2(0, 0), lights=[], flags=[],
                 radius: float = 2):
        Particle.__init__(self=self,
                          position=position,
                          lifespan=lifespan,
                          color=color,
                          vel=vel,
                          accel=accel,
                          lights=lights,
                          flags=flags)
        self.radius = radius

    def draw(self, surface):
        if Particle.MAIN_DRAW_DISABLED not in self.flags:
            if Particle.SCALE_SIZE_LIFETIME in self.flags:
                urad = math.ceil(self.lf * self.radius)
            else:
                urad = self.radius

            # Very small handling, change to pixel
            if urad < 1:
                urad = 1

            if Particle.SCALE_ALPHA_LIFETIME in self.flags:
                c = self.color
                ucol = (c[0], c[1], c[2], c[3] * self.lf)
            else:
                ucol = self.color
            draw_circle(surface=surface,
                        color=ucol,
                        center=self.position,
                        radius=urad)
        self.draw_light(surface)
