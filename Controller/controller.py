from state import State
from utils.valid import *
import globals
import random


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
        globals.state = State.AI

    def AI_play(self):
        valid_list = get_valid_list(self.board.matrix, globals.AI_color)
        (x, y) = random.sample(valid_list, 1)[0]
        self.board.matrix[x][y] = globals.AI_color
        self.eat(x, y)
        globals.state = State.player
        self.board.valid_matrix = get_valid_list(self.board.matrix, globals.player_color)
        self.notify()
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
