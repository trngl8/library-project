import unittest
from file import FileImport


class TestLibrary(unittest.TestCase):
    def test_import_file(self):
        file_importer = FileImport('var/import/')
        result = file_importer.import_file('test.csv')
        self.assertEqual(4, result)
