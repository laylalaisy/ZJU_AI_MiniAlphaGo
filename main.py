from tkinter import *
from game import start_game

if __name__ == "__main__":
    root = Tk()
    btn1 = Button(root, text='Player first', command=lambda: start_game(root, 0)).pack()
    btn2 = Button(root, text='AI first', command=lambda: start_game(root, 1)).pack()
    root.wm_title("Mini AlphaGo")
    root.mainloop()
