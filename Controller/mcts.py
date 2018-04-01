from Controller.node import Node


class MCSearchTree:
    root: Node

    def __init__(self, root):
        self.root = root
        self.depth = 0

    def uct_search(self):
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
