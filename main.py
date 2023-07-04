from library import Library


def print_item(index, value):
    print(f"[{index + 1}]. {value}")


def print_exception_range(max_value):
    print(f"You should enter a number between 1 and {max_value}")


def find_book(library : Library):
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
        return  "This author has written the following books: " + str(list_for_author)
    if len(list_for_title) > 0:
        return "There are the following books with this title: " + str(list_for_title)
    return "There is no books currently available with this title, author or ISBN"


def find_user():
    pass


def import_books():
    filename = input("Enter filename :> ")
    # TODO: implement import behavior
    count = 0
    return f"Imported {count} books"


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
