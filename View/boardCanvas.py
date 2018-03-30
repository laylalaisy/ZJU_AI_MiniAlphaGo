from tkinter import *


class BoardCanvas(Canvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        # let black be 0, white be 1
        # self.black=0
        # self.white=1
        self.black = 0
        self.white = 1

    def repaint(self, model):
        # print(model.matrix)
        # pass
        self.create_rectangle(50, 50, 450, 450, fill="#e3d94a", outline="#111")

        # Drawing the intermediate lines
        for i in range(7):
            line_shift = 50 + 50 * (i + 1)

            # Horizontal line
            self.create_line(50, line_shift, 450, line_shift, fill="#111")

            # Vertical line
            self.create_line(line_shift, 50, line_shift, 450, fill="#111")

            # draw circles
            self.circle(75, 75, 25, self.black)

        self.update()

    def circle(self, x, y, r, color):
        if color == self.black:
            color = 'black'
        else:
            color = 'white'
        id = self.create_oval(x - r, y - r, x + r, y + r)
        return id
