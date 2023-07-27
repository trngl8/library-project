from storage import DataStorage
import re


class Repository:

    def __init__(self, name, storage: DataStorage):
        self.name = name
        self.storage = storage
        self.items = []

    def load_items(self):
        self.items = []
        lines = self.storage.get_file_lines(self.name)
        col_lines = lines[:]

        columns = [x.lower() for x in col_lines.pop(0).split(',')]
        for line in col_lines:
            values = line.split(',')
            self.items.append(dict(zip(columns, values)))

    def find_all(self) -> list:
        if 0 == len(self.items):
            self.load_items()

        result = []
        for item in self.items:
            result.append(Book(int(item['id']), item['title'], item['author'], item['year']))
        return result

    def find(self, item_id):
        if 0 == len(self.items):
            self.load_items()

        for item in self.items:
            if item_id == int(item['id']):
                return Book(int(item['id']), item['title'], item['author'], item['year'])
        raise Exception(f"Item with id {item_id} not found")


class Library:
    def __init__(self, name, storage: DataStorage):
        self.name = name
        self.catalog = []
        self.users = []
        self.storage = storage

    def get_count(self):
        return len(self.get_repository('books').find_all())

    def add_book(self, book):
        book.id = len(self.catalog) + 1
        self.catalog.append(book)

    def find_book(self, find_id):
        for item in self.catalog:
            if item.id == find_id:
                return item
        return None

    def import_books(self, list_of_books, skip_lines=1):
        if len(list_of_books) == 0:
            return

        for i in range(skip_lines):
            list_of_books.pop(0)
        for item in list_of_books:
            self.add_book(Book(item[0], item[1], item[2], item[3]))

    def add_user(self, user):
        self.storage.save_user(user)
        self.users.append(user)

    def find_books(self, **kwargs):
        if not kwargs:
            return []

        year = kwargs.get("year", 0)
        title = kwargs.get("title", '')
        author = kwargs.get("author", '')

        filtered = self.catalog

        if year:
            filtered = [book for book in filtered if year == book.year]
        if len(title) > 0:
            filtered = [book for book in filtered if title.lower() in book.title.lower()]
        if len(author) > 0:
            filtered = [book for book in filtered if author.lower() in book.author.lower()]

        return filtered

    def get_repository(self, name):
        return Repository(name, self.storage)


class Visitor:
    def __init__(self, wanted_amount=1):
        self.wanted_amount = wanted_amount

    def available_library(self, library: Library):
        if library.get_count() >= self.wanted_amount:
            return True
        return False


class User(Visitor):
    def __init__(self, name, email, phone, wanted_amount=10):
        super().__init__(wanted_amount)
        self.name = name
        self.email = email
        self.phone = phone
        self.books = []

    def order_book(self, book):
        self.books.append(book)

    def has_books(self):
        if len(self.books) > 0:
            return True
        return False


class Book:
    def __init__(self, id, title, author, year, ISBN=None):
        self.id = id
        self.isbn = ISBN
        self.title = title
        self.author = author
        self.year = year
        self.available = False
        self.count = 0

    def __eq__(self, another) -> bool:
        if self.title == another.title and self.author == another.author and self.year == another.year:
            return True
        return False
