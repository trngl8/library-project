
library = Library()
book1 = Book("Python Crash Course")
book2 = Book("Learn Python Hard Way")
book3 = Book("Head First Python")

library.addBook(book1)
library.addBook(book2)
library.addBook(book3)

user = User()

user.register(library)
user.askOrder(book1)
user.borrow(book1)

library.check()
library.sendLetters()

user.release(book1)
user.askOrder(book2)
user.borrow(book2)




