import csv


class Library:
    def __init__(self) -> None:
        self.catalog = []

    def get_count(self):
        return len(self.catalog)

    def add_book(self, book):
        self.catalog.append(book)

    def import_books(self, list_of_books):
        for item in list_of_books:
            self.add_book(Book(item[0], item[1], item[2]))

    @staticmethod
    def read_from_csv_catalog(path):
        with open(path, 'r') as file:
            reader = csv.reader(file)
            reader = list(reader)
        return reader


class User:
    def __init__(self, wanted_amount=10) -> None:
        self.books = []
        self.wanted_amount = wanted_amount

    def available_library(self, library: Library):
        if library.get_count() >= self.wanted_amount:
            return True
        return False

    def order_book(self, book):
        self.books.append(book)

    def has_books(self):
        if len(self.books) > 0:
            return True
        return False


class Book:
    def __init__(self, title, author, year, ISBN=None) -> None:
        self.id = 1
        self.isbn = ISBN
        self.title = title
        self.author = author
        self.year = year
        self.available = False
        self.count = 0

    def __eq__(self, anohter) -> bool:
        if self.title == anohter.title and self.author == anohter.author and self.year == anohter.year:
            return True
        return False
