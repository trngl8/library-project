from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5

from library import Library
from library import Book

app = Flask(__name__)

bootstrap = Bootstrap5(app)


@app.route('/')
def index():
    name = 'Library "3 Books"'
    return render_template('enter.html', name=name)


@app.route('/index')
def catalog():
    name = 'Library "3 Books"'
    library = Library()
    library.add_book(Book("Python Crash Course", "Eric Matthes", 2019))
    library.add_book(Book("Python Hard Way", "Zed Shaw", 2013))
    library.add_book(Book("Head First Python", "Paul Barry", 2016))
    books = library.catalog
    return render_template('index.html', name=name, books=books)


if __name__ == '__main__':
    app.run()
