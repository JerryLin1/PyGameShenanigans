class Entity:
    def __init__(self):
        self.killed = False
        self.time_since_spawn = 0
        self.timers = {}

    def tick(self, tick_time: float):
        self.time_since_spawn += tick_time
        for timer in self.timers.values():
            timer.tick(tick_time)
