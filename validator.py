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
        return False

    def validate(self, object):
        if isinstance(object, Book):
            return self.validate_book(object)
        if len(object) == 0:
            for i in range(len(self.rules['email'])):
                self.errors.append("Validation failed")
            return False
        for i in self.rules.get(list(object.keys())[0]):
            if not i.validate(object):
                self.errors.append("Validation failed")
        if len(self.errors) == 0:
            return True
        else:
            return False


class Email:
    def validate(self, data):
        if re.match(r"(?!\.)([a-zA-Z0-9!#$%&'*\
+-/=?^_`{|}~](?!.*\.\.)){1,63}(?<!\.)@[a-z]{1,255}\.(com|or\
g|edu|gov|net|ua)(\.?)((co\
m|org|edu|gov|net|ua)?)", data['email']):
            return True
        else:
            return False
    

class Required:
    def validate(self, data):
        for key in data:
            if data[key] is None or data[key] == '':
                return False
        return True
