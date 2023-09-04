from library import Library
from library import User
from storage import DataStorage, FileLines
from file import FileImport
from validator import Validator, Required, Length
from error import DatabaseError


def print_item(index, value):
    print(f"[{index + 1}]. {value}")


def print_exception_range(max_value):
    print(f"You should enter a number between 1 and {max_value}")


def find_books(library: Library) -> str:
    title = input("Enter title :> ")
    author = input("Enter author :> ")
    year = input("Enter year :> ")
    isbn = input("Enter ISBN :> ")
    result = library.find_books(title=title, author=author, year=year, isbn=isbn)
    return f"{len(result)} books found"


def find_user():
    pass


def import_books(library: Library):
    importer = FileImport('var/import/')
    for i in importer.get_dir_files('var/import/'):
        print(i.split('/')[-1])
    new_file = input('Enter one of filenames from above: ')
    result = importer.import_file(new_file, library)
    return f"{result} books have been imported"


def add_user(library: Library):
    name = input("Name :> ")
    email = input("Email :> ")
    phone = input("Phone :> ")
    library.add_user(zip(name, email, phone))
    return f"User {name} added"


def add_book(library: Library):
    book_item = {
        'title': input("Title :> "),
        'author': input("Author :> "),
        'year': input("Year :> ")
    }
    validator = Validator()
    validator.add({
        'title': [Required()],
        'author': [Required()],
        'year': [Required(), Length(4, 4)]
    })
    if not validator.validate(book_item):
        return f"Invalid data {validator.errors}"
    try:
        result = library.get_repository('books').add(book_item)
        return f"Book added with ID {result}"
    except DatabaseError as e:
        return f"Database error: {e.message}"


def remove_book(library: Library):
    book_id = input("Enter book ID :> ")
    library.remove_book(book_id)
    return f"Book with ID {book_id} removed"


def get_choice_function(actions, param=None):
    return actions.get(param, lambda val: val)


def menu_choice(library: Library, actions, choice):
    choice_function = get_choice_function(actions, list(actions.keys())[choice - 1])
    return choice_function(library)


menu_actions = {
    "Find a book": find_books,
    "Find a user": find_user,
    "Import books": import_books,
    "Add user": add_user,
    "Add book": add_book,
    "Remove book": remove_book,
}

menu = list(menu_actions.keys())
menu_active = True
main_library = Library('3 Books', DataStorage(FileLines()))

while menu_active:
    print("#" * 40)
    for i, item in enumerate(menu):
        print_item(i, item)

    user_choice = 0

    try:
        user_choice = int(input("Enter your choice :> "))
    except ValueError:
        print_exception_range(len(menu))

    if user_choice < 1 or user_choice > len(menu):
        print_exception_range(len(menu))
        menu_active = False
    else:
        print(menu_choice(main_library, menu_actions, user_choice))
        input("Press any key to continue... ")
