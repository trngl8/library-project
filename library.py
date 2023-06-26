class Library:
    def __init__(self) -> None:
        self.catalog = []

    def get_count(self):
        return len(self.catalog)
    
    def add_book(self , book):
        self.catalog.append(book)
    

class User:
    def __init__(self , wanted_amount = 10) -> None:
        self.books = []
        self.wanted_amount = wanted_amount

    def available_library(self , library : Library):
        if library.get_count() > self.wanted_amount:
            return True
        return False

    def order_book(self , book):
        self.books.append(book)
    
    def has_books(self):
        if len(self.books) > 0:
            return True
        return False
    

class Book:
    def __init__(self , id = None, ISBN = None, title = None, author = None, year = None , available = None, count = None) -> None:
        self.id = id 
        self.isbn = ISBN
        self.title = title
        self.author = author
        self.year = year
        self.available = available
        self.count = count
