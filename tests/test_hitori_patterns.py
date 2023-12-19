import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from hitori_solver import hitori_patterns as hp


class HitoriBoardTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        del self.pr

    def test_resolve_repeats_in_row(self):
        board = hp.HitoriBoard(4, 1, [1, 1, 2, 1])
        self.pr = hp.HitoriPatternsResolver(board)
        self.pr.resolve_repeats()
        expected = "? ? . # \n"
        self.assertEqual(board.to_string_with_symbols(), expected)

    def test_resolve_repeats_in_col(self):
        board = hp.HitoriBoard(1, 5, [1, 1, 2, 3, 1])
        self.pr = hp.HitoriPatternsResolver(board)
        self.pr.resolve_repeats()
        expected = "? \n? \n? \n. \n# \n"
        self.assertEqual(board.to_string_with_symbols(), expected)        

    def test_resolve_corners(self):
        board = hp.HitoriBoard(3, 3, [2, 2, 1, 2, 1, 3, 1, 3, 2])
        self.pr = hp.HitoriPatternsResolver(board)
        self.pr.resolve_triple_corners()
        expected = "# . ? \n. ? ? \n? ? ? \n"
        self.assertEqual(board.to_string_with_symbols(), expected)

    def test_resolve_sandwiches(self):
        board = hp.HitoriBoard(3, 3, [2, 2, 2, 4, 5, 6, 1, 3, 1])
        self.pr = hp.HitoriPatternsResolver(board)
        self.pr.resolve_sandwiches()
        expected = "# . # \n. ? . \n? . ? \n"
        self.assertEqual(board.to_string_with_symbols(), expected)


if __name__ == "__main__":
    unittest.main()
