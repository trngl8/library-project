from flask import Flask, request, make_response, redirect, url_for
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
    user = request.cookies.get('SERVER_COOKIE')
    name = 'Library "3 Books"'
    library = Library()
    library.import_books(library.read_from_csv_catalog("var/data/books.csv"))
    books = library.catalog
    resp = make_response(render_template('index.html', name=name, books=books, user=user))
    return resp


@app.route('/enter', methods=["POST"])
def enter():
    user = request.form["username"]
    resp = redirect(url_for('catalog'))
    resp.set_cookie("SERVER_COOKIE", user)

    return resp


@app.route('/books/<int:book_id>')
def book(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    name = 'Library "3 Books"'
    library = Library()
    library.import_books(library.read_from_csv_catalog("var/data/books.csv"))
    item = library.find_book(book_id)
    resp = make_response(render_template('book.html', name=name, book=item, user=user))
    return resp


@app.route('/profile')
def profile():
    user = request.cookies.get('SERVER_COOKIE')
    books = user.books
    return render_template("profile.html", books=books, user=user)

@app.route('/settings')
def settings():
    user = request.cookies.get('SERVER_COOKIE')
    return render_template("settings.html", user=user)

@app.route("/logout")
def logout():
    return render_template("enter.html")

if __name__ == '__main__':
    app.run()
