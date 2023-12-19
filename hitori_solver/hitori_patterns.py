from hitori_solver.hitori_board import *
from hitori_solver.hitori_commands import *


class HitoriPatternsResolver:
    def __init__(self, board: HitoriBoard):
        self.board = board

    def resolve_repeats(self):
        for cell in self.board.get_cells_list():
            adjacent = self.board.get_adjacent_from_cell(cell)

            for neighbour in [c for c in adjacent if c.x == cell.x]:
                if neighbour.value == cell.value:
                    col = self.board.get_col(neighbour.x)
                    for col_cell in col:
                        if col_cell not in adjacent and col_cell != cell \
                            and col_cell.value == neighbour.value:
                                SetBlack(col_cell, self.board).do()

            for neighbour in [c for c in adjacent if c.y == cell.y]:
                if neighbour.value == cell.value:
                    row = self.board.get_row(neighbour.y)
                    for row_cell in row:
                        if row_cell not in adjacent and row_cell != cell \
                            and row_cell.value == neighbour.value:
                                SetBlack(row_cell, self.board).do()

    def resolve_triple_corners(self):
        corner_cells = [
            [self.board.get_cell(0, 0), self.board.get_cell(-1, 0), 
             self.board.get_cell(0, -1), self.board.get_cell(-1, -1)],
            [self.board.get_cell(1, 1), self.board.get_cell(-2, 1), 
             self.board.get_cell(1, -2), self.board.get_cell(-2, -2)]
        ]
        for i in range(4):
            adjacent = self.board.get_adjacent_from_cell(corner_cells[0][i])
            if adjacent[0].value == adjacent[1].value:
                if corner_cells[0][i].value == adjacent[0].value:
                    SetBlack(corner_cells[0][i], self.board).do()
                if corner_cells[1][i].value == adjacent[0].value:
                    SetBlack(corner_cells[1][i], self.board).do()

    def resolve_sandwiches(self):
        for cell in self.board.get_cells_list():
            adjacent = self.board.get_adjacent_from_cell(cell)

            if 0 < cell.x < self.board.width - 1:
                row_neighbours = [c for c in adjacent if c.y == cell.y]
                if row_neighbours[0].value == row_neighbours[1].value:
                    SetWhite(cell, self.board).do()

            if 0 < cell.y < self.board.height - 1:
                col_neighbours = [c for c in adjacent if c.x == cell.x]
                if col_neighbours[0].value == col_neighbours[1].value:
                    SetWhite(cell, self.board).do()
