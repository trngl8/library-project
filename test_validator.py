import unittest
from validator import Validator, Required, Email, Length, Phone, Isbn, Year
from library import Book


class TestValidator(unittest.TestCase):

    def test_validate_empty_rules(self):
        self.validator = Validator()
        self.assertEqual(True, self.validator.validate({}))

    def test_validate_empty_rules_book(self):
        self.validator = Validator()
        book = Book("Python Crash Course", "Eric Matthes", 2019, "9781718502703")
        self.assertEqual(True, self.validator.validate(book))

    def test_validate_book(self):
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

        book1 = Book("Python Crash Course", "Eric Matthes" ,2019, "9781718502703")
        book2 = Book("Python Hard Way", "Zed Shaw", 1899, "9780134692883")
        self.assertEqual(True, self.validator.validate(book1))
        self.assertAlmostEqual(False, self.validator.validate(book2))

    def test_validate_email_success(self):
        validator = Validator()
        validator.add({'email': [Required(), Email()]})
        data = {
            "email": "test@test.com"
        }
        result = validator.validate(data)
        self.assertEqual(True, result)
        self.assertEqual(0, len(validator.errors))

        data = {
            "email": "test@triangle.software"
        }
        result = validator.validate(data)
        self.assertEqual(True, result)

    def test_validate_complex_data(self):
        validator = Validator()
        validator.add({'name': [Required(), Length(min=3, max=50, message="Wrong Length")]})
        validator.add({'email': [Required(), Email()]})
        validator.add({'admin_email': [Email()]})
        data = {
            "name": "Test",
            "email": "test@triangle.software",
            "admin_email": "admin@triangle.software"
        }
        result = validator.validate(data)
        self.assertEqual(True, result)
        self.assertEqual(0, len(validator.errors))

    def test_validate_data_empty(self):
        validator = Validator()
        validator.add({'email': [Required(message="Field is required"), Email(message="Enter a valid email")]})
        data = {}
        result = validator.validate(data)
        self.assertEqual(False, result)
        self.assertEqual(2, len(validator.errors.get('email')))
        self.assertEqual('Field is required', validator.errors.get('email').pop(0))
        self.assertEqual('Enter a valid email', validator.errors.get('email').pop(0))

    def test_validate_email_invalid(self):
        validator = Validator()
        validator.add({'email': [Required(message="Field is required"), Email(message="Enter a valid email")]})
        data = {
            "email": "no_email"
        }
        result = validator.validate(data)
        self.assertEqual(False,result)
        self.assertEqual(1, len(validator.errors.get('email')))
        self.assertEqual('Enter a valid email', validator.errors.get('email').pop(0))

    def test_validate_phone_isbn(self):
        validator = Validator()
        validator.add({"phone" : [Phone(message="Wrong Phone"), Required(message="Field is required")]})
        validator.add({"isbn" : [Isbn(message="Wrong Isbn")]})
        data = {
            "phone" : "+1 (123) 456-7890",
            "isbn" : "9781718502703"
        }
        result = validator.validate(data)
        self.assertEqual(True, result)
        new_data ={
            "phone" : "12345"
        }
        self.assertEqual(validator.validate(new_data), False)
        self.assertEqual(1, len(validator.errors.get('phone')))

    def test_validate_invalid(self):
        validator = Validator()
        validator.add({"code": [Isbn()]})
        validator.add({"phone": [Length(min=3, max=13)]})
        data = {
            "code": "111",
            "phone": "+"
        }
        result = validator.validate(data)
        self.assertEqual(False, result)
        self.assertEqual('Wrong length', validator.errors.get('phone').pop(0))
        self.assertEqual('Wrong ISBN', validator.errors.get('code').pop(0))

    def test_validate_empty(self):
        validator = Validator()
        validator.add({"phone": [Required(), Phone()]})
        validator.add({"name": [Required()]})
        data = {
            "name": None,
            "phone": "",
            "address": "test"
        }
        result = validator.validate(data)
        self.assertEqual(False, result)
        self.assertEqual(2, len(validator.errors.get('phone')))
        self.assertEqual('Field is required', validator.errors.get('phone').pop(0))
        self.assertEqual('Wrong phone', validator.errors.get('phone').pop(0))
        self.assertEqual('Field is required', validator.errors.get('name').pop(0))

    def test_validate_year_valid(self):
        validator = Validator()
        validator.add({"year": [Required(), Year()]})
        data = {
            "year": 2023,
        }
        result = validator.validate(data)
        self.assertEqual(True, result)

    def test_validate_year_invalid(self):
        validator = Validator()
        validator.add({"year": [Required(), Year()]})
        data = {
            "year": 2199,
        }
        result = validator.validate(data)
        self.assertEqual(False, result)


if __name__ == "__main__":
    unittest.main()
