class Controller:
    def __init__(self, board, canvas):
        # super().__init__()
        self.board = board
        self.canvas = canvas
        pass

    def on_click(self, event):
        print(event)
        # modify self.board according to event.x and event.y
        self.notify()
        pass

    def notify(self):
        self.canvas.repaint(self.board)
