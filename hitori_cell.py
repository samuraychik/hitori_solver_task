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

    def __str__(self) -> str:
        if self.state == CellState.BLACK:
            return "#"
        if self.state == CellState.WHITE:
            return "."
        if self.state == CellState.GREY:
            return "?"

    def __repr__(self) -> str:
        return self.__str__()
