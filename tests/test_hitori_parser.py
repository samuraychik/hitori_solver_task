import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from hitori import hitori_parser as hp
from hitori import hitori_board as hb


class HitoriParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = hp.HitoriParser()

    def tearDown(self) -> None:
        del self.parser

    def test_parse_board_from_file(self):
        b = self.parser.parse_board_from_file("tests/test_files/simple.txt")
        self.assertEqual(b.width, 2)
        self.assertEqual(b.height, 3)
        self.assertEqual(b._board[1, 1].value, 1)
        self.assertEqual(b._board[2, 1].value, 2)

    def test_parse_file_from_board(self):
        old_board = hb.HitoriBoard(2, 2, [1, 2,
                                          2, 1])
        self.parser.parse_file_from_board(
            "tests/test_files/parsed.txt", old_board)
        new_board = self.parser.parse_board_from_file(
            "tests/test_files/parsed.txt")
        self.assertEqual(old_board.width, new_board.width)
        self.assertEqual(old_board.height, new_board.height)
        self.assertEqual(old_board._board[0, 0].value,
                         new_board._board[0, 0].value)
        self.assertEqual(old_board._board[0, 1].value,
                         new_board._board[0, 1].value)
        self.assertEqual(old_board._board[1, 0].value,
                         new_board._board[1, 0].value)
        self.assertEqual(old_board._board[1, 1].value,
                         new_board._board[1, 1].value)


if __name__ == "__main__":
    unittest.main()
