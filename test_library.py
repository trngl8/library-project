import unittest


class TestLibrary(unittest.TestCase):
    """ Some books
A visitor is able to visit
A reader is able to order a book """

    def test_are_books(self):
        target = Library()
        result = target.get_count()
        self.assertEqual(result, 100)

if __name__ == "__main__":
    unittest.main()
