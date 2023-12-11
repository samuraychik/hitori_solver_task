from enum import Enum
from hitori_commands import Command, CommandManager


class SetBlack(Command):
    def __init__(self) -> None:
        super().__init__()


class CellState(Enum):
    UNKNOWN = 0
    WHITE = 1
    BLACK = 2


class HitoriCell:
    def __init__(self, x, y, value) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.state = CellState.UNKNOWN


class HitoriBoard:
    def __init__(self, width, height, numbers) -> None:
        pass
