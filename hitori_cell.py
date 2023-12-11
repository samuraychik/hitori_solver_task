from enum import Enum


class CellState(Enum):
    GREY = 0
    WHITE = 1
    BLACK = 2


class HitoriCell:
    def __init__(self, x, y, value) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.state = CellState.GREY
