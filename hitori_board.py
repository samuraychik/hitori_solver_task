from hitori_cell import CellState, HitoriCell
import numpy as np
from collections import deque


class HitoriBoard:
    def __init__(self, side, numbers) -> None:
        if len(numbers) != side * side:
            raise Exception("Init HitoryBoard: Incorrect input")

        self.side = side
        
        cells = []

        i = 0
        for y in range(side):
            for x in range(side):
                if i < len(numbers):
                    cells.append(HitoriCell(x, y, numbers[i]))
                    i += 1

        self._board = np.array(cells).reshape(side, side)

    def get_row(self, number):
        return self._board[number]

    def get_col(self, number):
        return self._board[:, number]

    # Рекомендую использовать эту функцию вмето прямого обращения к клетке доски self._board[y, x]
    def get_cell(self, x, y):
        return self._board[y, x]
    
    def get_adjacent(self, x, y):
        dx = [-1, 1]
        dy = [-1, 1]
        adjacent = []
        for deltaX in dx:
            for deltaY in dy:
                if 0 < x + deltaX < self.side and 0 < y + deltaY < self.side:
                    adjacent.append(self.get_cell(x + deltaX, y + deltaY))
        return adjacent

    def get_col_repeats(self, x, y):
        col = self.get_col(x)
        origin_cell = self.get_cell(x, y)
        repeats = []
        for cell in col:
            if cell.value == origin_cell.value and cell.y != origin_cell.y:
                repeats.append(cell)
        return repeats

    def get_row_repeats(self, x, y):
        row = self.get_row(y)
        origin_cell = self.get_cell(x, y)
        repeats = []
        for cell in row:
            if cell.value == origin_cell.value and cell.x != origin_cell.x:
                repeats.append(cell)
        return repeats

    def get_repeats(self, x, y):
        col_repeats = self.get_col_repeats(x, y)
        row_repeats = self.get_row_repeats(x, y)
        return col_repeats + row_repeats

    def check_connectivity(self):
        start_cell = HitoriCell(0, 0, 0)
        for y in range(self.side):
            for x in range(self.side):
                if self.get_cell(x, y).state == CellState.WHITE:
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

        return len(visited) == len(self.get_cells_of_color(CellState.WHITE) + self.get_cells_of_color(CellState.GREY))

    def get_cells_of_color(self, color: CellState):
        cells = []
        for y in range(self.side):
            for x in range(self.side):
                if self.get_cell(x, y).state == color:
                    cells.append(self.get_cell(x, y))
        return cells

    # Перегрузки для более удобного вызова из других частей проекта
    def get_adjacent_from_cell(self, cell: HitoriCell):
        return self.get_adjacent(cell.x, cell.y)

    def get_repeats_from_cell(self, cell: HitoriCell):
        return self.get_repeats(cell.x, cell.y)
