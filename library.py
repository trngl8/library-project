import pandas as pd


class Library:
    def __init__(self) -> None:
        self.catalog = []
        data = read_from_file('library-project/google_books_1299.csv')
        for i in range(len(data)):
            self.addBook(Book(data["ISBN"][i] , data["author"][i] , data["title"][i] , data["published_date"][i]))
        
    def get_count(self):
        return len(self.catalog)

    def addBook(self , book):
        self.catalog.append(book)
     
    def borrowBook(self , book):
        book.isBorrowed = True
        self.catalog.remove(book)
        return f"You have borrowed {book.title}"
    
    def sellBook(self , book):
        book.isBought = True
        self.catalog.remove(book)
        return f"You have bought {book.title}"
    
 
class Book:
    def __init__(self ,isbn ,  author, title, publication_year) -> None:
        self.isbn = isbn
        self.author = author
        self.title = title
        self.publication_year = publication_year
        self.isBorrowed = False
        self.isBought = False

    def __str__(self):
        return f"{self.title} written by {self.author}"
    
    def __repr__(self) -> str:
        return f"{self.title} written by {self.author}"
    
class User:
    def __init__(self ,readerCardNumber,name , surname,email ) -> None:
        self.readerCardNumber = readerCardNumber
        self.name = name
        self.surname = surname
        self.email = email
        self.borrowedBooks = []
        self.boughtBooks = []
        self.mylibrary = None

    def availableLibrary(self,library):
        if not isinstance(library , Library):
            return False
        if library.get_count() >0:
            self.mylibrary = library
            return True
        
    def orderBook(self , book):
        self.boughtBooks.append(book)
        self.mylibrary.sellBook(book)
        self.boughtBooks.append(book)

    def hasBooks(self):
        if len(self.borrowedBooks) + len(self.boughtBooks) > 0:
            return True
        return False

def read_from_file(file_path):
    data = pd.read_csv(file_path)
    return data

if __name__ == "__main__":
    library = Library()
    print(library.get_count())


