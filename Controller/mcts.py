from copy import deepcopy
from datetime import *
from multiprocessing.dummy import Pool as ThreadPool
from random import choice
from Controller.node import Node
import globals

from math import log, sqrt, fabs

from globals import roxanne_table, AI_color
from utils.util import dumb_score, move

from Valid import valid


# from utils import valid


# TODO: complete this class!
class MCSearchTree:

    def __init__(self, board, player, **kwargs):
        # self.root = root
        self.depth = 0
        self.player = player
        # self.time_limit = timedelta(seconds=kwargs.get("time_limit", 5))
        self.time_limit = timedelta(seconds=kwargs.get("time_limit", 10))
        self.max_moves = kwargs.get('max_moves', 60)
        # self.max_depth = 0
        self.Cp = kwargs.get('Cp', 1.414)
        self.root = Node(board, player, None, None)
        self.default_time = timedelta(seconds=0)
        self.start_time = None
        self.definite_count = [0, 0]
        self.moves = 4  # 这个棋盘上已经有了多少个子
        self.priority_table = deepcopy(roxanne_table)

    def update(self, board, player, pre_move, force_add=False):
        """
        append board to history
        :param force_add:
        :param pre_move:
        :param player:
        :param board: GUI.Board
        :return:
        """
        # self.root = Node(board, player, self.root, pre_move)
        already_has_same_child = False
        for child in self.root.children:
            if child.pre_move == pre_move:
                print('already has same child!')
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
        self.depth = 0  # ???
        self.default_time = timedelta(seconds=0)  # ???
        self.moves = 0
        for i in board.matrix:
            for j in i:
                if j is not None:
                    self.moves += 1

    def uct_search(self):
        """!!!
        uct search.
        :return: a exec_move [x, y] maximizing winning percentage
        """
        # tree depth
        self.depth = 0
        # count of simulation
        self.start_time = datetime.utcnow()
        count = self.mul_simulation(self.root)
        print("Num of Simulations: {} \nTime played:{}\nDefault Policy Played:{}\n".
              format(count, datetime.utcnow() - self.start_time, self.default_time))
        if len(self.root.children) == 0:
            return None
        max_win_percent, chosen_child = self.best_child(self.root, 0)
        print("Maximum depth searched: {} \nMax percent of winning:{}".format(self.depth, max_win_percent))
        # print("Size of table: {}".format(len(valid_table)))
        print("{}/{}".format(self.root.q, self.root.n))
        for child in self.root.children:
            print("{}/{}".format(child.q, child.n))

        print('self.moves', self.moves)
        return chosen_child.pre_move

    def tree_policy(self, node):
        # print('tree_policy')
        """ 返回一个用来default policy的结点
                TREEPOLICY
                :param node: Node
                :return: Node
                """
        # print('isterminal:' + str(node.is_terminal()))
        while not node.is_terminal():
            # print(node.is_fully_expanded())
            if node.is_fully_expanded():
                # 如果都尝试过了，那就根据UCT选一个最好的儿子结点
                value, node = self.best_child(node, self.Cp)
            else:
                # 如果有未尝试过的放子位置
                return self.expand(node)
        return node

    def expand(self, node):
        # print('expand')
        """
        expand node
        :param node: Node
        :return: expanded node:Node
        """
        chosen_move = choice(node.un_tried_list)  # 从还没有尝试过的落子方式中随机选一个
        # chosen_move (x,y)
        node.add_child(chosen_move)
        # 更新一下这棵树的最大深度
        if node.children[-1].depth > self.depth:
            self.depth = node.children[-1].depth
        # 返回刚刚挂上去的Node
        return node.children[-1]

    def best_child(self, node, c):
        # print('best_child')
        """
        return the best child.
        :param node: Node
        :param c: constant
        :return: [value:double, child:Node]
        """
        # 为啥是1-Q/N...??
        child_value = [1 - child.q / child.n + c * sqrt(log(node.n) / child.n) for child in node.children]

        value = max(child_value)
        idx = child_value.index(value)
        return value, node.children[idx]

    def default_policy(self, node):
        # print('default_policy')
        """
        randomly choose child until terminate
        :param node: Node
        :return: reward node.player在模拟之后是否比对方棋子多
        """
        # global k, m
        # num_of_win = 0
        # for i in range(k):
        cur_player = node.player  # 当前是谁在落子？
        state = deepcopy(node.board)

        num_moves = 0
        while num_moves + self.moves < 64:  # ???
            if self.moves + num_moves < 56:  # ???
                valid_set = valid.get_priority_valid_moves(state.matrix, self.priority_table, cur_player)
                if len(valid_set) == 0:
                    num_moves += 1
                    cur_player = 1 - cur_player
                    continue
                (cx, cy) = choice(valid_set)
            else:
                valid_set = valid.get_valid_list(state.matrix, cur_player)
                if len(valid_set) == 0:  # 如果当前玩家不可能落子
                    cur_player = 1 - cur_player  # 反转落子权
                    num_moves += 1  # ???
                    continue
                (cx, cy) = choice(valid_set)  # 随便选一个
            state = move(state, cx, cy, cur_player)  # 棋盘更新一下
            cur_player = 1 - cur_player  # 玩家反转
            num_moves += 1
            # num_of_win += dumb_score(state, self.board.player) > 0
        # 走64步，看看64步之后谁的棋子更多？
        # print(globals.AI_color)
        return dumb_score(state.matrix, self.player) > 0

    def backup(self, node, reward):
        # print('backup')
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

    def mul_simulation(self, node):
        # print('mul_simulation')
        """
        multiprocessing simulation.
        :param node: root node
        :return: count
        """
        count = 0
        self.time_limit = timedelta(seconds=62 - fabs(34 - self.moves) * 2)
        # self.time_limit = timedelta(seconds=3)
        while datetime.utcnow() - self.start_time < self.time_limit:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.backup(v, reward)
            count += 1
            if node.is_fully_expanded():
                break
        if len(node.children) == 0:
            return count
        pool = ThreadPool(len(node.children))
        counts = pool.map(self.simulation, node.children)
        pool.close()
        pool.join()
        count += sum(counts)
        return count

    def simulation(self, node):
        # print('simulation')
        """
        :param node: root node:Node
        :return: count:int 模拟了多少次
        """
        count = 0
        while datetime.utcnow() - self.start_time < self.time_limit:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.backup(v, reward)
            count += 1
        return count
