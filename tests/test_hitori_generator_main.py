import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import hitori_generator_main as hgm
import hitori_solver_main as hsm


class HitoriMainTestCase(unittest.TestCase):
    def test_fail_bad_path(self):
        with self.assertRaises(SystemExit) as e:
            hgm.main(["this_path/does_not/exist",
                      "-x 5", "-y 5"])
        self.assertEqual(e.exception.code, 1)

    def test_fail_wrong_width(self):
        with self.assertRaises(SystemExit) as e:
            hgm.main(["tests/test_files/wrong_width.txt",
                      "-x 0", "-y 5"])
        self.assertEqual(e.exception.code, 2)

    def test_fail_wrong_height(self):
        with self.assertRaises(SystemExit) as e:
            hgm.main(["tests/test_files/wrong_height.txt",
                      "-x 5", "-y -2"])
        self.assertEqual(e.exception.code, 2)

    def test_generate_and_solve(self):
        with self.assertRaises(SystemExit) as e:
            hgm.main(["tests/test_files/generated.txt",
                      "-x 5", "-y 5"])
        self.assertEqual(e.exception.code, 0, "Failed to generate")

        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/generated.txt"])
        self.assertEqual(e.exception.code, 0, "Failed to solve")

    def test_generate_and_solve_with_diagonal_rule(self):
        with self.assertRaises(SystemExit) as e:
            hgm.main(["tests/test_files/generated_d.txt",
                      "-x 5", "-y 5", "-d"])
        self.assertEqual(e.exception.code, 0, "Failed to generate")

        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/generated_d.txt"])
        self.assertEqual(e.exception.code, 0, "Failed to solve")

    def test_generate_and_solve_big(self):
        with self.assertRaises(SystemExit) as e:
            hgm.main(["tests/test_files/generated_b.txt",
                      "-x 20", "-y 20"])
        self.assertEqual(e.exception.code, 0, "Failed to generate")

        with self.assertRaises(SystemExit) as e:
            hsm.main(["tests/test_files/generated_b.txt"])
        self.assertEqual(e.exception.code, 0, "Failed to solve")


if __name__ == "__main__":
    unittest.main()
