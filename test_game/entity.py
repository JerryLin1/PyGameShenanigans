from test_game.init import FIXED_DT


class Entity:
    def __init__(self):
        self.killed = False
        self.time_since_spawn = 0
        self.timers = {}

    def tick_physics(self):
        pass
    def post_tick_physics(self):
        for timer in self.timers.values():
            timer.tick(FIXED_DT)

    def tick(self, tick_time: float):
        self.time_since_spawn += tick_time
        self.pre_update(tick_time)
        self.update(tick_time)
        self.post_update(tick_time)

    def draw(self, surface):
        pass

    def update(self, tick_time):
        pass

    def pre_update(self, tick_time):
        pass

    def post_update(self, tick_time):
        pass

    def die(self):
        self.killed = True
