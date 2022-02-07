import pygame

# Global variables

entities = []
events = []
camera_pos = pygame.Vector2(0, 0)
WIDTH = 320
HEIGHT = 224
PHYSICS_UPDATES_PER_SECOND = 60
FIXED_DT = 1 / PHYSICS_UPDATES_PER_SECOND * 1000