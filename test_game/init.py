import pygame

# Global variables
entities = []
events = []
camera_pos = pygame.Vector2(0, 0)
WIDTH = 320
HEIGHT = 224
PHYSICS_UPDATES_PER_SECOND = 60
FIXED_DT = 1 / PHYSICS_UPDATES_PER_SECOND * 1000


def init_entity(entity):
    entities.append(entity)


def get_entity_by_type(entity_type):
    for entity in entities:
        if type(entity) == entity_type:
            return entity
    return None
