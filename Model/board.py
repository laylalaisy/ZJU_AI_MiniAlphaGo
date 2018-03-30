from utils.config import *


class Board:
    def __init__(self):
        self.matrix = []
        for i in range(row):
            self.matrix.append([])
            for j in range(col):
                self.matrix[i].append(None)
        self.matrix[3][3] = black
        self.matrix[4][4] = black
        self.matrix[3][4] = white
        self.matrix[4][3] = white
        # print(self.matrix)
