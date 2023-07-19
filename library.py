from storage import DataStorage
import re


class Library:
    def __init__(self, name, storage: DataStorage):
        self.name = name
        self.catalog = []
        self.users = []
        self.storage = storage

    def get_count(self):
        return len(self.catalog)

    def add_book(self, book):
        book.id = len(self.catalog) + 1
        self.catalog.append(book)

    def find_book(self, find_id):
        for item in self.catalog:
            if item.id == find_id:
                return item
        return None

    def import_books(self, skip_lines=1):
        list_of_books = self.storage.read_from_csv_catalog()
        if len(list_of_books) == 0:
            return

        for i in range(skip_lines):
            list_of_books.pop(0)
        for item in list_of_books:
            self.add_book(Book(item[1], item[2], item[3]))



    def add_user(self, user):
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


class Visitor:
    def __init__(self, wanted_amount=1):
        self.wanted_amount = wanted_amount

    def available_library(self, library: Library):
        if library.get_count() >= self.wanted_amount:
            return True
        return False


class User(Visitor):
    def __init__(self, name, email, phone, wanted_amount=10) -> None:
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
    def __init__(self, title, author, year, ISBN=None) -> None:
        self.id = None
        if ISBN == None or re.match(r"^(?:ISBN(?:-13)?:? )?(?=[0-9]{13}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)97[89][- ]?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]$", ISBN):
            self.isbn = ISBN
        else:
            raise Exception("You enetered wrong ISBN")
        self.title = title
        self.author = author
        self.year = year
        self.available = False
        self.count = 0

    def __eq__(self, another) -> bool:
        if self.title == another.title and self.author == another.author and self.year == another.year:
            return True
        return False

    def __repr__(self) -> str:
        return f"Book {self.title} written by {self.author} in {self.year}"
