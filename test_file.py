import unittest
from file import FileImport


class TestFileImport(unittest.TestCase):
    def test_import(self):
        importer = FileImport("var/import/")
        importer.process_file("books.csv", "books.csv", "library")
        self.assertEqual(4, len(importer.get_file_lines("books.csv")))

