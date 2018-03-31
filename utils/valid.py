from utils.config import *


def is_valid(matrix, x, y, color):
    if matrix[x][y] is not None:
        return False
    # right
    if x < col - 2 and matrix[x + 1][y] == 1 - color:
        for i in range(x + 2, col):
            if matrix[i][y] == color:
                return True
            if matrix[i][y] is None:
                break
    # left direct
    if x > 1 and matrix[x - 1][y] == 1 - color:
        for i in range(x - 2, -1, -1):
            if matrix[i][y] == color:
                return True
            if matrix[i][y] is None:
                break
    # up direct
    if y < 6 and matrix[x][y + 1] == 1 - color:
        for i in range(y + 2, 8):
            if matrix[x][i] == color:
                return True
            if matrix[x][i] is None:
                break
    # down direct
    if y > 1 and matrix[x][y - 1] == 1 - color:
        for i in range(y - 2, -1, -1):
            if matrix[x][i] == color:
                return True
            if matrix[x][i] is None:
                break
    # up right direct
    if x < 6 and y < 6 and matrix[x + 1][y + 1] == 1 - color:
        for i in range(2, min(8 - x, 8 - y)):
            if matrix[x + i][y + i] == color:
                return True
            if matrix[x + i][y + i] is None:
                break
    # up left
    if x > 1 and y < 6 and matrix[x - 1][y + 1] == 1 - color:
        for i in range(2, min(x + 1, 8 - y)):
            if matrix[x - i][y + i] == color:
                return True
            if matrix[x - i][y + i] is None:
                break
    # down right
    if x < 6 and y > 1 and matrix[x + 1][y - 1] == 1 - color:
        for i in range(2, min(8 - x, y + 1)):
            if matrix[x + i][y - i] == color:
                return True
            if matrix[x + i][y - i] is None:
                break
    # down left
    if x > 1 and y > 1 and matrix[x - 1][y - 1] == 1 - color:
        for i in range(2, min(x + 1, y + 1)):
            if matrix[x - i][y - i] == color:
                return True
            if matrix[x - i][y - i] is None:
                break

    return False


def get_valid_list(matrix, color):
    valid_list = []
    for i in range(col):
        for j in range(row):
            if is_valid(matrix, i, j, color):
                valid_list.append((i, j))
    return valid_list