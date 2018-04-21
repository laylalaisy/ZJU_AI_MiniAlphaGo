from tkinter import *

import globals
from View.game import *
from Model.board import Board
from View.boardCanvas import BoardCanvas
from Controller.controller import Controller
from state import State
from utils.config import *
from Valid import valid


def handler_adaptor(fun, **kwds):
    '''''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def start_game(root, player):
    root.destroy()
    root = Tk()
    screen = BoardCanvas(root, width=screen_width, height=screen_height, background="#856c23", highlightthickness=0)
    controller = Controller(root, screen, init_game)
    init_game(controller, player, screen)

    root.focus_set()
    root.mainloop()


def init_game(controller, player, screen):
    bo = Board()
    if player == 0:
        globals.file_name = 'player_first'
    else:
        globals.file_name = 'AI_first'
    controller.set_board(bo)
    if player is 0:
        globals.state = State.player
        bo.valid_matrix = valid.get_valid_list(bo.matrix, black)
        # bo.player_timer.start()
    else:
        globals.state = State.AI
        # globals.file_name = 'AI_first'
        print(globals.file_name)
        globals.player_color = white
        globals.AI_color = black
        bo.valid_matrix.clear()
        controller.AI_play()
    screen.delete(ALL)
    screen.create_arc(5, 5, 45, 45, fill="#000111", width="4", style="arc", outline="white", extent=300)
    screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")
    screen.bind("<Button-1>", handler_adaptor(on_canvas_click, controller=controller))
    screen.pack()
    screen.repaint(bo)
