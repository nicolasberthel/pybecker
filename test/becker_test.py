import unittest

from pybecker.becker_helper import generate_code
from pybecker.becker import COMMAND_UP
from pybecker.becker import COMMAND_DOWN
from pybecker.becker import COMMAND_HALT
from pybecker.database import Database


class TestBecker(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBecker, self).__init__(*args, **kwargs)
        self.db = Database()

    def test_db_init(self):
        unit = self.db.get_unit(1)
        self.assertEqual(unit[0], "1737b")

    def test_generate_up(self):
        unit = ['1737b', 0, 0]
        code = generate_code(1, unit, COMMAND_UP)
        self.assertEqual(code, "0000000002010B00000000001737B02101010020B4")

    def test_generate_down(self):
        unit = ['1737b', 0, 0]
        code = generate_code(1, unit, COMMAND_DOWN)
        self.assertEqual(code, "0000000002010B00000000001737B0210101004094")

    def test_generate_halt(self):
        unit = ['1737b', 0, 0]
        code = generate_code(1, unit, COMMAND_HALT)
        self.assertEqual(code, "0000000002010B00000000001737B02101010010C4")
