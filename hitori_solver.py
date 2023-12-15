from vitvit_commands import Command, CommandManager
from hitori_board import HitoriBoard
from hitori_cell import HitoriCell, CellState
from hitori_commands import SetBlack, SetWhite, HitoriWrongSolutionError
from hitori_patterns import HitoriPatternsResolver


class HitoriNoSolutionError(Exception):
    pass


class HitoriImpossiblePatternError(Exception):
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

        if self.is_solved(board):
            self.wrap_solution(board)
            return

        self.resolve_non_repeats(board)

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

    def resolve_non_repeats(self, board: HitoriBoard):
        grey_repeats = board.get_all_grey_repeats()
        grey_cells = board.get_cells_of_color(CellState.GREY)
        grey_non_repeats = grey_cells.difference(grey_repeats)
        for cell in grey_non_repeats:
            SetWhite(cell, board).do()

    def iterate_remaining(self, board: HitoriBoard, manager: CommandManager):
        grey_cells = board.get_cells_of_color(CellState.GREY)
        for grey_cell in grey_cells:
            try:
                manager.do(SetBlack(grey_cell, board))
            except HitoriWrongSolutionError:
                manager.undo()
            else:
                if self.is_solved(board):
                    raise HitoriSolutionFoundError

    def is_solved(self, board: HitoriBoard) -> bool:
        return len(board.get_all_grey_repeats()) == 0

    def wrap_solution(self, board: HitoriBoard):
        for cell in board.get_cells_of_color(CellState.GREY):
            cell.state = CellState.WHITE
