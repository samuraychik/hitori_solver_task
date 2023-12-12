from hitori_cell import CellState, HitoriCell
import numpy as np
from collections import deque


class HitoriBoard:
    def __init__(self, width, height, numbers) -> None:
        if len(numbers) != width * height:
            raise

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
        return np.transpose(self._board)[number]

    def get_cell(self, x, y):
        return self._board[x, y]
    
    def get_adjacent(self, x, y):
        dx = [-1, 1]
        dy = [-1, 1]
        adjacent = []
        for deltaX in dx:
            for deltaY in dy:
                if 0 < x + deltaX < self.width and 0 < y + deltaY < self.height:
                    adjacent.append(self._board[x + deltaX, y + deltaY])
        return adjacent

    def get_col_repeats(self, x, y):
        col = self.get_col(x)
        origin_cell = self._board[y][x]
        repeats = []
        for cell in col:
            if cell.value == origin_cell.value and cell.y != origin_cell.y:
                repeats.append(cell)
        return repeats

    def get_row_repeats(self, x, y):
        row = self.get_row(y)
        origin_cell = self._board[y][x]
        repeats = []
        for cell in row:
            if cell.value == origin_cell.value and cell.x != origin_cell.x:
                repeats.append(cell)
        return repeats

    def get_repeats(self, x, y):
        col_repeats = self.get_col_repeats(x, y)
        row_repeats = self.get_row_repeats(x, y)
        return col_repeats + row_repeats

    def сheck_сonnectivity(self):
        for y in range(self.height):
            for x in range(self.width):
                if self._board[x][y].state == CellState.WHITE:
                    start_cell = self._board[x][y]
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

        return len(visited) == len(self.get_white_cells())

    def get_white_cells(self):  # Тут и белые, и псевдобелые
        white_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self._board[x][y].state != CellState.BLACK:
                    white_cells.append(self._board[x][y])
        return white_cells

    # Перегрузки для более удобного вызова из других частей проекта
    def get_adjacent_from_cell(self, cell: HitoriCell):
        return self.get_adjacent(cell.x, cell.y)

    def get_repeats_from_cell(self, cell: HitoriCell):
        return self.get_repeats(cell.x, cell.y)
