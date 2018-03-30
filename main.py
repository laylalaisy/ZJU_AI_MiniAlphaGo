# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from tkinter import *
from View.game import *
from Model.board import Board
from View.boardCanvas import BoardCanvas
from Controller.controller import Controller
from utils.config import *
from utils.valid import *


def handler_adaptor(fun, **kwds):
    '''''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def start_game(root, player):
    root.destroy()
    root = Tk()
    bo = Board()
    global state
    if player is 0:
        state = State.player
        get_valid_list(bo.matrix, bo.valid_matrix, white)
    else:
        state = State.AI
        bo.valid_matrix.clear()
    screen = BoardCanvas(root, width=screen_width, height=screen_height, background="#856c23", highlightthickness=0)
    controller = Controller(bo, screen)
    screen.delete(ALL)
    screen.bind("<Button-1>", handler_adaptor(on_canvas_click, controller=controller))
    screen.pack()
    screen.repaint(bo)


    print(state)
    root.focus_set()
    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    btn1 = Button(root, text='Player first', command=lambda: start_game(root, 0)).pack()
    btn2 = Button(root, text='AI first', command=lambda: start_game(root, 1)).pack()
    root.wm_title("Mini AlphaGo")
    root.mainloop()
