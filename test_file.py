from file import process_lines
from unittest import TestCase


class TestFileImport(TestCase):
    def test_process_file(self):
        lines = [
            'ID,TITLE,AUTHOR,YEAR',
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ]
        result = process_lines(lines)
        self.assertEqual(4, result)
