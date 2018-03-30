class Controller():
    def __init__(self, board, canvas):
        # super().__init__()
        self.board = board
        self.canvas = canvas
        pass

    def on_click(self, event):
        print(event)
        self.notify()
        pass

    def notify(self):
        self.canvas.repaint(self.board)
