import tkinter.messagebox

import globals
from Controller import mcts
from Controller.node import Node
from state import State
from utils.util import move
from utils.valid import *


class Controller:
    def __init__(self, board, canvas, state):
        # super().__init__()
        self.board = board
        self.canvas = canvas
        # self.state = state
        pass

    def on_click(self, event):
        # print(self.state)
        # 现在不是该玩家下棋的状态,不处理点击事件
        if globals.state == State.player:
            self.player_play(event)
            self.AI_play()
        pass

    def notify(self):
        self.canvas.repaint(self.board)

    def get_position(self, event):
        """
        根据事件的坐标计算是哪一个方格被点击了

        """
        return (event.x - board_left_up_x) // board_box_width, (event.y - board_left_up_y) // board_box_height

    def player_play(self, event):
        x, y = self.get_position(event)
        valid_list = get_valid_list(self.board.matrix, globals.player_color)
        if len(valid_list) != 0:
            # 点的位置不在有效列表里,即点的位置不能下棋
            if (x, y) not in valid_list:
                return
            # self.move(globals.player_color, x, y)
            move(self.board, x, y, globals.player_color)
            # 删除提示
            self.board.valid_matrix = []
            # modify self.board according to x and y
            self.notify()
        else:
            print("valid_list is empty! player pass")
            if not self.board.has_empty_box():
                self.finish_game()
        globals.state = State.AI

    def AI_play(self):
        if globals.state != State.AI:
            return
        # self.board.AI_timer.start()
        valid_list = get_valid_list(self.board.matrix, globals.AI_color)
        if len(valid_list) != 0:
            (x, y) = mcts.MCSearchTree(Node(self.board, globals.AI_color)).uct_search()
            move(self.board, x, y, globals.AI_color)
        else:
            print("valid_list is empty! AI pass")
            if not self.board.has_empty_box():
                self.finish_game()
        # globals.state = State.player
        self.board.valid_matrix = get_valid_list(self.board.matrix, globals.player_color)
        self.notify()
        if len(self.board.valid_matrix) == 0:
            print("player pass!")
            self.AI_play()
        else:
            globals.state = State.player
            # self.board.player_timer.start()
        pass

    def finish_game(self):
        winner = self.get_winner()
        tkinter.messagebox.showinfo("游戏结束", winner + "赢了")
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
