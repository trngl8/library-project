import unittest
from library import Library, Book, User, Visitor


class TestLibrary(unittest.TestCase):
    """
    Some books
    A visitor is able to visit
    A reader is able to order a book
    """

    def test_library_no_books(self):
        target = Library()
        result = target.get_count()
        self.assertEqual(result, 0)

    def test_library_has_books(self):
        target = Library()
        book = Book("Python Crash Course", "Eric Matthes", 2019)
        target.add_book(book)
        result = target.get_count()
        self.assertEqual(result, 1)

    def test_user_book(self):
        user = User('test', 'test@test.com', '123456789')
        book = Book("Python Crash Course", "Eric Matthes", 2019)
        library = Library()
        library.add_book(book)
        user.order_book(book)
        self.assertEqual(True, user.has_books())

    def test_library_not_convenient(self):
        library = Library()
        visitor = Visitor(2)
        result = visitor.available_library(library)
        self.assertEqual(False, result)

    def test_library_convenient(self):
        library = Library()
        book1 = Book("Python Hard Way", "Zed Shaw", 2013)
        book2 = Book("Python Hard Way", "Zed Shaw", 2013)
        library.add_book(book1)
        library.add_book(book2)
        visitor = Visitor(2)
        result = visitor.available_library(library)
        self.assertEqual(True, result)

    def test_book(self):
        book = Book("Python Crash Course", "Eric Matthes", 2019)
        self.assertEqual("Python Crash Course", book.title)
        self.assertEqual("Eric Matthes", book.author)
        self.assertEqual(2019, book.year)
        self.assertEqual(False, book.available)
        self.assertEqual(0, book.count)

    def test_import_books(self):
        library = Library()
        book1 = Book("Python Crash Course", "Eric Matthes", 2019)
        book2 = Book("Python Hard Way", "Zed Shaw", 2013)
        book3 = Book("Head First Python", "Paul Barry", 2016)
        library.import_books([
            ["Python Crash Course", "Eric Matthes", 2019],
            ["Python Hard Way", "Zed Shaw", 2013],
            ["Head First Python", "Paul Barry", 2016]
        ])
        self.assertEqual(3, library.get_count())
        self.assertEqual(book1, library.catalog[0])
        self.assertEqual(book2, library.catalog[1])
        self.assertEqual(book3, library.catalog[2])


if __name__ == "__main__":
    unittest.main()
