import unittest
from validator import Validator, Required, Email, Length, Phone, Isbn, Year, Choice, Username
from library import Book


class TestValidator(unittest.TestCase):

    def test_validate_empty_rules(self):
        self.validator = Validator()
        self.assertEqual(True, self.validator.validate({}))

    def test_validate_empty_rules_book(self):
        self.validator = Validator()
        book = Book("Python Crash Course", "Eric Matthes", 2019, "9781718502703")
        self.assertEqual(True, self.validator.validate(book))

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
        validator.add({"test": [Required()]})
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
        self.assertEqual(1, len(validator.errors.get('test')))
        self.assertEqual('Field is required', validator.errors.get('test').pop(0))

    def test_validate_year_valid(self):
        validator = Validator()
        validator.add({"year": [Required(), Year()]})
        validator.add({"year_more": [Required(), Year(min=1970, max=2023)]})
        data = {
            "year": 1970,
            "year_more": "1970",
        }
        result = validator.validate(data)
        self.assertEqual(True, result)

    def test_validate_year_invalid(self):
        validator = Validator()
        validator.add({"year": [Required(), Year()]})
        validator.add({"year_more": [Required(), Year(min=1970, max=2050, message="Should be between 1970 and 2050")]})
        data = {
            "year": 2299,
            "year_more": "2199",
        }
        result = validator.validate(data)
        self.assertEqual(False, result)
        self.assertEqual(1, len(validator.errors.get('year_more')))
        self.assertEqual(1, len(validator.errors.get('year')))
        self.assertEqual('Invalid year', validator.errors.get('year').pop(0))
        self.assertEqual('Should be between 1970 and 2050', validator.errors.get('year_more').pop(0))

    def test_value_error(self):
        validator = Validator()
        validator.add({"year": [Required(), Year()]})
        data = {
            "year": "",
        }
        result = validator.validate(data)
        self.assertEqual(False, result)

    def test_validator_choice(self):
        validator = Validator()
        validator.add({"choice": [Required(), Choice(("yes", "no",))]})
        validator.add({"alternative_choice": [Required(), Choice((True, False,))]})
        data = {
            "choice": "yes",
            "alternative_choice": True
        }
        result = validator.validate(data)
        self.assertEqual(True, result)

    def test_validator_choice_invalid(self):
        validator = Validator()
        validator.add({"more": [Required(), Choice(("known", "another",))]})
        data = {
            "more": "unknown"
        }
        result = validator.validate(data)
        self.assertEqual(False, result)

    def test_validator_username_invalid(self):
        validator = Validator()
        validator.add({"username": [Username()]})
        data = {
            "username": "&2jdsd+"
        }
        result = validator.validate(data)
        self.assertEqual(False, result)

    def test_validator_username_valid(self):
        validator = Validator()
        validator.add({"username": [Username()]})
        data = {
            "username": "test.com"
        }
        result = validator.validate(data)
        self.assertEqual(True, result)


if __name__ == "__main__":
    unittest.main()
