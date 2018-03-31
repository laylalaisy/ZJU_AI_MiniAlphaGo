class AI:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def play(matrix, valid_list):
        # TODO: 现在的方法是返回第一个能落子的地方
        return valid_list[0]
