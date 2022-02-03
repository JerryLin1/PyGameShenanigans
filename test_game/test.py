import pygame
from init import entities, WIDTH, HEIGHT, init_entity

from test_game.player import Player

empty = (0, 0, 0, 0)  # The last 0 indicates 0 alpha, a transparent color


def main():
    pygame.init()
    pygame.display.set_caption("Test game")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    screen_main = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    running = True

    player = Player([WIDTH//2, HEIGHT//2])
    init_entity(player)
    # main loop
    while running:
        screen.fill((0, 0, 0))
        screen_main.fill(empty)

        dt = clock.tick(60)

        tick_entities(screen_main, dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(screen_main, (0, 0))
        pygame.display.update()


def tick_entities(surface, delta_time):
    for entity in entities:
        entity.tick(delta_time, surface)
        if entity.killed:
            entities.remove(entity)


if __name__ == "__main__":
    main()
