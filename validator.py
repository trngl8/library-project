import re
from abc import ABC, abstractmethod


class Validator:
    def __init__(self):
        self.rules = {}
        self.errors = {}

    def add(self, rules: dict):
        for key in rules.keys():
            self.rules[key] = rules[key]

    def validate(self, struct: dict) -> bool:
        if len(self.rules) == 0:
            return True

        for field in self.rules:
            for valid in self.rules[field]:
                if field in struct and valid.validate(struct[field]):
                    continue

                if field not in self.errors:
                    self.errors[field] = []
                self.errors[field].append(valid.message)

        return len(self.errors) == 0


class ValidatorRule(ABC):
    def __init__(self, message="Invalid value"):
        self.message = message

    @abstractmethod
    def validate(self, value) -> bool:
        if value is None:
            return False
        return True


class Required(ValidatorRule):
    def __init__(self, pattern='', message="Field is required"):
        super().__init__(message)
        self.pattern = pattern

    def validate(self, value) -> bool:
        if value == self.pattern:
            return False
        return super().validate(value)


class Expression(Required):
    def __init__(self, expression: str, message="Expression error") -> None:
        super().__init__('', message)
        self.expression = expression

    def validate(self, string):
        if not super().validate(string):
            return False
        return re.match(self.expression, string)


class Email(Expression):
    def __init__(self, message="Wrong email"):
        super().__init__(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message)


class Phone(Expression):
    def __init__(self, message="Wrong phone"):
        super().__init__(r'^(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}$', message)


class Isbn(Expression):
    def __init__(self, message="Wrong ISBN"):
        super().__init__(
            r'^(?:ISBN(?:-13)?:? )?(?=[0-9]{13}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)97[89][- ]?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]$', message)


class Number:
    def __init__(self, min=0, max=1, message="Wrong number"):
        self.min = min
        self.max = max
        self.message = message

    def validate(self, value: int) -> bool:
        return self.min <= value <= self.max


class Length(Number):
    def __init__(self, min, max, message="Wrong length"):
        super().__init__(min, max, message)
    
    def validate(self, string: str) -> bool:
        value = len(string)
        return super().validate(value)
    

class Year(Number):
    def __init__(self, min=1950, max=2199, message="Invalid year") -> None:
        super().__init__(min, max, message)

    def validate(self, year) -> bool:
        try:
            year = int(year)
        except ValueError:
            return False
        return super().validate(year)


class Choice(ValidatorRule):
    def __init__(self, choices: tuple):
        super().__init__()
        self.choices = choices

    def validate(self, value) -> bool:
        return value in self.choices
