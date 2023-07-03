from library import *


def print_item(index, value):
    print(f"[{index + 1}]. {value}")


def print_exception_range(max_value):
    print(f"You should enter a number between 1 and {max_value}")


def find_book():
    pass


def find_user():
    pass


def import_books(library : Library):
    filename = input("Enter filename :> ")
    library.import_books(library.read_from_csv_catalog(filename)[0])
    return f"Imported {library.read_from_csv_catalog(filename)[1]} books"


actions = {
    "Find a book": find_book,
    "Find a user": find_user,
    "Import books": import_books,
}

menu = list(actions.keys())
choice = 0
while choice == 0:
    for i, item in enumerate(menu):
        print_item(i, item)

    try:
        choice = int(input("Enter your choice :> "))
    except ValueError:
        print_exception_range(len(menu))

    if choice < 1 or choice > len(menu):
        print_exception_range(len(menu))
        choice = 0

function = actions.get(menu[choice - 1])
print(function())
