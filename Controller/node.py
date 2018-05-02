from utils.util import move

from Valid import valid


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
        self.n = 0  # simulation times
        self.q = 0  # win times
        self.parent = parent

    def add_child(self, step):
        new_board = move(self.board, step[0], step[1], self.player, copy=True)
        self.children.append(Node(new_board, 1 - self.player, self, step))
        self.un_tried_list.remove(step)

    def is_fully_expanded(self):
        return len(self.un_tried_list) == 0

    def is_terminal(self):
        return len(self.un_tried_list) == 0 and len(self.children) == 0

    def __str__(self):
        return str(self.player) + ' is going to play!\n' + \
               'board: ' + str(self.board) + '\n' + \
               'valid_list: ' + str(self.valid_list) + '\n' + \
               '#children: ' + str(len(self.children)) + '\n'
