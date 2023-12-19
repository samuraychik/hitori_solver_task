import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from hitori import hitori_board as hb


class HitoriBoardTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        del self.board

    def test_init_correctly(self):
        self.board = hb.HitoriBoard(3, 2, [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.board.width, 3)
        self.assertEqual(self.board.height, 2)
        self.assertEqual(self.board._board[1, 1].value, 5)

    def test_get_cell(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        self.assertEqual(self.board.get_cell(1, 1), self.board._board[1, 1])

    def test_get_col(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        expected = [self.board._board[0, 1], self.board._board[1, 1]]
        self.assertCountEqual(self.board.get_col(1).tolist(), expected)

    def test_get_row(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        expected = [self.board._board[1, 0], self.board._board[1, 1]]
        self.assertCountEqual(self.board.get_row(1).tolist(), expected)

    def test_get_cells_list(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        excepted = [self.board._board[0, 0], self.board._board[0, 1],
                    self.board._board[1, 0], self.board._board[1, 1]]
        self.assertCountEqual(self.board.get_cells_list(), excepted)

    def test_get_adjacent(self):
        self.board = hb.HitoriBoard(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        expected = [self.board._board[1, 0], self.board._board[0, 1], 
                    self.board._board[1, 2], self.board._board[2, 1]]
        self.assertCountEqual(self.board.get_adjacent(1, 1), expected)
        self.assertCountEqual(self.board.get_adjacent_from_cell(
            hb.HitoriCell(1, 1, 5)), expected)

    def test_get_repeats(self):
        self.board = hb.HitoriBoard(3, 3, [1, 2, 3, 1, 2, 1, 3, 2, 1])
        expected = [self.board._board[0, 0], self.board._board[1, 2]]
        self.assertCountEqual(self.board.get_repeats(0, 1), expected)
        self.assertCountEqual(self.board.get_repeats_from_cell(
            hb.HitoriCell(0, 1, 1)), expected)

    def test_get_cells_of_color(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        self.board._board[0, 0].state = hb.CellState.BLACK
        self.board._board[1, 1].state = hb.CellState.WHITE
        expected = [self.board._board[1, 0], self.board._board[0, 1]]
        self.assertCountEqual(
            self.board.get_cells_of_color(hb.CellState.GREY), expected)

    def test_check_connectivity_true(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        self.board._board[0, 0].state = hb.CellState.BLACK
        self.assertTrue(self.board.check_connectivity())

    def test_check_coonectivity_false(self):
        self.board = hb.HitoriBoard(2, 2, [1, 2, 3, 4])
        self.board._board[0, 0].state = hb.CellState.BLACK
        self.board._board[1, 1].state = hb.CellState.BLACK
        self.assertFalse(self.board.check_connectivity())


if __name__ == "__main__":
    unittest.main()
