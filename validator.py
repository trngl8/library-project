import re
from library import Book


class Validator():
    def __init__(self):
        self.rules = {}
        self.errors = []

    def add(self, rules: dict):
        for key in rules.keys():
            self.rules[key] = rules[key]

    def add_rule(self, rule : dict):
        self.rules[list(rule.keys())[0]] = rule[list(rule.keys())[0]]

    def validate_book(self, book: Book):
        if len(self.rules) == 0:
            return True
        if isinstance(book.isbn, self.rules["ISBN"]["type"]) and re.match(self.rules["ISBN"]["regexp"],
                                                                            book.isbn) and \
                isinstance(book.year, self.rules["year"]["type"]) and self.rules["year"]["min"] < book.year < \
                self.rules["year"]["max"]:
            return True

    def validate(self, object):
        if isinstance(object, Book):
            return self.validate_book(object)

        for rules in self.rules.values():
            for rule in rules:
                # TODO: implement validation behavior
                result = rule.validate(object)

        if len(object) == 0:
            for i in range(2):
                self.errors.append("Validation failed")
            return False
        for i in self.rules.get(list(object.keys())[0]):
            if not i.validate(object.get(list(object.keys())[0])):
                self.errors.append("Validation failed")
        if len(self.errors) == 0:
            return True
        else:
            return False


class Email:
    def validate(self, email):
        if re.match(r"(?!\.)([a-zA-Z0-9!#$%&'*\
+-/=?^_`{|}~](?!.*\.\.)){1,63}(?<!\.)@[a-z]{1,255}\.(com|or\
g|edu|gov|net|ua)(\.?)((co\
m|org|edu|gov|net|ua)?)", email):
            return True
        else:
            return False
    

class Required:
    def validate(self, string):
        return string is not None and string != ""
