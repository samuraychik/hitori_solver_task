import os
import sys
import glob
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import hitori_main as hm


class HitoriMainTestCase(unittest.TestCase):
    def test_fail_bad_path(self):
        with self.assertRaises(SystemExit) as e:
            hm.main(["this_path/does_not/exist"])
        self.assertEqual(e.exception.code, 1)

    def test_fail_missing_cell(self):
        with self.assertRaises(SystemExit) as e:
            hm.main(["tests/test_files/missing_cell.txt"])
        self.assertEqual(e.exception.code, 2)

    def test_fail_wrong_size(self):
        with self.assertRaises(SystemExit) as e:
            hm.main(["tests/test_files/wrong_size.txt"])
        self.assertEqual(e.exception.code, 2)

    def test_fail_unsolvable(self):
        with self.assertRaises(SystemExit) as e:
            hm.main(["tests/test_files/unsolvable.txt"])
        self.assertEqual(e.exception.code, 3)

    def test_solve_real_puzzles(self):
        for file in glob.glob("tests/test_files/real_puzzles/*.txt"):
            with self.assertRaises(SystemExit) as e:
                hm.main([file])
            self.assertEqual(e.exception.code, 0, f"Fail on {file}")


if __name__ == "__main__":
    unittest.main()
