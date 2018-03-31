import tkinter.messagebox

import globals
from Controller.AI import AI
from state import State
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
            # 玩家放子
            self.board.matrix[x][y] = globals.player_color
            # 删除提示
            self.board.valid_matrix = []
            # 吃掉对方的子
            self.eat(x, y)
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
        self.board.AI_timer.start()
        valid_list = get_valid_list(self.board.matrix, globals.AI_color)
        if len(valid_list) != 0:
            (x, y) = AI.play(self.board.matrix, valid_list)
            self.board.matrix[x][y] = globals.AI_color
            self.eat(x, y)
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
            self.board.player_timer.start()
        pass

    def eat(self, x, y):
        color = self.board.matrix[x][y]
        # right
        if x < col - 2 and self.board.matrix[x + 1][y] == 1 - color:
            for i in range(x + 2, col):
                if self.board.matrix[i][y] == color:
                    for j in range(x, i):
                        self.board.matrix[j][y] = color
                if self.board.matrix[i][y] is None:
                    break
        # left direct
        if x > 1 and self.board.matrix[x - 1][y] == 1 - color:
            for i in range(x - 2, -1, -1):
                if self.board.matrix[i][y] == color:
                    for j in range(i, x):
                        self.board.matrix[j][y] = color
                if self.board.matrix[i][y] is None:
                    break
        # down direct
        if y < 6 and self.board.matrix[x][y + 1] == 1 - color:
            for i in range(y + 2, 8):
                if self.board.matrix[x][i] == color:
                    for j in range(y, i):
                        self.board.matrix[x][j] = color
                if self.board.matrix[x][i] is None:
                    break
        # up direct
        if y > 1 and self.board.matrix[x][y - 1] == 1 - color:
            for i in range(y - 2, -1, -1):
                if self.board.matrix[x][i] == color:
                    for j in range(i, y):
                        self.board.matrix[x][j] = color
                if self.board.matrix[x][i] is None:
                    break
        # down right
        if x < col - 2 and y < row - 2 and self.board.matrix[x + 1][y + 1] == 1 - color:
            for i in range(2, min(col - x, row - y)):
                if self.board.matrix[x + i][y + i] == color:
                    for j in range(i):
                        self.board.matrix[x + j][y + j] = color
                if self.board.matrix[x + i][y + i] is None:
                    break
        # down left
        if x > 1 and y < row - 2 and self.board.matrix[x - 1][y + 1] == 1 - color:
            for i in range(2, min(x + 1, row - y)):
                if self.board.matrix[x - i][y + i] == color:
                    for j in range(i):
                        self.board.matrix[x - j][y + j] = color
                if self.board.matrix[x - i][y + i] is None:
                    break
        # up right
        if x < col - 2 and y > 1 and self.board.matrix[x + 1][y - 1] == 1 - color:
            for i in range(2, min(col - x, y + 1)):
                if self.board.matrix[x + i][y - i] == color:
                    for j in range(i):
                        self.board.matrix[x + j][y - j] = color
                if self.board.matrix[x + i][y - i] is None:
                    break
        # up left
        if x > 1 and y > 1 and self.board.matrix[x - 1][y - 1] == 1 - color:
            for i in range(2, min(x + 1, y + 1)):
                if self.board.matrix[x - i][y - i] == color:
                    for j in range(i):
                        self.board.matrix[x - j][y - j] = color
                if self.board.matrix[x - i][y - i] is None:
                    break
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
