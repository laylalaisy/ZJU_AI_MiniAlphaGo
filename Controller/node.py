from Model.board import Board
from utils.util import move

from Valid import valid


# from utils import valid

class Node:

    def __init__(self, board, player, parent, pre_move):
        self.pre_move = pre_move
        self.board = board
        self.depth = 0
        self.parent = None
        self.player = player
        self.children = []
        self.valid_list = valid.get_valid_list(board.matrix, player)
        self.un_tried_list = self.valid_list
        self.n = 0  # 模拟次数
        self.q = 0  # 赢的次数
        self.parent = parent

    def add_child(self, step):
        # print('self:', self)
        new_board = move(self.board, step[0], step[1], self.player, copy=True)
        self.children.append(Node(new_board, 1 - self.player, self, step))
        # print('children len: ', len(self.children))
        self.un_tried_list.remove(step)

    def is_fully_expanded(self):
        # print(len(self.un_tried_list))
        return len(self.un_tried_list) == 0

    def is_terminal(self):
        # print('len(self.children):' + str(len(self.children)))
        return len(self.un_tried_list) == 0 and len(self.children) == 0

    def __str__(self):
        return str(self.player) + ' is going to play!\n' + \
               'board: ' + str(self.board) + '\n' + \
               'valid_list: ' + str(self.valid_list) + '\n' + \
               '#children: ' + str(len(self.children)) + '\n'
