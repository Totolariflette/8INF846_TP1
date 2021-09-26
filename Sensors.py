import numpy as np


class Sensors:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.matrix = np.zeros((5, 5))

    def set_matrix(self, matrix):
        self.matrix = matrix
