import unittest
from library import Library, Book, User


class TestLibrary(unittest.TestCase):
    """
    Some books
    A visitor is able to visit
    A reader is able to order a book
    """

    def testLibraryHasBooks(self):
        target = Library()
        result = target.get_count()
        self.assertEqual(result, 0)

    def testLibraryConvenient(self):
        visitor = User()
        target = Library()
        result = visitor.availableLibrary(target)
        self.assertEqual(True, result)

    def testUserBook(self):
        user = User()
        book = Book()
        library = Library()
        library.addBook(book)
        user.orderBook(book)
        self.assertEqual(True, user.hasBooks())


if __name__ == "__main__":
    unittest.main()
