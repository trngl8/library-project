import unittest
from unittest.mock import Mock
from file import FileImport


class TestStorageImport(unittest.TestCase):
    def test_import(self):
        filename = "books.csv"
        importer = FileImport("var/import/")
        data = importer.read_data(filename)
        self.assertEqual(5, len(data))


if __name__ == '__main__':
    unittest.main()
