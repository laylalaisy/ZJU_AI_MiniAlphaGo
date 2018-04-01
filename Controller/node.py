from Model.board import Board
from utils.util import move
from utils.valid import get_valid_list


class Node:
    board: Board
    player: int
    depth: int

    def __init__(self, board, player):
        self.board = board
        self.depth = 0
        self.parent = None
        self.player = player
        self.children = []
        self.valid_list = get_valid_list(board.matrix, player)
        self.un_tried_list = self.valid_list
        self.n = 0  # 模拟次数
        self.q = 0  # 赢的次数

    def add_child(self, step):
        new_matrix = move(self, step[0], step[1], self.player, copy=True)
        self.children.append(Node(new_matrix, 1 - self.player))
        self.un_tried_list.remove(step)

    def is_fully_expanded(self):
        return len(self.un_tried_list) == 0

    def is_terminal(self):
        return len(self.un_tried_list) == 0 and len(self.children) == 0
