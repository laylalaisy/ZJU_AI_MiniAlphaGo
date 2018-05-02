from utils.config import *


class Board:
    def __init__(self):
        self.chess_cnt = 4
        self.matrix = []
        self.valid_matrix = []
        for i in range(row):
            self.matrix.append([])
            for j in range(col):
                self.matrix[i].append(None)
        self.matrix[3][3] = white
        self.matrix[4][4] = white
        self.matrix[3][4] = black
        self.matrix[4][3] = black

    def has_empty_box(self):
        for i in range(row):
            for j in range(col):
                if self.matrix[i][j] is None:
                    return True
        return False

    def __str__(self):
        return str(self.matrix)

