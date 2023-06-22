import pandas as pd


class Library:
    def __init__(self) -> None:
        self.catalog = []
        
    def get_count(self):
        return len(self.catalog)

    def add_book(self , book):
        self.catalog.append(book)
     
    def borrow_book(self , book):
        book.is_borrowed = True
        self.catalog.remove(book)
        return f"You have borrowed {book.title}"
    
 
class Book:
    def __init__(self ,isbn ,  author, title, publication_year) -> None:
        self.isbn = isbn
        self.author = author
        self.title = title
        self.publication_year = publication_year
        self.is_borrowed = False

    def __str__(self):
        return f"{self.title} written by {self.author}"
    
    def __repr__(self) -> str:
        return f"{self.title} written by {self.author}"

def read_from_file(file_path):
    data = pd.read_csv(file_path)
    return data

if __name__ == "__main__":
    library = Library()
    data = read_from_file('google_books_1299.csv')
    for i in range(len(data)):
        library.add_book(Book(data["ISBN"][i] , data["author"][i] , data["title"][i] , data["published_date"][i]))
