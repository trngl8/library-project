from storage import DataStorage


class Repository:

    def __init__(self, name, storage: DataStorage):
        self.name = name
        self.storage = storage
        self.items = []
        self.items_data = {}

    def load_items(self):
        self.items = []
        lines = self.storage.get_lines(self.name)
        header = self.storage.get_header(self.name)
        columns = [x.lower() for x in header.split(',')]
        for line in lines:
            values = line.split(',')
            self.items.append(dict(zip(columns, values)))

    def load_items_data(self):
        self.items_data = {}
        lines = self.storage.get_lines(self.name)
        header = self.storage.get_header(self.name)
        columns = [x.lower() for x in header.split(',')]
        for line in lines:
            values = line.split(',')
            item_id = int(values[0])
            self.items_data[item_id] = (dict(zip(columns, values)))

    def add_item(self, item):
        self.load_items_data()
        if 0 == len(self.items_data):
            item_id = 1
        else:
            item_id = next(reversed(self.items_data)) + 1
        self.items_data[item_id] = item
        self.storage.add_line(self.name, item)
        return item_id

    def get_item(self, item_id):
        return self.items_data[item_id]

    def remove_item(self, item_id):
        del self.items_data[item_id]

    def update_item(self, item_id, item):
        self.items_data[item_id] = item

    def save(self):
        lines = []
        for item_id, item in self.items_data.items():
            line = str(item_id) + "," + ",".join(item.values())
            lines.append(line)
        self.storage.write_lines(self.name, lines)


class BooksRepository(Repository):
    def find_all(self) -> list:
        if 0 == len(self.items):
            self.load_items()

        result = []
        for item in self.items:
            book = Book(item['title'], item['author'], item['year'])
            book.id = item['id']
            result.append(book)
        return result

    def find(self, item_id):
        if 0 == len(self.items):
            self.load_items()

        for item in self.items:
            if item_id == int(item['id']):
                book = Book(item['title'], item['author'], item['year'])
                book.id = item['id']
                return book
        raise Exception(f"Item with id {item_id} not found")


class UsersRepository(Repository):
    pass


class OrdersRepository(Repository):
    pass


class Library:
    def __init__(self, name, storage: DataStorage):
        self.name = name
        self.catalog = []
        self.users = []
        self.storage = storage
        self.cart = Cart()
        self.repositories = {
            'books': BooksRepository('books', storage),
            'users': UsersRepository('users', storage),
            'orders': OrdersRepository('users', storage)
        }

    def get_count(self):
        return len(self.get_repository('books').find_all())

    def add_book(self, book):
        self.catalog.append(book)
        line = {
            'title': book.title,
            'author': book.author,
            'year': book.year
        }
        book_id = self.storage.add_line('books', line)
        return book_id

    def remove_book(self, book_id):
        self.storage.remove_line('books', book_id)

    def import_books(self, list_of_books, skip_lines=1):
        if len(list_of_books) == 0:
            return

        for i in range(skip_lines):
            list_of_books.pop(0)
        for item in list_of_books:
            self.add_book(Book(item[1], item[2], item[3]))

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
        return self.repositories.get(name)


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
    def __init__(self, title, author, year, ISBN=None, price=100):
        self.id = None
        self.isbn = ISBN
        self.title = title
        self.author = author
        self.year = year
        self.available = False
        self.count = 0
        self.price = price

    def __eq__(self, another) -> bool:
        if self.title == another.title and self.author == another.author and self.year == another.year:
            return True
        return False


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_total(self) -> int:
        total = 0
        for item in self.items:
            total += item.price
        return total

    def clear(self):
        self.items = []
