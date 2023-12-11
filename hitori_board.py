from hitori_cell import CellState, HitoriCell
import numpy as np


class HitoriBoard:
    def __init__(self, width, height, numbers) -> None:
        if len(numbers) != width * height:
            raise

        self._cells = []
        self.width = width
        self.height = height

        i = 0
        for y in range(height):
            for x in range(width):
                if i < len(numbers):
                    self.cells.append(HitoriCell(x, y, numbers[i]))
                    i += 1

        self._board = np.array(self.cells).reshape(height, width)

    def get_row(self, number):
        return self._board[number]

    def get_col(self, number):
        return np.transpose(self._board)[number]
    
    def get_adjacent(self, x, y):
        dx = [-1, 1]
        dy = [-1, 1]
        adjacent = []
        for deltaX in dx:
            for deltaY in dy:
                if 0 < x + deltaX < self.width and 0 < y + deltaY < self.height:
                    adjacent.append(self._board[x + deltaX, y + deltaY])
        return adjacent

    def get_repeats(self, x, y):
        pass

    def сheck_сonnectivity(self):
        pass

    # Перегрузки для более удобного вызова из других частей проекта
    def get_adjacent_from_cell(self, cell: HitoriCell):
        return self.get_adjacent(cell.x, cell.y)

    def get_repeats_from_cell(self, cell: HitoriCell):
        return self.get_repeats(cell.x, cell.y)
