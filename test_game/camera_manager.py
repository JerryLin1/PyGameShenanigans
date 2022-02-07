import random

from test_game import init
from test_game.entity import Entity
from test_game.helpers import copy_vector2, random_vector2, get_random_color, \
    Light
from test_game.init import get_entity_by_type, init_entity
from test_game.particles import Particle
from test_game.player import Player


class CameraManager(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.player = get_entity_by_type(Player)
        self.camera_pos = init.camera_pos

    def tick_physics(self):

    def update(self, tick_time):
        if self.player is None or self.player.killed:
            self.player = get_entity_by_type(Player)

            vector = random_vector2()
            vector *= random.uniform(0, 100)
            # init_entity(Particle(position=copy_vector2(self.camera_pos),
            #                      color=get_random_color(100, 255,
            #                                             0, 255,
            #                                             0, 255) + (200,),
            #                      lifespan=1000,
            #                      vel=vector,
            #                      lights=[
            #                          Light(2, 0.8)
            #                      ],
            #                      flags=[
            #                          Particle.SCALE_ALPHA_LIFETIME,
            #                          Particle.SCALE_SIZE_LIFETIME,
            #                          Particle.MAIN_DRAW_DISABLED
            #                      ]))

            return
        p = self.player.position
        init.camera_pos = (p[0] - init.WIDTH // 2,
                           p[1] - init.HEIGHT // 2) + self.player.vel * 0.1
