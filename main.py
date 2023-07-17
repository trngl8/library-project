from library import Library
from library import User
from functions import save_user

def print_item(index, value):
    print(f"[{index + 1}]. {value}")


def print_exception_range(max_value):
    print(f"You should enter a number between 1 and {max_value}")


def find_book(library: Library):
    to_find = str(input("Enter title, author or ISBN "))
    list_for_author = []
    list_for_title = []
    for i in library.catalog:
        if i.title == to_find and i.available is True:
            list_for_title.append(i)
        if i.author == to_find and i.available is True:
            list_for_author.append(i)
        if i.isbn == to_find and i.available is True:
            return "There is an available book with such isbn"
    if len(list_for_author) > 0:
        return "This author has written the following books: " + str(list_for_author)
    if len(list_for_title) > 0:
        return "There are the following books with this title: " + str(list_for_title)
    return "There is no books currently available with this title, author or ISBN"


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
    filename = input("Enter filename :> ")
    filename = "var/data/" + filename
    list_of_books = library.read_from_csv_catalog(filename)
    number_of_imported_books = len(list_of_books)
    library.import_books(list_of_books)
    return f"Imported {number_of_imported_books} books"


def add_user(library: Library):
    name = input("Name :> ")
    email = input("Email :> ")
    phone = input("Phone :> ")
    user = User(name, email, phone)
    library.add_user(user)
    save_user(user)
    return f"User {name} added"


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
}

menu = list(menu_actions.keys())
menu_active = True
main_library = Library()

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
