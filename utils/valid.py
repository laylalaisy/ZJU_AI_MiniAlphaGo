from utils.config import *


def is_valid(matrix, x, y, color):
    if matrix[x][y] is not None:
        return False
    # right
    if x < col - 2:
        for i in range(x + 1, col):
            if matrix[i][y] is None:
                return False
            elif matrix[i][y] == color and i - x > 1:
                return True
    # TODO: test right and implement  left,up,down...
    pass


def get_valid_list(matrix, valid_list, color):
    for i in range(col):
        for j in range(row):
            if is_valid(matrix, i, j, color):
                valid_list.append((i, j))
