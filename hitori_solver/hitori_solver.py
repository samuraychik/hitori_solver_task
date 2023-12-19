import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from commands.vitvit_commands import *
from hitori_solver.hitori_board import *
from hitori_solver.hitori_cell import *
from hitori_solver.hitori_commands import *
from hitori_solver.hitori_patterns import *


class HitoriNoSolutionError(Exception):
    pass


class HitoriImpossiblePatternError(Exception):
    pass


class HitoriImpossibleCellError(Exception):
    pass


class HitoriNoNonRepeatsError(Exception):
    pass


class HitoriNoSurfaceCellsError(Exception):
    pass


class HitoriSolutionFoundError(Exception):
    pass


class HitoriSolver:     
    def solve(self, board: HitoriBoard):       
        if self.is_solved(board):
            self.wrap_solution(board)
            return

        try:
            self.resolve_patterns(board)
        except HitoriImpossiblePatternError:
            raise HitoriNoSolutionError()

        try:
            self.resolve_forced_cells(board)
        except HitoriImpossibleCellError:
            raise HitoriNoSolutionError
        except HitoriSolutionFoundError:
            self.wrap_solution(board)
            return

        try:
            self.iterate_remaining(board, CommandManager())
        except HitoriSolutionFoundError:
            self.wrap_solution(board)
        else:
            raise HitoriNoSolutionError()

    def resolve_patterns(self, board: HitoriBoard):
        try:
            patterns_resolver = HitoriPatternsResolver(board)
            patterns_resolver.resolve_repeats()
            patterns_resolver.resolve_triple_corners()
            patterns_resolver.resolve_sandwiches()
        except HitoriWrongSolutionError:
            raise HitoriImpossiblePatternError()

    def resolve_forced_cells(self, board: HitoriBoard):
        manager = CommandManager()
        has_non_repeats = True
        has_surface_cells = True

        while has_non_repeats or has_surface_cells:
            try:
                self.resolve_non_repeats(board, manager)
            except HitoriNoNonRepeatsError:
                has_non_repeats = False
            else:
                has_non_repeats = True
                has_surface_cells = True

            try:
                self.resolve_surface_cells(board, manager)
            except HitoriNoSurfaceCellsError:
                has_surface_cells = False
            else:
                has_non_repeats = True
                has_surface_cells = True

            if self.is_solved(board):
                raise HitoriSolutionFoundError()

    def resolve_non_repeats(self, board: HitoriBoard, 
                            manager: CommandManager):
        grey_repeats = board.get_all_grey_repeats()
        grey_cells = board.get_cells_of_color(CellState.GREY)
        grey_non_repeats = set(grey_cells).difference(grey_repeats)

        if len(grey_non_repeats) == 0:
            raise HitoriNoNonRepeatsError()
        for cell in grey_non_repeats:
            manager.do(SetWhite(cell, board))

    def resolve_surface_cells(self, board: HitoriBoard, 
                              manager: CommandManager):
        found_surface_cells = False
        for cell in board.get_cells_list():
            if cell.state != CellState.GREY:
                continue

            try:
                manager.do(SetBlack(cell, board))
            except HitoriWrongSolutionError:
                can_be_black = False
            else:
                can_be_black = True
            manager.undo()

            try:
                manager.do(SetWhite(cell, board))
            except HitoriWrongSolutionError:
                can_be_white = False
            else:
                can_be_white = True
            manager.undo()

            if can_be_black and not can_be_white:
                manager.do(SetBlack(cell, board))
                found_surface_cells = True
            elif not can_be_black and can_be_white:
                manager.do(SetWhite(cell, board))
                found_surface_cells = True
            elif not can_be_black and not can_be_white:
                raise HitoriImpossibleCellError()

        if not found_surface_cells:
            raise HitoriNoSurfaceCellsError()

    def iterate_remaining(self, board: HitoriBoard, 
                          manager: CommandManager):
        for cell in board.get_cells_list():
            if cell.state != CellState.GREY:
                continue

            can_be_black = True
            try:
                manager.do(SetBlack(cell, board))
            except HitoriWrongSolutionError:
                can_be_black = False
            else:
                try:
                    self.resolve_forced_cells(board)
                except HitoriImpossibleCellError:
                    can_be_black = False
                else:
                    if self.is_solved(board):
                        raise HitoriSolutionFoundError
                    self.iterate_remaining(board, manager)
            manager.undo()

            can_be_white = True
            try:
                manager.do(SetWhite(cell, board))
            except HitoriWrongSolutionError:
                can_be_white = False
            else:
                try:
                    self.resolve_forced_cells(board)
                except HitoriImpossibleCellError:
                    can_be_white = False
                else:
                    if self.is_solved(board):
                        raise HitoriSolutionFoundError
                    self.iterate_remaining(board, manager)
            manager.undo()

            if not can_be_black and not can_be_white:
                return

    def is_solved(self, board: HitoriBoard) -> bool:
        return len(board.get_all_grey_repeats()) == 0

    def wrap_solution(self, board: HitoriBoard):
        for cell in board.get_cells_of_color(CellState.GREY):
            cell.state = CellState.WHITE
