class Entity:
    def __init__(self):
        self.killed = False

    def tick(self, tick_time: float):
        raise NotImplementedError
