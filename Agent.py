import numpy as np
from Sensors import Sensors
from Environment import Environment


class Agent:

    def __init__(self):
        self.sensors = Sensors()

    def update_sensors(self, env: Environment):
        self.sensors.set_matrix(env.get_matrix())

    def get_action(self, env: Environment):
        pass

    def get_dirty_rooms(self):
        rooms_to_clean = []
        for e in self.sensors.matrix:
            if e in [2, 3]:
                format = {}  # TODO formatage des données de la pièce
                rooms_to_clean.append(format)
