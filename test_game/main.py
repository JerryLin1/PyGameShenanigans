import pygame
from init import entities, WIDTH, HEIGHT, init_entity, FIXED_DT
from test_game import init
from test_game.entity import Entity
from test_game.helpers import draw_rect, Timer

from test_game.player import Player

empty = (0, 0, 0, 0)  # The last 0 indicates 0 alpha, a transparent color


def main():
    pygame.init()
    pygame.display.set_caption("Game")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    running = True
    physics_update_counter = 0

    player = Player(pygame.Vector2(WIDTH // 2, HEIGHT // 2))
    init_entity(player)

    debug_timer = Entity()
    debug_timer.timers["print"] = Timer(2500, lambda: (
        print("Number of entities: " + str(len(entities))),
        print("FPS: " + str(clock.get_fps()))))
    init_entity(debug_timer)
    # main loop
    while running:
        init.events = pygame.event.get()
        screen.fill((0, 0, 0))
        draw_rect(screen, (50, 20, 120), (100, 100, 200, 80))

        dt = clock.tick(60)
        physics_update_counter += dt
        updates = int(physics_update_counter // FIXED_DT)
        physics_update_counter = physics_update_counter % FIXED_DT
        for u in range(updates):
            tick_physics(screen, dt)
        tick_entities(screen, dt)
        for u in range(updates):
            post_tick_physics(screen, dt)
        tick_draw(screen, dt)

        for event in init.events:
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()


def tick_physics(surface, delta_time):
    for i in range(len(entities) - 1, -1, -1):
        entity = entities[i]
        entity.tick_physics()


def tick_entities(surface, delta_time):
    for i in range(len(entities) - 1, -1, -1):
        entity = entities[i]
        entity.tick(delta_time)
        if entity.killed:
            entities.remove(entity)


def tick_draw(surface, delta_time):
    for i in range(len(entities) - 1, -1, -1):
        entity = entities[i]
        entity.draw(surface)


def post_tick_physics(surface, delta_time):
    for i in range(len(entities) - 1, -1, -1):
        entity = entities[i]
        entity.post_tick_physics()


if __name__ == "__main__":
    main()
