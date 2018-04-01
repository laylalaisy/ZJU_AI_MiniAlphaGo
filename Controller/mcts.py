from Controller.node import Node


# TODO: complete this class!
class MCSearchTree:
    root: Node

    def __init__(self, root):
        self.root = root
        self.depth = 0

    def uct_search(self):
        # 现在的方法是简单的取第一个能放子的地方
        return self.root.valid_list[0]
        pass

    def tree_policy(self):
        pass

    def expand(self):
        pass

    def best_child(self):
        pass

    def default_policy(self):
        pass

    def backup(self):
        pass
