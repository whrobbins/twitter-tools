
from unittest import TestCase

from _pytest import unittest

from src.api.json_io import JsonIO


class TestJsonIO(TestCase):
    """
    Tests JsonIO class for easily reading in json and writing objects to file
    Derived from Assignment 2
    """
    def setUp(self):
        self.io = JsonIO('testio.json')

    def test_save_to_file(self):
        self.io.save_to_file({'test_data': 1})
        with open('testio.json', 'w'):
            pass

    def test_read_from_file(self):
        self.io.save_to_file({'test_data': 1})
        data = self.io.read_from_file()
        if data:
            self.assertEquals(data['test_data'], 1)


if __name__ == '__main__':
    unittest.main()