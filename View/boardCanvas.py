from tkinter import *
from utils.config import *


class BoardCanvas(Canvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

    def repaint(self, model):
        self.create_rectangle(board_left_up_x, board_left_up_y, board_right_down_x,
                              board_right_down_y, fill=board_bg_color,
                              outline=board_outline_color)

        # Drawing the intermediate lines
        for i in range(row - 1):
            line_shift = board_left_up_x + board_box_width * (i + 1)

            # Horizontal line
            self.create_line(board_left_up_x, line_shift, board_right_down_x, line_shift, fill=line_color)

            # Vertical line
            self.create_line(line_shift, board_left_up_y, line_shift, board_right_down_y, fill=line_color)

        # draw circles
        for i in range(row):
            for j in range(col):
                if model.matrix[i][j] is not None:
                    self.circle(left_up_chess_x + board_box_width * i, left_up_chess_y + board_box_height * j,
                                chess_radius, model.matrix[i][j])

        for point in model.valid_matrix:
            self.circle(left_up_chess_x + board_box_width * point[0], left_up_chess_y + board_box_height * point[1],
                        prompt_radius, prompt_color)

        self.update()

    def circle(self, x, y, r, color):
        if color == black:
            color = 'black'
        elif color == white:
            color = 'white'
        else:
            pass
        self.create_oval(x - r, y - r, x + r, y + r, fill=color)
