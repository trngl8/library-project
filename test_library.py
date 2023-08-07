import unittest
from library import Library, Book, User, Visitor
from unittest.mock import Mock


class TestLibrary(unittest.TestCase):
    """
    Some books
    A visitor is able to visit
    A reader is able to order a book
    """

    def setUp(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = [
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ]
        self.library = Library('test', storage)
        self.library.import_books([
            ["ID", "TITLE", "AUTHOR", "YEAR"],
            [1, "Python Crash Course", "Eric Matthes", 2019],
            [2, "Python Hard Way", "Zed Shaw", 2013],
            [3, "Head First Python", "Paul Barry", 2016],
            [4, "Startup Hard Development", "Roman Anderson", 2019]
        ])

    def test_library_no_books(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = []
        target = Library('test', storage)
        result = target.get_count()
        self.assertEqual(result, 0)

    def test_library_has_books(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = [
            '1,Python Crash Course,Eric Matthes,2019',
        ]
        target = Library('test', storage)
        book = Book(1, "Python Crash Course", "Eric Matthes", 2019)
        target.add_book(book)
        result = target.get_count()
        self.assertEqual(result, 1)

    def test_user_book(self):
        storage = Mock()
        user = User('test', 'test@test.com', '123456789')
        book = Book(1, "Python Crash Course", "Eric Matthes", 2019)
        library = Library('test', storage)
        library.add_book(book)
        self.assertEqual(False, user.has_books())
        user.order_book(book)
        self.assertEqual(True, user.has_books())

    def test_library_not_convenient(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = []
        library = Library('test', storage)
        visitor = Visitor(2)
        result = visitor.available_library(library)
        self.assertEqual(False, result)

    def test_library_convenient(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = [
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
        ]
        library = Library('test', storage)
        book1 = Book(1, "Python Hard Way", "Zed Shaw", 2013)
        book2 = Book(2, "Python Hard Way", "Zed Shaw", 2013)
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
        library = self.library
        storage = Mock()
        import_library = Library('No import', storage)
        self.assertEqual(None, import_library.import_books([]))
        book1 = Book("Python Crash Course", "Eric Matthes", 2019)
        book2 = Book("Python Hard Way", "Zed Shaw", 2013)
        book3 = Book("Head First Python", "Paul Barry", 2016)
        self.assertFalse(book1 == book2)
        self.assertEqual(4, library.get_count())
        self.assertEqual(book1, library.catalog[0])
        self.assertEqual(book2, library.catalog[1])
        self.assertEqual(book3, library.catalog[2])


    def test_find_books(self):
        library = self.library

        result = library.find_books(title="python")
        self.assertEqual(3, len(result))
        self.assertEqual("Python Crash Course", result[0].title)
        self.assertEqual("Python Hard Way", result[1].title)
        self.assertEqual("Head First Python", result[2].title)

        result = library.find_books(title="python", author="eric")
        self.assertEqual(1, len(result))
        self.assertEqual("Python Crash Course", result[0].title)

        result = library.find_books(year=2019)
        self.assertEqual(2, len(result))
        self.assertEqual("Python Crash Course", result[0].title)
        self.assertEqual("Startup Hard Development", result[1].title)

        result = library.find_books(year=2022, title="python")
        self.assertEqual(0, len(result))

        result = library.find_books()
        self.assertEqual(0, len(result))

        result = library.find_books(title="python", author="", year="", isbn="")
        self.assertEqual(3, len(result))

    def test_find_books_all(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = [
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ]
        library = Library('test', storage)
        list_books = library.get_repository('books').find_all()
        self.assertEqual(4, len(list_books))

    def test_find_book_by_id(self):
        storage = Mock()
        storage.get_header.return_value = 'ID,TITLE,AUTHOR,YEAR'
        storage.get_lines.return_value = [
            '1,Python Crash Course,Eric Matthes,2019',
            '2,Python Hard Way,Zed Shaw,2013',
            '3,Head First Python,Paul Barry,2016',
            '4,Startup Hard Development,Roman Anderson,2019'
        ]
        library = Library('test', storage)
        book = library.get_repository('books').find(2)
        self.assertEqual('Python Hard Way', book.title)
        with self.assertRaises(Exception):
            library.get_repository('books').find(9)

    def test_add_user(self):
        library = self.library
        library.add_user(User("Artem", 'artemkrayevskiy@gmail.com', "0676708881"))


if __name__ == "__main__":
    unittest.main()
