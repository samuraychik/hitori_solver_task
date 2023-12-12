from hitori_board import *
from hitori_commands import SetBlack, SetWhite


class HitoriPatterns:
    def __init__(self, board: HitoriBoard):
        self._board = board

    def solve_repeats(self):  # Если две соседние ячейки имеют одинаковый номер баним повторюшки
        for y in range(self._board.height):
            for x in range(self._board.width):
                adjacent = self._board.get_adjacent_from_cell(self._board.get_cell(x, y))
                for neighbour in [cell for cell in adjacent if cell.y == y]:
                    if neighbour.value == self._board.get_cell(x, y).value:
                        col = self._board.get_col(neighbour.x)
                        for cell in col:
                            if cell != neighbour and cell != self._board.get_cell(x, y) and cell.value == neighbour.value:
                                SetBlack(cell, self._board).do()
                for neighbour in [cell for cell in adjacent if cell.x == x]:
                    if neighbour.value == self._board.get_cell(x, y).value:
                        row = self._board.get_row(neighbour.y)
                        for cell in row:
                            if cell != neighbour and cell != self._board.get_cell(x, y) and cell.value == neighbour.value:
                                SetBlack(cell, self._board).do()

    def solve_triple_corner(self):
        corner_cells = [
            [self._board.get_cell(0, 0), self._board.get_cell(-1, 0), self._board.get_cell(0, -1), self._board.get_cell(-1, -1)],
            [self._board.get_cell(1, 1), self._board.get_cell(-2, 1), self._board.get_cell(1, -2), self._board.get_cell(-2, -2)]
        ]
        for i in range(4):
            adjacent = self._board.get_adjacent_from_cell(corner_cells[0][i])
            if adjacent[0].value == adjacent[1].value:
                if corner_cells[0][i].value == adjacent[0].value:
                    SetBlack(corner_cells[0][i], self._board)
                if corner_cells[1][i].value == adjacent[0].value:
                    SetBlack(corner_cells[1][i], self._board)

    def solve_sandwich(self):
        for y in range(self._board.height):  # не забыть обработать граничные случаи
            for x in range(self._board.width):
                cell = self._board.get_cell(x, y)
                adjacent = self._board.get_adjacent_from_cell(cell)
                if 0 < x < self._board.width - 1:
                    row_neighbours = [cell for cell in adjacent if cell.x == x]
                    if row_neighbours[0].value == row_neighbours[1].value:
                        SetWhite(cell, self._board)
                        if cell.value == row_neighbours[0].value:
                            SetBlack(row_neighbours[0], self._board)
                            SetBlack(row_neighbours[1], self._board)
                if 0 < y < self._board.height - 1:
                    col_neighbours = [cell for cell in adjacent if cell.y == y]
                    if col_neighbours[0].value == col_neighbours[1].value:
                        SetWhite(cell, self._board)
                        if cell.value == col_neighbours[0].value:
                            SetBlack(col_neighbours[0], self._board)
                            SetBlack(col_neighbours[1], self._board)
