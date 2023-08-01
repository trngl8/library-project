import re
import os

from flask import Flask, request, make_response, redirect, url_for, flash
from flask import render_template
from flask_bootstrap import Bootstrap5

from forms import OrderForm
from storage import DataStorage
from library import Library, Book
from processing import Processing
from validator import Validator

app = Flask(__name__)
app.secret_key = b'_57#y2L"F4hQ8z\n\xebc]/'

bootstrap = Bootstrap5(app)

library = Library("3 Books", DataStorage())


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        username = request.form["username"]
        if not re.match(r"[A-Za-z0-9_-]+", username):
            flash("Your name is not valid", category="error")
            return redirect(url_for("home"))
        resp = redirect(url_for('index'))
        resp.set_cookie("SERVER_COOKIE", username)
        return resp

    return render_template('enter.html', library=library)


@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['file']    
        if not os.path.exists(os.path.dirname(__file__) + "/var/import/"):
            os.makedirs(os.path.dirname(__file__) + "/var/import/")
        file.save(os.path.join("var/import/" + file.filename))
        return redirect(url_for("import_books", file_name=file.filename))
    user = request.cookies.get('SERVER_COOKIE')
    books = library.get_repository('books').find_all()
    resp = make_response(render_template('index.html', books=books, user=user, library=library))
    return resp


@app.route('/books/<int:book_id>')
def book(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    item = library.get_repository('books').find(book_id)
    resp = make_response(render_template('book.html', book=item, user=user, library=library))
    return resp


@app.route('/books/<int:book_id>/borrow', methods=["GET", "POST"])
def order(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    item = library.get_repository('books').find(book_id)
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        result = Processing().create_order(form)
        if result:
            flash('Thanks for order')
        else:
            flash("Processing failed", category="error")
        return redirect(url_for('confirm', book_id=book_id))
    resp = make_response(render_template('book_order.html', book=item, form=form, user=user, library=library))
    return resp


@app.route('/profile')
def profile():
    user = request.cookies.get('SERVER_COOKIE')
    return render_template("profile.html", user=user, library=library)

  
@app.route('/settings')
def settings():
    user = request.cookies.get('SERVER_COOKIE')
    return render_template("settings.html", user=user, library=library)

  
@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie('SERVER_COOKIE')
    return response

  
@app.route('/order/<int:book_id>/confirm', methods=["GET", "POST"])
def confirm(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    item = library.get_repository('books').find(book_id)
    return make_response(render_template('order_confirm.html', library=library, book=item, user=user))


@app.route('/books/import/<string:file_name>')
def import_books(file_name):
        with open(os.path.join("var/import/" + file_name)) as file:
            file_containment = file.readlines()
        result = []
        result.append(file_containment[0])
        flag = False
        validator = Validator()
        for line in file_containment[1:]:
            line = line.replace('\n', '').split(",")
            book = Book(int(line[0]), line[1], line[2], int(line[3]))
            if validator.validate(book=book):
                for j in result:
                    try:
                        if j == book:
                            flag = True
                    except:
                        continue
            if not flag:
                result.append(book)
            flag = False
        with open(os.path.join("var/import/" + file_name), 'w') as file:
            file.write(result[0])
            for i in result[1:]:
                file.write(str(i.id) + "," + i.title + ',' + i.author + ',' + str(i.year) + '\n')
        user = request.cookies.get('SERVER_COOKIE')
        books = library.get_repository('books').find_all()
        flash("Your file was imported successfully", category='success')
        resp = make_response(render_template('index.html', books=books, user=user, library=library))
        return resp


if __name__ == '__main__':
    app.run(debug=True)
