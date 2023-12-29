import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from hitori import hitori_generator as hg


class HitoriParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.gen = hg.HitoriGenerator()

    def tearDown(self) -> None:
        del self.gen

    def test_generate_successfully(self):
        generated = False
        fails = 0

        while not generated:
            try:
                self.gen.generate(5, 5)
                self.gen.generate(5, 5, True)
                self.gen.generate(20, 20)
                self.gen.generate(5, 20)
                self.gen.generate(1, 20)
            except hg.HitoriRetryGenerationError:
                fails += 1
            else:
                generated = True

        self.assertLess(fails, 42)


if __name__ == "__main__":
    unittest.main()
