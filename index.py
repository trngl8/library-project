from flask import Flask, request, make_response, redirect, url_for, flash
from flask import render_template
from flask_bootstrap import Bootstrap5
from wtforms import Form, BooleanField, StringField, EmailField, SelectField, validators
import re

from library import Library

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

bootstrap = Bootstrap5(app)


class OrderForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=4, max=25)])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25)])
    email = EmailField('Email', [validators.Email()])
    phone = StringField('Phone', [validators.Length(min=6, max=11)])
    address = StringField('Address', [validators.Length(min=6, max=35)])
    period = SelectField('Period', choices=[('2', '2 weeks'), ('4', '4 weeks'), ('16', '16 weeks')])
    accept = BooleanField('I accept agreement', [validators.DataRequired()])


@app.route('/')
def index():
    library = Library("3 Books", "var/data")
    return render_template('enter.html', library=library)


@app.route('/index')
def catalog():
    user = request.cookies.get('SERVER_COOKIE')
    library = Library("3 Books", "var/data")
    books = library.catalog
    resp = make_response(render_template('index.html', books=books, user=user))
    return resp


@app.route('/enter', methods=["POST"])
def enter():
    user = request.form["username"]
    if not re.match(r"[A-Za-z0-9_-]+", user):
        flash("Your name is not valid" , category="error")
        return redirect(url_for("index"))
    resp = redirect(url_for('catalog'))
    resp.set_cookie("SERVER_COOKIE", user)
    return resp


@app.route('/books/<int:book_id>')
def book(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    library = Library("3 Books", "var/data")
    item = library.find_book(book_id)
    resp = make_response(render_template('book.html', book=item, user=user))
    return resp


@app.route('/books/<int:book_id>/borrow', methods=["GET", "POST"])
def order(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    library = Library("3 Books", "var/data")
    item = library.find_book(book_id)
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Thanks for order')
        return redirect(url_for('confirm', book_id=book_id))

    resp = make_response(render_template('book_order.html', book=item, form=form, user=user))
    return resp


@app.route('/order/<int:book_id>/confirm', methods=["GET", "POST"])
def confirm(book_id):
    user = request.cookies.get('SERVER_COOKIE')
    library = Library("3 Books", "var/data")
    item = library.find_book(book_id)

    return make_response(render_template('order_confirm.html', book=item, user=user))


if __name__ == '__main__':
    app.run()
