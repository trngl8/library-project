import unittest
from library import Library, Book, User, Visitor
from main import find_book

class TestConsole(unittest.TestCase):

    def test_find_book(self):
        library = Library()
        book1 = Book("Python Crash Course", "Eric Matthes", 2019)
        book2 = Book("Python Hard Way", "Zed Shaw", 2013)
        book3 = Book("Head First Python", "Paul Barry", 2016)
        library.import_books([
            ["Python Crash Course", "Eric Matthes", 2019],
            ["Python Hard Way", "Zed Shaw", 2013],
            ["Head First Python", "Paul Barry", 2016]
        ])

        pass


if __name__ == "__main__":
    unittest.main()
