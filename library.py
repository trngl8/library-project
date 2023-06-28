import csv


class Library:
    def __init__(self) -> None:
        self.catalog = []

    def get_count(self):
        return len(self.catalog)
    
    def add_book(self , book):
        self.catalog.append(book)
    
    def get_catalog(self , path):
        with open(path , 'r') as file:
            reader = csv.reader(file)
            reader = list(reader)
        self.catalog = reader[1:]
         
class User:
    def __init__(self , wanted_amount = 10) -> None:
        self.books = []
        self.wanted_amount = wanted_amount

    def available_library(self , library : Library):
        if library.get_count() >= self.wanted_amount:
            return True
        return False

    def order_book(self , book):
        self.books.append(book)
    
    def has_books(self):
        if len(self.books) > 0:
            return True
        return False
    

class Book:
    def __init__(self, title, author, year, ISBN=None) -> None:
        self.isbn = ISBN
        self.title = title
        self.author = author
        self.year = year
        self.available = False
        self.count = 0


    def __eq__(self, anohter) -> bool:
        if self.name == anohter.name and self.author == anohter.author:
            return True
        return False

def create_csv(path):
    column_names = ['id' , 'ISBN' , "Titile" , "Author", "Year", "Available", "Count"]
    with open(path , 'w') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)

def add_book_to_csv(book : Book , path):
    if  not check_if_book_in_csv(path = path, book=book)[0]:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        data.append([book.id, book.isbn, book.name, book.author,\
                            book.year, book.available, book.count])
        with open(path , 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    elif check_if_book_in_csv(path = path, book = book)[0]:
        row_number = check_if_book_in_csv(path = path, book = book)[1]
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        data[row_number][6] = int(data[row_number][6])
        data[row_number][6] += 1
        with open(path , 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)

def check_if_book_in_csv(path , book):
    with open(path , 'r') as file:
        reader = csv.reader(file)
        reader = list(reader)
        for number_of_row , row in enumerate(reader):
            if book == Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6]):
                return True , number_of_row
        return False , 0


if __name__ == "__main__":
    create_csv('new_books.csv')
    book1 = Book(title="My name is book" , id = 1 , author = "Me")
    add_book_to_csv(book = book1, path = 'new_books.csv')
    book2 = Book(title="My name is book" , id = 2 , author = 'Me')
    add_book_to_csv(book = book2, path = 'new_books.csv')
