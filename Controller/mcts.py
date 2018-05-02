from copy import deepcopy
from datetime import *
from multiprocessing.dummy import Pool as ThreadPool
from random import choice
from Controller.node import Node

from math import log, sqrt, fabs

from globals import roxanne_table
from utils.config import single_time_limit
from utils.util import dumb_score, move

from Valid import valid


class MCSearchTree:

    def __init__(self, board, player, **kwargs):
        self.player = player
        self.time_limit = timedelta(seconds=kwargs.get("time_limit", 10))
        self.max_moves = kwargs.get('max_moves', 60)
        self.Cp = kwargs.get('Cp', 1.414)
        self.root = Node(board, player, None, None)
        self.start_time = None
        self.definite_count = [0, 0]
        self.moves = 4
        self.priority_table = deepcopy(roxanne_table)

    def update(self, board, player, pre_move, force_add=False):
        """
        :param force_add:
        :param pre_move:
        :param player:
        :param board: GUI.Board
        :return:
        """
        already_has_same_child = False
        for child in self.root.children:
            if child.pre_move == pre_move:
                if not force_add:
                    self.root = child
                else:
                    self.root.children.remove(child)
                    child = Node(board, player, self.root, pre_move)
                    self.root.children.append(child)
                    self.root = child
                already_has_same_child = True
                break
        if not already_has_same_child:
            child = Node(board, player, self.root, pre_move)
            self.root.children.append(child)
            self.root = child
        self.root.valid_list = valid.get_valid_list(self.root.board.matrix, player)
        self.moves = 0
        for i in board.matrix:
            for j in i:
                if j is not None:
                    self.moves += 1

    def uct_search(self):
        """
        uct search.
        :return: a step [x, y]
        """
        self.start_time = datetime.utcnow()
        self.do_simulations(self.root)
        if len(self.root.children) == 0:
            return None
        max_win_percent, chosen_child = self.best_child(self.root, 0)
        print("Winning percentage", max_win_percent)
        return chosen_child.pre_move

    def tree_policy(self, v):
        """
        TREEPOLICY
        :param v: Node
        :return: Node
        """
        while not v.is_terminal():
            if v.is_fully_expanded():
                value, v = self.best_child(v, self.Cp)
            else:
                return self.expand(v)
        return v

    @staticmethod
    def expand(v):
        """
        expand node
        :param v: Node
        :return: expanded node:Node
        """
        chosen_move = choice(v.un_tried_list)
        v.add_child(chosen_move)
        return v.children[-1]

    @staticmethod
    def best_child(node, c):
        """
        return the best child.
        :param node: Node
        :param c: constant
        :return: [value:double, child:Node]
        """
        child_value = [1 - child.q / child.n + c * sqrt(log(node.n) / child.n) for child in node.children]

        value = max(child_value)
        idx = child_value.index(value)
        return value, node.children[idx]

    def default_policy(self, node):
        """
        randomly choose child until terminate
        :param node: Node
        :return: reward node.player
        """
        cur_player = node.player
        state = deepcopy(node.board)

        num_moves = 0
        while num_moves + self.moves < 64:
            if self.moves + num_moves < 56:
                valid_set = valid.get_priority_valid_moves(state.matrix, self.priority_table, cur_player)
                if len(valid_set) == 0:
                    num_moves += 1
                    cur_player = 1 - cur_player
                    continue
                (cx, cy) = choice(valid_set)
            else:
                valid_set = valid.get_valid_list(state.matrix, cur_player)
                if len(valid_set) == 0:
                    cur_player = 1 - cur_player  # toggle player
                    num_moves += 1
                    continue
                (cx, cy) = choice(valid_set)  # choose one randomly
            state = move(state, cx, cy, cur_player)  # update board
            cur_player = 1 - cur_player  # toggle player
            num_moves += 1
        return dumb_score(state.matrix, self.player) > 0

    def backup(self, node, reward):
        """
        back up.
        :param node: Node
        :param reward: reward:1 or 0
        :return:
        """
        while node is not None:
            node.n += 1
            if node.player == self.player:
                node.q += reward
            else:
                node.q += 1 - reward
            node = node.parent

    def do_simulations(self, node):
        """
        multiprocessing simulation.
        :param node: root node
        :return: count
        """
        count = 0
        self.time_limit = timedelta(seconds=min(single_time_limit, 62 - fabs(34 - self.moves) * 2))
        while datetime.utcnow() - self.start_time < self.time_limit:
            vl = self.tree_policy(node)
            delta = self.default_policy(vl)
            self.backup(vl, delta)
            count += 1
            if node.is_fully_expanded():
                break
        if len(node.children) == 0:
            return count
        # use multi-thread policy, refering github
        pool = ThreadPool(len(node.children))
        counts = pool.map(self.simulation, node.children)
        pool.close()
        pool.join()
        count += sum(counts)
        return count

    def simulation(self, node):
        """
        :param node: root node:Node
        :return: count:int. simulation times
        """
        count = 0
        while datetime.utcnow() - self.start_time < self.time_limit:
            vl = self.tree_policy(node)
            delta = self.default_policy(vl)
            self.backup(vl, delta)
            count += 1
        return count
