import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from hitori import hitori_solver as hs


class HitoriSolverTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.solver = hs.HitoriSolver()

    def tearDown(self) -> None:
        del self.solver

    def test_resolve_patterns(self):
        board = hs.HitoriBoard(5, 5,
                               [4, 2, 4, 1, 5,
                                2, 3, 1, 2, 4,
                                5, 4, 3, 2, 4,
                                1, 5, 2, 4, 3,
                                1, 1, 5, 3, 4])
        self.solver.resolve_patterns(board)
        ex = "? . ? ? ? \n? ? ? ? ? \n? ? ? ? ? \n. ? ? ? . \n# . ? . # \n"
        ac = board.to_string_with_symbols()
        self.assertEqual(ac, ex, f"\nExpected:\n{ex}\nActual:\n{ac}")

    def test_resolve_non_repeats(self):
        board = hs.HitoriBoard(3, 3,
                               [1, 2, 3,
                                1, 1, 2,
                                2, 3, 2])
        self.solver.resolve_non_repeats(board, hs.CommandManager())
        ex = "? . . \n? ? ? \n? . ? \n"
        ac = board.to_string_with_symbols()
        self.assertEqual(ac, ex, f"\nExpected:\n{ex}\nActual:\n{ac}")

    def test_resolve_surface_cells(self):
        board = hs.HitoriBoard(3, 3,
                               [1, 2, 3,
                                1, 1, 2,
                                2, 3, 2])
        self.solver.resolve_surface_cells(board, hs.CommandManager())
        ex = ". . ? \n# . . \n. . # \n"
        ac = board.to_string_with_symbols()
        self.assertEqual(ac, ex, f"\nExpected:\n{ex}\nActual:\n{ac}")

    def test_is_solved(self):
        board = hs.HitoriBoard(2, 2, [1, 2,
                                      2, 2])
        solved_before = self.solver.is_solved(board)
        board._board[1, 1].state = hs.CellState.BLACK
        solved_after = self.solver.is_solved(board)
        self.assertFalse(solved_before, "States solved when shouldn't")
        self.assertTrue(solved_after, "Doesn't state solved when should")

    def test_solve_solvable(self):
        board = hs.HitoriBoard(3, 3, [1, 2, 3,
                                      2, 1, 1,
                                      3, 1, 1])

        self.solver.solve(board)
        ex = ". . . \n. # . \n. . # \n"
        ac = board.to_string_with_symbols()
        self.assertEqual(ac, ex, f"\nExpected:\n{ex}\nActual:\n{ac}")

    def test_fail_solve_unsolvable(self):
        board = hs.HitoriBoard(2, 2, [1, 1,
                                      1, 1])
        with self.assertRaises(hs.HitoriNoSolutionError):
            self.solver.solve(board)

    def test_fail_solve_unsolvable_with_diagonal_rule_only(self):
        board = hs.HitoriBoard(3, 3, [1, 2, 3,
                                      2, 1, 1,
                                      3, 1, 1], True)
        # this board is solvable without diagonal rule 
        # see: test_solve_solvable

        with self.assertRaises(hs.HitoriNoSolutionError):
            self.solver.solve(board)


if __name__ == "__main__":
    unittest.main()
