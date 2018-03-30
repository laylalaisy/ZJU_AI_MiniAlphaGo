from tkinter import *


class BoardCanvas(Canvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

    def update(self, model):

        print(model.matrix)
        pass
