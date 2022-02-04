import pygame

# Global variables
entities = []
camera_pos = pygame.Vector2(0, 0)
WIDTH = 320
HEIGHT = 224


def init_entity(entity):
    entities.append(entity)
