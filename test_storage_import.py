import unittest
from unittest.mock import Mock
from file import FileImport


class TestStorageImport(unittest.TestCase):
    def test_import(self):
        importer = FileImport("var/import/", "test.csv")
        data = importer.lines
        self.assertEqual(1, len(data))


if __name__ == '__main__':
    unittest.main()
