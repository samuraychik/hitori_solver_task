from random import randint

from commands.vitvit_commands import CommandManager
from hitori.hitori_board import HitoriBoard
from hitori.hitori_cell import CellState
from hitori.hitori_commands import SetBlack, SetWhite, HitoriWrongCommandError


class HitoriNumberGenerationFailedError(Exception):
    pass


class HitoriRetryGenerationError(Exception):
    pass


class HitoriGenerator:
    def generate(self, width: int, height: int, 
                 diagonal_rule_enabled=False) -> HitoriBoard:
        numbers = [i for i in range(width * height)]
        board = HitoriBoard(width, height, numbers,
                                 diagonal_rule_enabled)

        self.color_board_cells(board)

        try:
            self.fill_white_with_numbers(board)
        except HitoriNumberGenerationFailedError:
            raise HitoriRetryGenerationError()

        if diagonal_rule_enabled:
            try:
                self.fill_black_with_numbers_with_rule(board)
            except HitoriNumberGenerationFailedError:
                raise HitoriRetryGenerationError()

        else:
            self.fill_black_with_numbers(board)

        self.grey_out(board)
        return board

    def color_board_cells(self, board: HitoriBoard) -> None:
        manager = CommandManager()
        for cell in board.get_cells_list():
            if cell.state != CellState.GREY:
                continue

            try_black = randint(1, 100) <= 75
            if try_black:
                try:
                    manager.do(SetBlack(cell, board))
                except HitoriWrongCommandError:
                    manager.undo()
                    manager.do(SetWhite(cell, board))
            else:
                manager.do(SetWhite(cell, board))

    def fill_white_with_numbers(self, board: HitoriBoard) -> None:
        optimized_cardinals = self.get_optimized_white_cardinals(board)

        for tuple in optimized_cardinals:
            cell = tuple[0]
            cell_cardinals = tuple[1]
            if len(cell.value) == 0:
                raise HitoriNumberGenerationFailedError()

            cell.value = cell.value[randint(0, len(cell.value) - 1)]
            for cardinal in cell_cardinals:
                if type(cardinal.value) == int:
                    continue
                if cell.value in cardinal.value:
                    cardinal.value.remove(cell.value)

    def fill_black_with_numbers(self, board: HitoriBoard) -> None:
        for cell in board.get_cells_of_color(CellState.BLACK):
            use_row = randint(1, 100) <= 50
            if use_row:
                whites = [c for c 
                          in board.get_row(cell.y) 
                          if c.state == CellState.WHITE]
            else:
                whites = [c for c
                          in board.get_col(cell.x)
                          if c.state == CellState.WHITE]
            cell.value = whites[randint(0, len(whites) - 1)].value

    def fill_black_with_numbers_with_rule(self, board: HitoriBoard) -> None:
        optimized_diagonals = self.get_optimized_black_diagonals(board)

        for tuple in optimized_diagonals:
            cell = tuple[0]
            cell_diagonals = tuple[1]
            if len(cell.value) == 0:
                raise HitoriNumberGenerationFailedError()

            cell.value = cell.value[randint(0, len(cell.value) - 1)]
            for diagonal in cell_diagonals:
                if type(diagonal.value) == int:
                    continue
                if cell.value in diagonal.value:
                    diagonal.value.remove(cell.value)

    def get_optimized_white_cardinals(self, board: HitoriBoard) -> list():
        white_cardinals = dict()
        for cell in board.get_cells_of_color(CellState.WHITE):
            cell.value = [i + 1 for i
                          in range(max(board.width, board.height))]

            white_cardinals[cell] = [c for c
                                     in board.get_cardinals_from_cell(cell)
                                     if c.state == CellState.WHITE]

        return sorted(white_cardinals.items(),
                      key=lambda t:len(t[1]), reverse=True)

    def get_optimized_black_diagonals(self, board: HitoriBoard) -> list():
        black_diagonals = dict()
        for cell in board.get_cells_of_color(CellState.BLACK):
            white_cardinals = [c for c
                               in board.get_cardinals_from_cell(cell)
                               if c.state == CellState.WHITE]
            values = set()
            for cardinal in white_cardinals:
                values.add(cardinal.value)
            cell.value = list(values)

            black_diagonals[cell] = [c for c
                                     in board.get_diagonals_from_cell(cell)
                                     if c.state == CellState.BLACK]

        return sorted(black_diagonals.items(),
                      key=lambda t:len(t[1]), reverse=True)

    def grey_out(self, board: HitoriBoard) -> None:
        for cell in board.get_cells_list():
            cell.state = CellState.GREY
