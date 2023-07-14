from library import Library
from library import User
from library import Book
import csv


def add_book_to_csv(book: Book, path):
    if not check_if_book_in_csv(path=path, book=book)[0]:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        data.append([book.title, book.author, \
                     book.year, book.available, book.count])
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    elif check_if_book_in_csv(path=path, book=book)[0]:
        row_number = check_if_book_in_csv(path=path, book=book)[1]
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        data[row_number][5] = int(data[row_number][5])
        data[row_number][5] += 1
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)


def check_if_book_in_csv(path, book):
    with open(path, 'r') as file:
        reader = csv.reader(file)
        reader = list(reader)
        for number_of_row, row in enumerate(reader):
            if book == Book(row[0], row[1], row[2], row[3]):
                return True, number_of_row
        return False, 0


def save_user(user: User):
    with open("var/data/users.csv", "r") as file:
        data = list(csv.reader(file))
    data.append([user.name, user.email, user.phone, user.wanted_amount])
    with open("var/data/users.csv", 'w') as file:
        csv.writer(file).writerows(data)


def temp():
    file = open("books.csv", "r")
    lines = file.readlines()

    library = Library()

    for line in lines:
        line = line.strip()
        book1 = Book(line[1])
        library.add_book(book1)
        print(line)

    file.close()

    book1 = Book("Python Crash Course")
    book2 = Book("Learn Python Hard Way")
    book3 = Book("Head First Python")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    user = User()

    user.register(library)
    user.ask_order(book1)
    user.borrow(book1)

    library.check()
    library.send_letters()

    user.release(book1)
    user.ask_order(book2)
    user.borrow(book2)
