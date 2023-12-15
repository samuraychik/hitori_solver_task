from hitori_board import *
from hitori_commands import SetBlack, SetWhite


class HitoriPatternsResolver:
    def __init__(self, board: HitoriBoard):
        self._board = board

    def resolve_repeats(self):  # Если две соседние ячейки имеют одинаковый номер баним повторюшки
        for y in range(self._board.size):
            for x in range(self._board.size):
                adjacent = self._board.get_adjacent_from_cell(self._board.get_cell(x, y))
                for neighbour in [cell for cell in adjacent if cell.x == x]:
                    if neighbour.value == self._board.get_cell(x, y).value:
                        col = self._board.get_col(neighbour.x)
                        for cell in col:
                            if not adjacent.__contains__(cell) and cell != self._board.get_cell(x, y) \
                                    and cell.value == neighbour.value:
                                SetBlack(cell, self._board).do()
                for neighbour in [cell for cell in adjacent if cell.y == y]:
                    if neighbour.value == self._board.get_cell(x, y).value:
                        row = self._board.get_row(neighbour.y)
                        for cell in row:
                            if not adjacent.__contains__(cell) and cell != self._board.get_cell(x, y) \
                                    and cell.value == neighbour.value:
                                SetBlack(cell, self._board).do()

    def resolve_triple_corners(self):
        corner_cells = [
            [self._board.get_cell(0, 0), self._board.get_cell(-1, 0), self._board.get_cell(0, -1), self._board.get_cell(-1, -1)],
            [self._board.get_cell(1, 1), self._board.get_cell(-2, 1), self._board.get_cell(1, -2), self._board.get_cell(-2, -2)]
        ]
        for i in range(4):
            adjacent = self._board.get_adjacent_from_cell(corner_cells[0][i])
            if adjacent[0].value == adjacent[1].value:
                if corner_cells[0][i].value == adjacent[0].value:
                    SetBlack(corner_cells[0][i], self._board).do()
                if corner_cells[1][i].value == adjacent[0].value:
                    SetBlack(corner_cells[1][i], self._board).do()

    def resolve_sandwiches(self):
        for y in range(self._board.size):  # не забыть обработать граничные случаи
            for x in range(self._board.size):
                cell = self._board.get_cell(x, y)
                adjacent = self._board.get_adjacent_from_cell(cell)
                if 0 < x < self._board.size - 1:
                    row_neighbours = [cell for cell in adjacent if cell.y == y]
                    if row_neighbours[0].value == row_neighbours[1].value:
                        SetWhite(cell, self._board).do()
                if 0 < y < self._board.size - 1:
                    col_neighbours = [cell for cell in adjacent if cell.x == x]
                    if col_neighbours[0].value == col_neighbours[1].value:
                        SetWhite(cell, self._board).do()
