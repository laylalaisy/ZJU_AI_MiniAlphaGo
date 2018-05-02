from utils.config import *

def is_valid(list matrix, int x, int y, int color):
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
    # down direct
    if y < row - 2 and matrix[x][y + 1] == 1 - color:
        for i in range(y + 2, row):
            if matrix[x][i] == color:
                return True
            if matrix[x][i] is None:
                break
    # up direct
    if y > 1 and matrix[x][y - 1] == 1 - color:
        for i in range(y - 2, -1, -1):
            if matrix[x][i] == color:
                return True
            if matrix[x][i] is None:
                break
    # down right direct
    if x < col - 2 and y < row - 2 and matrix[x + 1][y + 1] == 1 - color:
        for i in range(2, min(col - x, row - y)):
            if matrix[x + i][y + i] == color:
                return True
            if matrix[x + i][y + i] is None:
                break
    # down left
    if x > 1 and y < row - 2 and matrix[x - 1][y + 1] == 1 - color:
        for i in range(2, min(x + 1, row - y)):
            if matrix[x - i][y + i] == color:
                return True
            if matrix[x - i][y + i] is None:
                break
    # up right
    if x < col - 2 and y > 1 and matrix[x + 1][y - 1] == 1 - color:
        for i in range(2, min(col - x, y + 1)):
            if matrix[x + i][y - i] == color:
                return True
            if matrix[x + i][y - i] is None:
                break
    # up left
    if x > 1 and y > 1 and matrix[x - 1][y - 1] == 1 - color:
        for i in range(2, min(x + 1, y + 1)):
            if matrix[x - i][y - i] == color:
                return True
            if matrix[x - i][y - i] is None:
                break

    return False

def get_valid_list(list matrix, int color):
    cdef list valid_list = []
    for i in range(col):
        for j in range(row):
            if is_valid(matrix, i, j, color):
                valid_list.append((i, j))
    return valid_list


def eat(list matrix, int x, int y):
    cdef int color = matrix[x][y]
    # right
    if x < col - 2 and matrix[x + 1][y] == 1 - color:
        for i in range(x + 2, col):
            if matrix[i][y] == color:
                for j in range(x, i):
                    matrix[j][y] = color
                break
            if matrix[i][y] is None:
                break
    # left direct
    if x > 1 and matrix[x - 1][y] == 1 - color:
        for i in range(x - 2, -1, -1):
            if matrix[i][y] == color:
                for j in range(i, x):
                    matrix[j][y] = color
                break
            if matrix[i][y] is None:
                break
    # down direct
    if y < 6 and matrix[x][y + 1] == 1 - color:
        for i in range(y + 2, 8):
            if matrix[x][i] == color:
                for j in range(y, i):
                    matrix[x][j] = color
                break
            if matrix[x][i] is None:
                break
    # up direct
    if y > 1 and matrix[x][y - 1] == 1 - color:
        for i in range(y - 2, -1, -1):
            if matrix[x][i] == color:
                for j in range(i, y):
                    matrix[x][j] = color
                break
            if matrix[x][i] is None:
                break
    # down right
    if x < col - 2 and y < row - 2 and matrix[x + 1][y + 1] == 1 - color:
        for i in range(2, min(col - x, row - y)):
            if matrix[x + i][y + i] == color:
                for j in range(i):
                    matrix[x + j][y + j] = color
                break
            if matrix[x + i][y + i] is None:
                break
    # down left
    if x > 1 and y < row - 2 and matrix[x - 1][y + 1] == 1 - color:
        for i in range(2, min(x + 1, row - y)):
            if matrix[x - i][y + i] == color:
                for j in range(i):
                    matrix[x - j][y + j] = color
                break
            if matrix[x - i][y + i] is None:
                break
    # up right
    if x < col - 2 and y > 1 and matrix[x + 1][y - 1] == 1 - color:
        for i in range(2, min(col - x, y + 1)):
            if matrix[x + i][y - i] == color:
                for j in range(i):
                    matrix[x + j][y - j] = color
                break
            if matrix[x + i][y - i] is None:
                break
    # up left
    if x > 1 and y > 1 and matrix[x - 1][y - 1] == 1 - color:
        for i in range(2, min(x + 1, y + 1)):
            if matrix[x - i][y - i] == color:
                for j in range(i):
                    matrix[x - j][y - j] = color
                break
            if matrix[x - i][y - i] is None:
                break
    pass

def get_priority_valid_moves(list array, list priority_table, int player=1):
    cdef list valid_moves = []
    for priority in priority_table:
        for (x, y) in priority:
            if is_valid(array, x, y, player):
                valid_moves.append((x, y))
        if len(valid_moves) > 0:
            break
    return valid_moves
