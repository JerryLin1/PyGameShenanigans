import math

import pygame
from pygame.math import Vector2
from pygame import draw
from pygame.color import Color
import random
from init import entities

from particles import Particle, ParticleCircle
from test_game.player import Unit

WIDTH = 240
HEIGHT = 180

empty = (0, 0, 0, 0)  # The last 0 indicates 0 alpha, a transparent color


def main():
    pygame.init()
    pygame.display.set_caption("Test game")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    screen_main = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    running = True
    player = Unit([0, 0])
    entities.append(player)
    # main loop
    while running:
        screen.fill((0, 0, 0))
        screen_main.fill(empty)

        dt = clock.tick(60)

        tick_entities(screen_main, entities, dt)
        for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONUP:
            #     x, y = pygame.mouse.get_pos()
            #     burst_particles((x, y), 200)
            if event.type == pygame.QUIT:
                running = False
        screen.blit(screen_main, (0, 0))
        pygame.display.update()


def tick_entities(surface, entities, delta_time):
    for entity in entities:
        entity.tick(delta_time, surface)
        if entity.killed:
            entities.remove(entity)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
