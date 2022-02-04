import math

import pygame
from pygame.math import Vector2
from pygame import draw
from pygame.color import Color

from test_game.helpers import draw_circle, draw_rect
from test_game.entity import Entity


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
        self.vel = vel
        self.accel = accel
        self.current_life = 0
        self.flags = flags

    def tick(self, tick_time: float, surface):
        Entity.tick(self, tick_time)
        lf = (1 - self.current_life / self.lifespan)
        if lf < 0:
            lf = 0
        self.draw(surface, lf)
        self.draw_light(surface, lf)
        self.vel += self.accel * tick_time / 1000
        self.position += self.vel
        if self.lifespan >= 0:
            self.current_life += tick_time
            if self.current_life >= self.lifespan:
                self.killed = True

    def draw(self, surface, lf):
        if Particle.MAIN_DRAW_DISABLED in self.flags:
            return
        if Particle.SCALE_ALPHA_LIFETIME in self.flags:
            ucol = self.color + (255 * lf,)
        else:
            ucol = self.color
        upos = (round(self.position[0] - 1), round(self.position[1] - 1))
        draw_rect(surface, ucol, upos + (1, 1))

    def draw_light(self, surface, lf):
        for light in self.lights:
            if Particle.SCALE_SIZE_LIFETIME in self.flags:
                urad = lf * light
            else:
                urad = light
            if Particle.LIGHT_FLICKER in self.flags:
                urad = 0.2 * math.sin(0.005 * self.time_since_spawn) + urad
                if urad < 0:
                    urad = 0

            if Particle.SCALE_ALPHA_LIFETIME in self.flags:
                c = self.color
                ucol = (c[0] * lf, c[1] * lf, c[2] * lf)
            else:
                ucol = self.color

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

    def draw(self, surface, lf):
        if Particle.SCALE_SIZE_LIFETIME in self.flags:
            urad = math.ceil(lf * self.radius)
        else:
            urad = self.radius
        if Particle.SCALE_ALPHA_LIFETIME in self.flags:
            ucol = self.color + (255 * lf,)
        else:
            ucol = self.color
        draw_circle(surface=surface,
                    color=ucol,
                    center=self.position,
                    radius=urad)
