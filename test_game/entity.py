class Entity:
    def __init__(self):
        self.killed = False
        self.time_since_spawn = 0
        self.timers = {}

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
        for timer in self.timers.values():
            timer.tick(tick_time)

