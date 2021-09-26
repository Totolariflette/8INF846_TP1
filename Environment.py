import numpy as np
from random import randrange
import time


# Etats :
# 0 clean
# 1 jewel
# 2 dirt
# 3 jewel + dirt

class Environment:
    def __init__(self):
        self.matrix = np.zeros((5, 5))

    def get_matrix(self):
        return self.matrix.copy()

    def update_environment(self):
        while True:
            # Générer saleté
            probability = randrange(100)
            if probability > 75:
                x = randrange(5)
                y = randrange(5)
                self.add_dirt(x, y)
            # Générer bijou
            if probability < 10:
                x = randrange(5)
                y = randrange(5)
                self.add_jewel(x, y)

            time.sleep(2)

    def add_dirt(self, x, y):
        if self.matrix[x][y] == 0:
            self.matrix[x][y] = 2
        elif self.matrix[x][y] == 1:
            self.matrix[x][y] = 3

    def add_jewel(self, x, y):
        if self.matrix[x][y] == 0:
            self.matrix[x][y] = 1
        elif self.matrix[x][y] == 2:
            self.matrix[x][y] = 3
