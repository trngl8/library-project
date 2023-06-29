import csv


class Library:
    def __init__(self) -> None:
        self.catalog = []

    def get_count(self):
        return len(self.catalog)
    
    def add_book(self , book):
        self.catalog.append(book)
    
    def import_books(self , lst_of_books):
        self.catalog = lst_of_books
    
    @staticmethod
    def read_from_csv_catalog(path):
        with open(path , 'r') as file:
            reader = csv.reader(file)
            reader = list(reader)
         
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
    def __init__(self, title = None, author = None, year = 0 , available = False, count = 0) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.available = False
        self.count = 0


    def __eq__(self, anohter) -> bool:
        if self.title == anohter.title and self.author == anohter.author:
            return True
        return False

# def create_csv(path):
#     column_names = ['id' , 'ISBN' , "Titile" , "Author", "Year", "Available", "Count"]
#     with open(path , 'w') as file:
#         writer = csv.writer(file)
#         writer.writerow(column_names)

# def add_book_to_csv(book : Book , path):
#     if  not check_if_book_in_csv(path = path, book=book)[0]:
#         with open(path, 'r') as file:
#             reader = csv.reader(file)
#             data = list(reader)
#         data.append([book.title, book.author,\
#                             book.year, book.available, book.count])
#         with open(path , 'w') as file:
#             writer = csv.writer(file)
#             writer.writerows(data)
#     elif check_if_book_in_csv(path = path, book = book)[0]:
#         row_number = check_if_book_in_csv(path = path, book = book)[1]
#         with open(path, 'r') as file:
#             reader = csv.reader(file)
#             data = list(reader)
#         data[row_number][4] = int(data[row_number][4])
#         data[row_number][4] += 1
#         with open(path , 'w') as file:
#             writer = csv.writer(file)
#             writer.writerows(data)

# def check_if_book_in_csv(path , book):
#     with open(path , 'r') as file:
#         reader = csv.reader(file)
#         reader = list(reader)
#         for number_of_row , row in enumerate(reader):
#             if book == Book(row[0], row[1], row[2], row[3], row[4]):
#                 return True , number_of_row
#         return False , 0
