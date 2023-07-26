import unittest
from validator import Validator
from library import Book

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()
        self.validator.add_rule({
            "ISBN": {
                "type": str,
                "regexp": r"^(?:ISBN(?:-13)?:? )?(?=[0-9]{13}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)97[89][- ]?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]$"
            },
        })
        self.validator.add_rule({
            "year": {
                "type": int,
                "min": 1900,
                "max": 2050
            },
        })

    def test_validate(self):
        book1 = Book(1, "Python Crash Course", "Eric Matthes" ,2019, "9781718502703")
        book2 = Book(2,"Python Hard Way", "Zed Shaw", 1899, "9780134692883")
        self.assertEqual(True, self.validator.validate(book1))
        self.assertAlmostEqual(False, self.validator.validate(book2))


if __name__ == "__main__":
    unittest.main()
