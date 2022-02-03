class Entity:
    def __init__(self):
        self.killed = False
        self.time_since_spawn = 0

    def tick(self, tick_time: float):
        self.time_since_spawn+=tick_time
