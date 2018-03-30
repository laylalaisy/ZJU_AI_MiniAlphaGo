class Board:
    def __init__(self):
        self.row = self.col = 8
        self.matrix = []
        for i in range(self.row):
            self.matrix.append([])
            for j in range(self.col):
                self.matrix[i].append(None)
        # let black be 0, white be 1
        # self.black=0
        # self.white=1
        self.black=0
        self.white=1
        self.matrix[3][3] = self.black
        self.matrix[4][4] = self.black
        self.matrix[3][4] = self.white
        self.matrix[4][3] = self.white
        # print(self.matrix)
