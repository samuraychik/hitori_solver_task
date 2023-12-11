from vitvit_commands import Command, CommandManager
from hitori_board import HitoriBoard
from hitori_cell import HitoriCell, CellState
from hitori_commands import SetBlack, SetWhite


class NoSolutionError(Exception):
    pass


class HitoriSolver:
    def solve(self, board: HitoriBoard):
        pass
