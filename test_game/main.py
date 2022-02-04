import pygame
from init import entities, WIDTH, HEIGHT, init_entity
from test_game import init
from test_game.helpers import draw_rect

from test_game.player import Player

empty = (0, 0, 0, 0)  # The last 0 indicates 0 alpha, a transparent color


def main():
    pygame.init()
    pygame.display.set_caption("Game")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    running = True

    player = Player(pygame.Vector2(WIDTH // 2, HEIGHT // 2))
    init_entity(player)
    # main loop
    while running:
        init.events = pygame.event.get()
        screen.fill((0, 0, 0))
        draw_rect(screen, (50, 20, 120), (100, 100, 200, 80))

        dt = clock.tick(60)

        tick_entities(screen, dt)
        for event in init.events:
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


def tick_entities(surface, delta_time):
    for i in range(len(entities) - 1, -1, -1):
        entity = entities[i]
        entity.tick(delta_time, surface)
        if entity.killed:
            entities.remove(entity)


if __name__ == "__main__":
    main()
