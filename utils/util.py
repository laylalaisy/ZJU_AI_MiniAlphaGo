from utils.config import col, row
from copy import deepcopy


def move(board, x, y, player, copy=False):
    if copy:
        m = deepcopy(board)
    else:
        m = board
    m.matrix[x][y] = player
    m.chess_cnt = m.chess_cnt + 1
    # 吃掉对方的子
    eat(m.matrix, x, y)
    # print(m.chess_cnt)
    return m


def eat(matrix, x, y):
    color = matrix[x][y]
    # right
    if x < col - 2 and matrix[x + 1][y] == 1 - color:
        for i in range(x + 2, col):
            if matrix[i][y] == color:
                for j in range(x, i):
                    matrix[j][y] = color
            if matrix[i][y] is None:
                break
    # left direct
    if x > 1 and matrix[x - 1][y] == 1 - color:
        for i in range(x - 2, -1, -1):
            if matrix[i][y] == color:
                for j in range(i, x):
                    matrix[j][y] = color
            if matrix[i][y] is None:
                break
    # down direct
    if y < 6 and matrix[x][y + 1] == 1 - color:
        for i in range(y + 2, 8):
            if matrix[x][i] == color:
                for j in range(y, i):
                    matrix[x][j] = color
            if matrix[x][i] is None:
                break
    # up direct
    if y > 1 and matrix[x][y - 1] == 1 - color:
        for i in range(y - 2, -1, -1):
            if matrix[x][i] == color:
                for j in range(i, y):
                    matrix[x][j] = color
            if matrix[x][i] is None:
                break
    # down right
    if x < col - 2 and y < row - 2 and matrix[x + 1][y + 1] == 1 - color:
        for i in range(2, min(col - x, row - y)):
            if matrix[x + i][y + i] == color:
                for j in range(i):
                    matrix[x + j][y + j] = color
            if matrix[x + i][y + i] is None:
                break
    # down left
    if x > 1 and y < row - 2 and matrix[x - 1][y + 1] == 1 - color:
        for i in range(2, min(x + 1, row - y)):
            if matrix[x - i][y + i] == color:
                for j in range(i):
                    matrix[x - j][y + j] = color
            if matrix[x - i][y + i] is None:
                break
    # up right
    if x < col - 2 and y > 1 and matrix[x + 1][y - 1] == 1 - color:
        for i in range(2, min(col - x, y + 1)):
            if matrix[x + i][y - i] == color:
                for j in range(i):
                    matrix[x + j][y - j] = color
            if matrix[x + i][y - i] is None:
                break
    # up left
    if x > 1 and y > 1 and matrix[x - 1][y - 1] == 1 - color:
        for i in range(2, min(x + 1, y + 1)):
            if matrix[x - i][y - i] == color:
                for j in range(i):
                    matrix[x - j][y - j] = color
            if matrix[x - i][y - i] is None:
                break
    pass
