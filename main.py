form library import Library
from library import User
from library import Book

library = Library()
book1 = Book("Python Crash Course")
book2 = Book("Learn Python Hard Way")
book3 = Book("Head First Python")

library.addBook(book1)
library.addBook(book2)
library.addBook(book3)

user = User()

user.register(library)
user.ask_order(book1)
user.borrow(book1)

library.check()
library.send_letters()

user.release(book1)
user.ask_order(book2)
user.borrow(book2)




