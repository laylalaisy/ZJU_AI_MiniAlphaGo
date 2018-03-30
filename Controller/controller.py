from utils.config import *


class Controller:
    def __init__(self, board, canvas):
        # super().__init__()
        self.board = board
        self.canvas = canvas
        pass

    def on_click(self, event):
        # print(event)
        x, y = self.get_position(event)
        # modify self.board according to x and y
        self.notify()
        pass

    def notify(self):
        self.canvas.repaint(self.board)

    def get_position(self, event):
        """
        根据事件的坐标计算是哪一个方格被点击了

        """
        return (event.x - board_left_up_x) // board_box_width, (event.y - board_left_up_y) // board_box_height
