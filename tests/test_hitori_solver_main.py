import os
import sys
import glob
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import hitori_solver_main as hsm


class HitoriMainTestCase(unittest.TestCase):
    def test_fail_bad_path(self):
        with self.assertRaises(SystemExit) as e:
            hsm.main(["this_path/does_not/exist"])
        self.assertEqual(e.exception.code, 1)

    def test_fail_missing_cell(self):
        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/missing_cell.txt"])
        self.assertEqual(e.exception.code, 2)

    def test_fail_wrong_size(self):
        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/wrong_size.txt"])
        self.assertEqual(e.exception.code, 2)

    def test_fail_unsolvable(self):
        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/unsolvable.txt"])
        self.assertEqual(e.exception.code, 3)

    def test_solve_real_puzzles(self):
        for file in glob.glob("tests/test_files/real_puzzles/*.txt"):
            with self.assertRaises(SystemExit) as e:
                hsm.main([file])
            self.assertEqual(e.exception.code, 0, f"Fail on {file}")

    def test_enable_diagonal_rule_and_fail(self):
        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/real_puzzles/easy_1.txt"])
        self.assertEqual(e.exception.code, 0, "Should have solved with "
                         "diagonal rule disabled")

        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/real_puzzles/easy_1.txt", "-d"])
        self.assertEqual(e.exception.code, 3, "Should not have solved with "
                         "diagonal rule enabled")


if __name__ == "__main__":
    unittest.main()
