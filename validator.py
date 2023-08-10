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
        else:
            if len(object) == 0:
                checker = []
                for rule in self.rules:
                    for i in self.rules[rule]:
                        if i not in checker:
                            checker.append(i)
                self.errors = ["Validation error"]* len(checker)
                return False
            for key in object:
                object_to_check = object[key]
                rules_to_check = self.rules[key]
                for i in rules_to_check:
                    if not i.validate(object_to_check):
                        self.errors.append("Validation error")
            if len(self.errors) != 0:
                return False
            return True



class Email:
    def validate(self, string):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', string):
            return True
        else:
            return False
    

class Required:
    def validate(self, string):
        if string is None or string == '':
            return False
        return True


class Length:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def validate(self, string):
        if self.min <= len(string) <= self.max:
            return True
        return False
