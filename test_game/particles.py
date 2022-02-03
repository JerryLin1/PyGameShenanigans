import math

import pygame
from pygame.math import Vector2
from pygame import draw
from pygame.color import Color

from test_game.helpers import draw_circle_alpha, draw_rect_alpha
from test_game.entity import Entity


class Particle(Entity):
    def __init__(self, position: Vector2, color: Color = (255, 255, 255),
                 lifespan: float = 5000, vel: Vector2 = Vector2(0, 0),
                 accel: Vector2 = Vector2(0, 0), lights=[]):
        Entity.__init__(self)
        self.position = position
        self.lifespan = lifespan
        self.lights = lights
        self.color = color
        self.vel = vel
        self.accel = accel
        self.current_life = 0

    def tick(self, tick_time: float, surface):
        self.current_life += tick_time
        self.vel += self.accel * tick_time / 1000
        self.position += self.vel
        lf = (1 - self.current_life / self.lifespan)
        if lf < 0:
            lf = 0
        self.draw(surface, lf)
        self.draw_light(surface, lf)
        if self.current_life >= self.lifespan:
            self.killed = True

    def draw(self, surface, lf):
        ucol = self.color + (255 * lf,)
        upos = (round(self.position[0] - 1), round(self.position[1] - 1))
        draw_rect_alpha(surface, ucol, upos + (1, 1))

    def draw_light(self, surface, lf):
        for light in self.lights:
            urad = lf * light
            ucol_light = self.color + (100 * lf,)
            draw_circle_alpha(surface, ucol_light, self.position, urad * 6)


class ParticleCircle(Particle):
    def __init__(self, position: Vector2, color: Color = (255, 255, 255),
                 lifespan: float = 5000, vel: Vector2 = Vector2(0, 0),
                 accel: Vector2 = Vector2(0, 0), lights=[], radius: float = 2):
        Particle.__init__(self=self,
                          position=position,
                          lifespan=lifespan,
                          color=color,
                          vel=vel,
                          accel=accel,
                          lights=lights)
        self.radius = radius

    def draw(self, surface, lf):
        urad = math.ceil(lf * self.radius)
        ucol = self.color + (255 * lf,)
        draw_circle_alpha(surface=surface,
                          color=ucol,
                          center=self.position,
                          radius=urad)
