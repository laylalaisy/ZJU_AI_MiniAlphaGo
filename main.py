# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from tkinter import *
from View.game import *
from Model.board import Board
from View.boardCanvas import BoardCanvas
from Controller.controller import Controller


def handlerAdaptor(fun, **kwds):
    '''''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def start_game(root, player):
    root.destroy()
    root = Tk()
    bo = Board()
    screen = BoardCanvas(root, width=500, height=600, background="#222", highlightthickness=0)
    controller = Controller(bo, screen)
    screen.delete(ALL)
    screen.bind("<Button-1>", handlerAdaptor(on_canvas_click, controller=controller))
    screen.pack()
    screen.repaint(bo)
    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    btn1 = Button(root, text='Player first', command=lambda: start_game(root, 0)).pack()
    btn2 = Button(root, text='AI first', command=lambda: start_game(root, 1)).pack()
    root.wm_title("Mini AlphaGo")
    root.mainloop()
