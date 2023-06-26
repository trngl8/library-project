from library import Library
from library import User
from library import Book

# TODO: import from csv file
library = Library()
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




