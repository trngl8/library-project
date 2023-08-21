import re
from library import Book


class Validator():
    def __init__(self):
        self.rules = {}
        self.errors = {}

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
                for rule in self.rules:
                    self.errors[rule] = []
                    for i in self.rules[rule]:
                        self.errors[rule].append(i.message)
                return False
            for key in object:
                self.errors[key] = []
                object_to_check = object[key]
                rules_to_check = self.rules[key]
                for i in rules_to_check:
                    if not i.validate(object_to_check):
                        self.errors.get(key).append(i.message)
            checker = 0
            keys_to_remove = []
            for i in self.errors:
                if len(self.errors[i]) == 0:
                    keys_to_remove.append(i)
            for key in keys_to_remove:
                del self.errors[key]
            for key in self.errors:
                checker += len(self.errors[key])
            if checker != 0:
                return False
            return True



class Email:
    def __init__(self, message="Validation error"):
        self.message = message

    def validate(self, string):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', string):
            return True
        else:
            return False
    

class Required:
    def __init__(self, message="Validation error"):
        self.message = message

    def validate(self, string):
        if string is None or string == '':
            return False
        return True


class Length:
    def __init__(self, min, max, message="Validation error"):
        self.min = min
        self.max = max
        self.message = message
    
    def validate(self, string):
        if self.min <= len(string) <= self.max:
            return True
        return False
