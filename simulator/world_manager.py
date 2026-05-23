class WorldManager:
    def __init__(self, world):
        self.world = world

    def set_weather(self, weather):
        self.world.set_weather(weather)