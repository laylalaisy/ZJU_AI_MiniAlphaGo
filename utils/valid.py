from Model.board import Board
from utils.config import *
from copy import deepcopy

from Model.board import Board
from utils.config import *
from copy import deepcopy


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


def get_valid_list(matrix, color):
    valid_list = []
    for i in range(col):
        for j in range(row):
            if is_valid(matrix, i, j, color):
                valid_list.append((i, j))
    return valid_list


# def move(Board board, x, y, player, bool copy=False):
#     Board m
#     if copy:
#         m = deepcopy(board)
#     else:
#         m = board
#     m.matrix[x][y] = player
#     m.chess_cnt = m.chess_cnt + 1
#     # 吃掉对方的子
#     eat(m.matrix, x, y)
#     # print(m.chess_cnt)
#     return m


def eat(matrix, x, y):
    color = matrix[x][y]
    # right
    if x < col - 2 and matrix[x + 1][y] == 1 - color:
        for i in range(x + 2, col):
            if matrix[i][y] == color:
                for j in range(x, i):
                    matrix[j][y] = color
                # if matrix[i][y] is None:
                #     break
                break
    # left direct
    if x > 1 and matrix[x - 1][y] == 1 - color:
        for i in range(x - 2, -1, -1):
            if matrix[i][y] == color:
                for j in range(i, x):
                    matrix[j][y] = color
                # if matrix[i][y] is None:
                #     break
                break
    # down direct
    if y < 6 and matrix[x][y + 1] == 1 - color:
        for i in range(y + 2, 8):
            if matrix[x][i] == color:
                for j in range(y, i):
                    matrix[x][j] = color
                # if matrix[x][i] is None:
                #     break
                break
    # up direct
    if y > 1 and matrix[x][y - 1] == 1 - color:
        for i in range(y - 2, -1, -1):
            if matrix[x][i] == color:
                for j in range(i, y):
                    matrix[x][j] = color
                # if matrix[x][i] is None:
                #     break
                break
    # down right
    if x < col - 2 and y < row - 2 and matrix[x + 1][y + 1] == 1 - color:
        for i in range(2, min(col - x, row - y)):
            if matrix[x + i][y + i] == color:
                for j in range(i):
                    matrix[x + j][y + j] = color
                # if matrix[x + i][y + i] is None:
                #     break
                break
    # down left
    if x > 1 and y < row - 2 and matrix[x - 1][y + 1] == 1 - color:
        for i in range(2, min(x + 1, row - y)):
            if matrix[x - i][y + i] == color:
                for j in range(i):
                    matrix[x - j][y + j] = color
                # if matrix[x - i][y + i] is None:
                #     break
                break
    # up right
    if x < col - 2 and y > 1 and matrix[x + 1][y - 1] == 1 - color:
        for i in range(2, min(col - x, y + 1)):
            if matrix[x + i][y - i] == color:
                for j in range(i):
                    matrix[x + j][y - j] = color
                # if matrix[x + i][y - i] is None:
                #     break
                break
    # up left
    if x > 1 and y > 1 and matrix[x - 1][y - 1] == 1 - color:
        for i in range(2, min(x + 1, y + 1)):
            if matrix[x - i][y - i] == color:
                for j in range(i):
                    matrix[x - j][y - j] = color
                # if matrix[x - i][y - i] is None:
                #     break
                break
    pass


def get_priority_valid_moves(array, priority_table, player=1):
    """
    get the valid moves of the same priority.
    :param array: 8x8 matrix
    :param priority_table: 优先表
    :param player: 默认为计算机
    :return: valid list
    """
    valid_moves = []
    for priority in priority_table:
        for (x, y) in priority:
            if is_valid(array, x, y, player):
                valid_moves.append((x, y))
        if len(valid_moves) > 0:
            break
    return valid_moves


if __name__ == '__main__':
    matrix = []
    for i in range(8):
        matrix.append([])
        for j in range(8):
            matrix[i].append(None)
    matrix[0][2] = matrix[0][3] = matrix[0][4] = matrix[0][6] = 0
    matrix[0][5] = matrix[0][7] = 1
    matrix[0][1] = 1
    eat(matrix, 0, 1)
    print(matrix)