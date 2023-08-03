import re

from flask import Flask, request, make_response, redirect, url_for, flash
from flask import render_template
from flask import session
from flask_bootstrap import Bootstrap5

from forms import OrderForm
from storage import DataStorage
from library import Library
from library import Cart
from processing import Processing

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


@app.route('/index')
def index():
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


@app.route('/cart', methods=["GET", "POST"])
def cart_index():
    user = request.cookies.get('SERVER_COOKIE')
    if request.method == 'POST':
        cart = library.cart
        cart.clear()
        if 'cart' in session:
            session.pop('cart', None)

    return make_response(render_template('cart.html', library=library, user=user))


@app.route('/cart/<int:book_id>/add', methods=["POST"])
def add_to_cart(book_id):
    cart = library.cart
    item = library.get_repository('books').find(book_id)
    cart.add_item(item)
    session['cart'] = {
        "count_items": len(cart.items),
    }

    return {
        "result": len(cart.items),
    }


if __name__ == '__main__':
    app.run()
