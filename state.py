from enum import Enum


class State(Enum):
    stopping = 1
    player = 2
    AI = 3
    finished = 4
