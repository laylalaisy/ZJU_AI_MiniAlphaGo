import tkinter.messagebox
import pickle
import globals
from Controller import mcts
from state import State
from utils.config import board_left_up_x, board_box_width, board_box_height, board_left_up_y, row, col, black
from utils.util import move
from Valid import valid


class Controller:
    def __init__(self, root, canvas, init_game):
        # super().__init__()
        self.root = root
        # self.board = board
        self.canvas = canvas
        self.init_game = init_game
        # self.state = state

        pass

    def set_board(self, board):
        self.board = board
        # if globals.player_color == black:
        #     self.tree = mcts.MCSearchTree(self.board, globals.player_color)
        # else:
        #     pass
        self.tree = self.get_tree()
        # print(self.tree.root.q, self.tree.root.n)
        # self.tree = mcts.MCSearchTree(self.board, globals.player_color)

    def on_click(self, event):
        # print(self.state)
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

    def get_position(self, event):
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
        # globals.state = State.AI
        self.switch_player((x, y))

    def AI_play(self):
        # print(globals.file_name)
        if globals.state != State.AI:
            return
        # self.board.AI_timer.start()
        valid_list = valid.get_valid_list(self.board.matrix, globals.AI_color)
        (x, y) = (None, None)
        if len(valid_list) != 0:
            (x, y) = self.tree.uct_search()
            # self.write(globals.file_name, self.tree)
            move(self.board, x, y, globals.AI_color)
        else:
            print("valid_list is empty! AI pass")
            if not self.board.has_empty_box():
                self.finish_game()
        # globals.state = State.player
        self.board.valid_matrix = valid.get_valid_list(self.board.matrix, globals.player_color)
        self.notify()
        if len(self.board.valid_matrix) == 0:
            print("player pass!")
            self.tree.update(self.board, globals.AI_color, (x, y))
            self.AI_play()
        else:
            # globals.state = State.player
            self.switch_player((x, y))
            # self.board.player_timer.start()
        pass

    def switch_player(self, pre_move):
        player = None
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
        self.write(globals.file_name, self.tree)
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
            # print(globals.file_name)
            tree = self.read(globals.file_name)
            while tree.root.parent is not None:
                tree.root = tree.root.parent
        except FileNotFoundError:
            self.write(globals.file_name)
            tree = self.read(globals.file_name)
        return tree

    def read(self, filename):
        # print('in read, filename = ',filename)
        with open(filename, 'rb') as f:
            aa = pickle.load(f)
            # print(type(aa))
            return aa

    def write(self, filename, t=None):
        # print('in write, filename = ',filename)
        with open(filename, 'wb') as f:
            if t is None:
                t = mcts.MCSearchTree(self.board, black)
            pickle.dump(t, f)
