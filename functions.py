from library import Book
import csv


def add_book_to_csv(book: Book, path):
    if not check_if_book_in_csv(path=path, book=book)[0]:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        data.append([book.title, book.author, book.year, book.available, book.count])
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
