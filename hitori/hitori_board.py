import numpy as np
from collections import deque

from hitori.hitori_cell import CellState, HitoriCell


class HitoriBoard:
    def __init__(self, width, height, numbers) -> None:
        if len(numbers) != width * height:
            raise ValueError()

        self.width = width
        self.height = height

        cells = []

        i = 0
        for y in range(height):
            for x in range(width):
                if i < len(numbers):
                    cells.append(HitoriCell(x, y, numbers[i]))
                    i += 1

        self._board = np.array(cells).reshape(height, width)

    def get_row(self, number):
        return self._board[number]

    def get_col(self, number):
        return self._board[:, number]

    def get_cell(self, x, y) -> HitoriCell:
        return self._board[y, x]

    def get_cells_list(self) -> list:
        cells = list()
        for y in range(self.height):
            for x in range(self.width):
                cells.append(self.get_cell(x, y))
        return cells

    def get_cells_of_color(self, color: CellState) -> list:
        colored_cells = list()
        for cell in self.get_cells_list():
            if cell.state == color:
                colored_cells.append(cell)
        return colored_cells

    def get_adjacent(self, x, y) -> list:
        adjacent = []
        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                adjacent.append(self.get_cell(x + dx, y + dy))
        return adjacent

    def get_adjacent_from_cell(self, cell: HitoriCell) -> list:
        return self.get_adjacent(cell.x, cell.y)

    def get_col_repeats(self, x, y) -> list:
        col = self.get_col(x)
        origin_cell = self.get_cell(x, y)
        repeats = list()
        for cell in col:
            if cell.value == origin_cell.value and cell.y != origin_cell.y:
                repeats.append(cell)
        return repeats

    def get_row_repeats(self, x, y) -> list:
        row = self.get_row(y)
        origin_cell = self.get_cell(x, y)
        repeats = list()
        for cell in row:
            if cell.value == origin_cell.value and cell.x != origin_cell.x:
                repeats.append(cell)
        return repeats

    def get_repeats(self, x, y) -> list:
        col_repeats = self.get_col_repeats(x, y)
        row_repeats = self.get_row_repeats(x, y)
        return col_repeats + row_repeats

    def get_repeats_from_cell(self, cell: HitoriCell) -> list:
        return self.get_repeats(cell.x, cell.y)

    def check_connectivity(self) -> bool:
        start_cell = HitoriCell(0, 0, 0)
        for cell in self.get_cells_list():
            if cell.state != CellState.BLACK:
                start_cell = cell
                break

        visited, queue = set(), deque([start_cell])
        visited.add(start_cell)
        while queue:
            cell = queue.popleft()
            for adj in self.get_adjacent_from_cell(cell):
                if adj not in visited and adj.state != CellState.BLACK:
                    visited.add(adj)
                    queue.append(adj)

        non_blacks = []
        non_blacks += self.get_cells_of_color(CellState.WHITE)
        non_blacks += self.get_cells_of_color(CellState.GREY)
        return len(visited) == len(non_blacks)

    def get_all_grey_repeats(self) -> set:
        all_grey_repeats = set()
        grey_cells = self.get_cells_of_color(CellState.GREY)
        for cell in grey_cells:
            repeats = self.get_repeats_from_cell(cell)
            grey_repeats = {c for c in repeats if c.state == CellState.GREY}
            all_grey_repeats.update(grey_repeats)
        return all_grey_repeats

    def to_string_with_numbers(self) -> str:
        output = ""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.state == CellState.BLACK:
                    output += "  "
                else:
                    output += str(cell.value).rjust(2)
                output += " "
            output += "\n"
        return output

    def to_string_with_symbols(self) -> str:
        output = ""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                output += cell.symbol() + " "
            output += "\n"
        return output

    def __str__(self) -> str:
        return self.to_string_with_numbers()
