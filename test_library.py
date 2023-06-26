import unittest
from library import Library, Book, User


class TestLibrary(unittest.TestCase):
    """
    Some books
    A visitor is able to visit
    A reader is able to order a book
    """

    def test_library_has_books(self):
        target = Library()
        result = target.get_count()
        self.assertEqual(result, 0)

    def test_user_book(self):
        user = User()
        book = Book()
        library = Library()
        library.add_book(book)
        user.order_book(book)
        self.assertEqual(True, user.has_books())

    def test_library_convenient(self):
        library = Library()
        book = Book()
        library.add_book(book)
        visitor = User(0)

        result = visitor.available_library(library)
        self.assertEqual(True, result)

    def test_book(self):
        book = Book("Python Crash Course", "Eric Matthes", 2019)
        self.assertEqual("Python", book.name)
        self.assertEqual("Eric Matthes", book.author)
        self.assertEqual(2019, book.year)
        self.assertEqual(False, book.available)
        self.assertEqual(0, book.count)


if __name__ == "__main__":
    unittest.main()
