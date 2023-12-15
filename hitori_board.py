from hitori_cell import CellState, HitoriCell
import numpy as np
from collections import deque


class HitoriBoard:
    def __init__(self, size, numbers) -> None:
        if len(numbers) != size * size:
            raise Exception("Init HitoryBoard: Incorrect input")

        self.size = size
        
        cells = []

        i = 0
        for y in range(size):
            for x in range(size):
                if i < len(numbers):
                    cells.append(HitoriCell(x, y, numbers[i]))
                    i += 1

        self._board = np.array(cells).reshape(size, size)

    def get_row(self, number):
        return self._board[number]

    def get_col(self, number):
        return self._board[:, number]

    # Рекомендую использовать эту функцию вмето прямого обращения к клетке доски self._board[y, x]
    def get_cell(self, x, y) -> HitoriCell:
        return self._board[y, x]
    
    def get_adjacent(self, x, y) -> list:
        adjacent = []
        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                adjacent.append(self.get_cell(x + dx, y + dy))
        return adjacent

    def get_col_repeats(self, x, y) -> set:
        col = self.get_col(x)
        origin_cell = self.get_cell(x, y)
        repeats = set()
        for cell in col:
            if cell.value == origin_cell.value and cell.y != origin_cell.y:
                repeats.add(cell)
        return repeats

    def get_row_repeats(self, x, y) -> set:
        row = self.get_row(y)
        origin_cell = self.get_cell(x, y)
        repeats = set()
        for cell in row:
            if cell.value == origin_cell.value and cell.x != origin_cell.x:
                repeats.add(cell)
        return repeats

    def get_repeats(self, x, y) -> set:
        col_repeats = self.get_col_repeats(x, y)
        row_repeats = self.get_row_repeats(x, y)
        return col_repeats | row_repeats

    def check_connectivity(self) -> bool:
        start_cell = HitoriCell(0, 0, 0)
        for y in range(self.size):
            for x in range(self.size):
                if self.get_cell(x, y).state != CellState.BLACK:
                    start_cell = self.get_cell(x, y)
                    break
            break

        visited, queue = set(), deque([start_cell])
        visited.add(start_cell)
        while queue:
            cell = queue.popleft()
            for neighbour in self.get_adjacent_from_cell(cell):
                if neighbour not in visited and neighbour.state != CellState.BLACK:
                    visited.add(neighbour)
                    queue.append(neighbour)
        non_blacks = self.get_cells_of_color(CellState.WHITE) | self.get_cells_of_color(CellState.GREY)
        return len(visited) == len(non_blacks)

    def get_cells_of_color(self, color: CellState) -> set:
        cells = set()
        for y in range(self.size):
            for x in range(self.size):
                if self.get_cell(x, y).state == color:
                    cells.add(self.get_cell(x, y))
        return cells

    def get_all_grey_repeats(self) -> set:
        all_grey_repeats = set()
        grey_cells = self.get_cells_of_color(CellState.GREY)
        for cell in grey_cells:
            repeats = self.get_repeats_from_cell(cell)
            grey_repeats = {cell for cell in repeats if cell.state == CellState.GREY}
            all_grey_repeats.update(grey_repeats)
        return all_grey_repeats

    # Перегрузки для более удобного вызова из других частей проекта
    def get_adjacent_from_cell(self, cell: HitoriCell) -> list:
        return self.get_adjacent(cell.x, cell.y)

    def get_repeats_from_cell(self, cell: HitoriCell) -> set:
        return self.get_repeats(cell.x, cell.y)

    def __str__(self) -> str:
        output = ""
        for y in range(self.size):
            for x in range(self.size):
                cell = self.get_cell(x, y)
                output += f"{cell} "
            output += "\n"
        return output
