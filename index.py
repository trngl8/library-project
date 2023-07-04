from flask import Flask, request, make_response
from flask import render_template
from flask_bootstrap import Bootstrap5

from library import Library

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
    library.import_books(library.read_from_csv_catalog("var/data/books.csv"))

    books = library.catalog
    return render_template('index.html', name=name, books=books)

@app.route('/enter' , methods = ["POST", "GET"])
def enter():
    if request.method == "POST":
        user = request.form["nm"]
        resp = make_response(render_template("readcookie.html"))
        resp.set_cookie("userID", user)

        return resp

@app.route("/getcookie")
def getcookie():
    name = request.cookies.get("userID")
    return '<h1>welcome ' + name + '</h1>'

@app.route('/books/<int:book_id>')
def book(book_id):
    name = 'Library "3 Books"'
    library = Library()
    library.import_books(library.read_from_csv_catalog("var/data/books.csv"))
    item = library.find_book(book_id)
    return render_template('book.html', name=name, book=item)


if __name__ == '__main__':
    app.run()
