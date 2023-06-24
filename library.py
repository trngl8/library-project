class Library:
    def __init__(self) -> None:
        self.catalog = []

    def get_count(self):
        return len(self.catalog)
    
    def addBook(self , book):
        self.catalog.append(book)
    

class User:
    def __init__(self) -> None:
        self.books = []

    def availableLibrary(self , library):
        if isinstance(library , Library):
            return True
        
    def orderBook(self , book):
        self.books.append(book)
    
    def hasBooks(self):
        if len(self.books) > 0:
            return True
        return False
    

class Book:
    def __init__(self , name = None) -> None:
        self.name = name
