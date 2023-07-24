import unittest


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()
        self.validator.add_rule({
            "ISBN": {
                "type": "string",
                "regexp": "(?:ISBN(?:-13)?:? )?(?=[0-9]{13}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)97[89][- ]?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]"
            },
        })
        self.validator.add_rule({
            "year": {
                "type": "integer",
                "min": 1900,
                "max": 2050
            },
        })

    def test_validate(self):
        self.assertEqual(True, self.validator.validate())
