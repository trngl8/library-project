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
        book1 = Book()
        book2 = Book()
        library.add_book(book1)
        library.add_book(book2)
        visitor = User(2)

        result = visitor.available_library(library)
        self.assertEqual(True, result)


if __name__ == "__main__":
    unittest.main()
