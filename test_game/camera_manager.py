import math
import random

from pygame import Vector2

from test_game import init
from test_game.entity import Entity
from test_game.helpers import copy_vector2, random_vector2, get_random_color, \
    Light, Timer, get_entity_by_type
from test_game.init import FIXED_DT
from test_game.particles import Particle
from test_game.player import Player


class CameraManager(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.player = get_entity_by_type("Player")
        self.vel = Vector2(0, 0)
        self.accel = Vector2(0, 0)
        self.friction = 0.5
        self.speed = 500
        self.timers = {
            "stop_camera_shake": Timer(1000, self.stop_camera_shake, False),
            "randomize_vel": Timer(1000, self.randomize_vel, False)
        }

        self.shake_magnitude = None

    def tick_physics(self):
        if self.player is None or self.player.killed:
            return
        p = self.player.position
        self.vel += self.accel * (FIXED_DT / 1000)

        # "friction"
        self.vel *= self.friction * math.pow(math.e, -(FIXED_DT / 1000))
        if self.accel == Vector2(0, 0):
            # Prevent floating point weirdness
            if self.vel.magnitude() < 0.1:
                self.vel = Vector2(0, 0)
        init.camera_pos += self.vel * (FIXED_DT / 1000)
        # init.camera_pos = (p[0] - init.WIDTH // 2,
        #                    p[1] - init.HEIGHT // 2) + self.player.vel * 0.1

    def update(self, tick_time):
        if self.player is None or self.player.killed:
            self.player = get_entity_by_type("Player")
            return
        p = self.player.position
        padj = (p[0] - init.WIDTH // 2,
                p[1] - init.HEIGHT // 2) + self.player.vel * 0.2
        vector = (padj - init.camera_pos) * self.speed
        self.accel = vector

    def camera_shake(self, magnitude = 200, length = 100, speed=10):
        self.timers.get("stop_camera_shake").time = length
        self.timers.get("stop_camera_shake").is_active = True
        self.timers.get("randomize_vel").time = speed
        self.timers.get("randomize_vel").is_active = True
        self.shake_magnitude = magnitude

    def stop_camera_shake(self):
        # print(self.timers)
        self.timers.get("stop_camera_shake").is_active = False
        self.timers.get("randomize_vel").is_active = False

    def randomize_vel(self):
        self.vel += random_vector2() * random.uniform(0, self.shake_magnitude)
