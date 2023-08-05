import unittest
from unittest.mock import Mock

from storage import DataStorage


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.file_lines = Mock()
        self.file_lines.read_lines.return_value = [
            'ID,TITLE,AUTHOR,YEAR',
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ]

    def test_get_lines(self):
        storage = DataStorage(self.file_lines)
        self.assertEqual(4, storage.get_count('books'))
        self.assertEqual('ID,TITLE,AUTHOR,YEAR', storage.get_header('books'))
        self.assertEqual([
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ], storage.get_lines('books'))

    def test_add_line(self):
        storage = DataStorage(self.file_lines)
        storage.add_line('books', {
            'title': 'Test',
            'author': 'Test',
            'year': '2020'
        })
        self.assertEqual(5, storage.get_count('books'))
        self.assertEqual('ID,TITLE,AUTHOR,YEAR', storage.get_header('books'))
        self.assertEqual([
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019',
            '5,Test,Test,2020'
        ], storage.get_lines('books'))

    def test_remove_line(self):
        storage = DataStorage(self.file_lines)
        storage.remove_line('books', 1)
        self.assertEqual(3, storage.get_count('books'))
        self.assertEqual('ID,TITLE,AUTHOR,YEAR', storage.get_header('books'))
        self.assertEqual([
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ], storage.get_lines('books'))


if __name__ == "__main__":
    unittest.main()
