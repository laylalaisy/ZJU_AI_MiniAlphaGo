import time
import tkinter.messagebox
import pickle
from datetime import datetime

import globals
from Controller import mcts
from state import State
from utils.config import board_left_up_x, board_box_width, board_box_height, board_left_up_y, row, col, black
from utils.util import move
from Valid import valid


class Controller:
    def __init__(self, root, canvas, init_game):
        self.root = root
        self.canvas = canvas
        self.init_game = init_game
        self.total_time = 0

    def set_board(self, board):
        self.board = board
        self.tree = self.get_tree()

    def on_click(self, event):
        # 现在不是该玩家下棋的状态,不处理点击事件
        if globals.state == State.player:
            if event.x <= 50 and event.y <= 50:
                self.init_game(self, globals.player_color, self.canvas)
            else:
                self.player_play(event)
                self.AI_play()
        pass

    def notify(self):
        self.canvas.repaint(self.board)

    @staticmethod
    def get_position(event):
        """
        根据事件的坐标计算是哪一个方格被点击了
        """
        return (event.x - board_left_up_x) // board_box_width, (event.y - board_left_up_y) // board_box_height

    def player_play(self, event):
        x, y = self.get_position(event)
        valid_list = valid.get_valid_list(self.board.matrix, globals.player_color)
        if len(valid_list) != 0:
            # 点的位置不在有效列表里,即点的位置不能下棋
            if (x, y) not in valid_list:
                return
            move(self.board, x, y, globals.player_color)
            # 删除提示
            self.board.valid_matrix = []
            self.notify()
        else:
            print("valid_list is empty! player pass")
            if not self.board.has_empty_box():
                self.finish_game()
        self.switch_player((x, y))

    def AI_play(self):
        if globals.state != State.AI:
            return
        valid_list = valid.get_valid_list(self.board.matrix, globals.AI_color)
        (x, y) = (None, None)
        if len(valid_list) != 0:
            try:
                single_step_begin = time.time()
                (x, y) = self.tree.uct_search()
                single_step_end = time.time()
                self.total_time += single_step_end - single_step_begin
                print('Time used: ', single_step_end - single_step_begin)
                print('AI: ', y + 1, x + 1)
            except Exception:
                print(self.tree.root)
                # print()
            move(self.board, x, y, globals.AI_color)
        else:
            print("valid_list is empty! AI pass")
            if not self.board.has_empty_box():
                self.finish_game()
        self.board.valid_matrix = valid.get_valid_list(self.board.matrix, globals.player_color)
        self.notify()
        if len(self.board.valid_matrix) == 0:
            print("player pass!")
            self.tree.update(self.board, globals.AI_color, (x, y), force_add=True)
            self.AI_play()
        else:
            self.switch_player((x, y))
        pass

    def switch_player(self, pre_move):
        if globals.state == State.player:
            globals.state = State.AI
            player = globals.AI_color
        else:
            globals.state = State.player
            player = globals.player_color
        if pre_move[0] is not None and pre_move[1] is not None:
            self.tree.update(self.board, player, pre_move)

    def finish_game(self):
        winner = self.get_winner()
        tkinter.messagebox.showinfo("游戏结束", winner + "赢了")
        print('total time', self.total_time)
        # self.write(globals.file_name, self.tree)
        globals.state = State.finished

    def get_winner(self):
        player_cnt = 0
        AI_cnt = 0
        for i in range(row):
            for j in range(col):
                if self.board.matrix[i][j] == globals.player_color:
                    player_cnt += 1
                else:
                    AI_cnt += 1
        if player_cnt > AI_cnt:
            return 'player'
        else:
            return 'AI'

    def get_tree(self):
        try:
            tree = self.read(globals.file_name)
            while tree.root.parent is not None:
                tree.root = tree.root.parent
        except FileNotFoundError:
            self.write(globals.file_name)
            tree = self.read(globals.file_name)
        return tree

    @staticmethod
    def read(filename):
        with open(filename, 'rb') as f:
            aa = pickle.load(f)
            return aa

    def write(self, filename, t=None):
        with open(filename, 'wb') as f:
            if t is None:
                t = mcts.MCSearchTree(self.board, black)
            pickle.dump(t, f)
