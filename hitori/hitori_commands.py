import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from commands.vitvit_commands import Command, CommandManager
from hitori.hitori_board import HitoriBoard
from hitori.hitori_cell import HitoriCell, CellState


class HitoriWrongCommandError(Exception):
    pass


class SetWhite(Command):
    def __init__(self, cell: HitoriCell, board: HitoriBoard):
        self.cell = cell
        self.board = board
        self.manager = CommandManager()

    def do(self):
        if self.cell.state == CellState.WHITE:
            return
        if self.cell.state == CellState.BLACK:
            raise HitoriWrongCommandError()

        self.cell.state = CellState.WHITE

        repeats = self.board.get_repeats_from_cell(self.cell)
        for repeat in repeats:
            if repeat.state != CellState.BLACK:
                self.manager.do(SetBlack(repeat, self.board))

    def undo(self):
        self.cell.state = CellState.GREY
        while len(self.manager.history) > 0:
            self.manager.undo()


class SetBlack(Command):
    def __init__(self, cell: HitoriCell, board: HitoriBoard):
        self.cell = cell
        self.board = board
        self.manager = CommandManager()

    def do(self):
        if self.cell.state == CellState.BLACK:
            return
        if self.cell.state == CellState.WHITE:
            raise HitoriWrongCommandError()

        self.cell.state = CellState.BLACK

        if not self.board.check_connectivity():
            raise HitoriWrongCommandError()

        adjacents = self.board.get_adjacent_from_cell(self.cell)
        for adjacent in adjacents:
            if adjacent.state != CellState.WHITE:
                self.manager.do(SetWhite(adjacent, self.board))

        if self.board.diagonal_rule_enabled:
            repeats = self.board.get_diagonal_repeats_from_cell(self.cell)
            for repeat in repeats:
                if repeat.state != CellState.WHITE:
                    self.manager.do(SetWhite(repeat, self.board))

    def undo(self):
        self.cell.state = CellState.GREY
        while len(self.manager.history) > 0:
            self.manager.undo()
