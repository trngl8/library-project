import re
from library import Book



class Validator():
    def __init__(self):
        self.rules = {}
    
    def add_rule(self, rule : dict):
        self.rules[list(rule.keys())[0]] = rule[list(rule.keys())[0]]

    def validate(self, book : Book):
        if len(self.rules) == 0:
            return True
        if isinstance(book.isbn, self.rules["ISBN"]["type"]) and re.match(self.rules["ISBN"]["regexp"], book.isbn) and \
isinstance(book.year, self.rules["year"]["type"]) and self.rules["year"]["min"]< book.year < self.rules["year"]["max"]:
            return True
        return False


