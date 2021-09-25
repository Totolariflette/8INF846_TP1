import numpy as np
from random import randrange


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
        # Générer saleté
        will_add_dirt = randrange(100)
        if will_add_dirt > 75:
            x = randrange(5)
            y = randrange(5)
            self.add_dirt(x, y)
        will_add_jewel = randrange(100)
        # Générer bijou
        if will_add_jewel > 90:
            x = randrange(5)
            y = randrange(5)
            self.add_jewel(x, y)

    def add_dirt(self, x, y):
        case = self.matrix[x][y]
        if case == 0:
            case = 2
        elif case == 1:
            case = 3

    def add_jewel(self, x, y):
        case = self.matrix[x][y]
        if case == 0:
            case = 1
        elif case == 2:
            case = 3
