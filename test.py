from app import hello
from customTypes import Number
import unittest


def increment(n: Number) -> Number:
    return n + 1


class Test1(unittest.TestCase):
    def test(self):
        self.assertEqual(increment(3), 4)
