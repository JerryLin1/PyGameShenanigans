import pygame
from init import entities, WIDTH, HEIGHT, init_entity

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
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (50, 20, 120), pygame.Rect(100, 100, 200, 80))

        dt = clock.tick(60)

        tick_entities(screen, dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(screen, (0, 0))
        pygame.display.update()


def tick_entities(surface, delta_time):
    for i in range(len(entities)-1, -1, -1):
        entity = entities[i]
        entity.tick(delta_time, surface)
        if entity.killed:
            entities.remove(entity)


if __name__ == "__main__":
    main()
