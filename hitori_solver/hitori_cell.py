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

    def color(self) -> str:
        return ["G", "W", "B"][self.state.value]

    def symbol(self) -> str:
        return ["?", ".", "#"][self.state.value]

    def __str__(self) -> str:
        return f"({self.x},{self.y} : {self.value}{self.color()})"

    def __repr__(self) -> str:
        return self.__str__()
