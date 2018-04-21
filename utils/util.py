from utils.config import col, row
from copy import deepcopy

from Valid import valid


def move(board, x, y, player, copy=False):
    if copy:
        m = deepcopy(board)
    else:
        m = board
    m.matrix[x][y] = player
    m.chess_cnt = m.chess_cnt + 1
    # 吃掉对方的子
    valid.eat(m.matrix, x, y)
    # print(m.chess_cnt)
    return m

def dumb_score(array, player):
    """
    Simple heuristic. Compares number of each tile.
    :param array: 8x8 matrix
    :param player: 0(player) or 1(computer)
    :return: player - opponent
    """
    score = 0
    # Set player and opponent colors
    color = player
    opponent = 1 - player

    # +1 if it's player color, -1 if it's opponent color
    for x in range(8):
        for y in range(8):
            if array[x][y] == color:
                score += 1
            elif array[x][y] == opponent:
                score -= 1
    return score