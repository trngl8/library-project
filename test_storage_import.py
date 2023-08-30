import unittest
from unittest.mock import Mock
from file import FileImport


class TestStorageImport(unittest.TestCase):
    def test_import(self):
        library = Mock()
        file = Mock()
        file.save.return_value = "var/import/books.csv"
        importer = FileImport("var/import/")
        result = importer.process_file(file, "books.csv", library)
        self.assertEqual(5, result)


if __name__ == '__main__':
    unittest.main()
