import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from hitori import hitori_parser as hp


class HitoriParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = hp.HitoriParser()

    def tearDown(self) -> None:
        del self.parser

    def test_parse_correctly(self):
        b = self.parser.parse_board_from_file("tests/test_files/simple.txt")
        self.assertEqual(b.width, 2)
        self.assertEqual(b.height, 3)
        self.assertEqual(b._board[1, 1].value, 1)
        self.assertEqual(b._board[2, 1].value, 2)


if __name__ == "__main__":
    unittest.main()
