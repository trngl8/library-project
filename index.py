import re
import dotenv
import os
import datetime

from flask import Flask, request, make_response, redirect, url_for, flash
from flask import render_template
from flask import session
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename

from forms import OrderForm, BookEditForm, BookRemoveForm, NewNameForm
from storage import DataStorage, FileLines
from library import Library
from processing import Processing
from file import FileImport
from error import DatabaseError

UPLOAD_FOLDER = 'var/import/'
ALLOWED_EXTENSIONS = {'csv', 'tsv'}

dotenv.load_dotenv()
dotenv.load_dotenv('.env.local', override=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ADMIN_PERMISSION'] = os.getenv("ADMINISTRATOR_EMAIL")
app.secret_key = b'_57#y2L"F4hQ8z\n\xebc]/'

bootstrap = Bootstrap5(app)

library = Library("3 Books", DataStorage(FileLines()))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        username = request.form["username"]
        if not re.match(r"[A-Za-z0-9_-]+", username):
            flash("Your name is not valid", category="error")
            return redirect(url_for("home"))
        session['username'] = username
        try:
            library.get_repository('users').add({
                'email': username,
                'name': username,
                'date': datetime.date,
                'ip_address': request.remote_addr,
                'user_agent': request.user_agent
            })
        except DatabaseError:
            flash("Can not add user", category="error")
        return redirect(url_for('index'))

    return render_template('enter.html', library=library)


@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', category="error")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            import_service = FileImport(app.config['UPLOAD_FOLDER'])
            amount = import_service.process_file(file, filename, library=library)
            flash(f"Your file was imported successfully. {amount} unique books imported", category='success')
            return redirect(url_for('index'))
    books = library.get_repository('books').find_all()
    resp = make_response(render_template('index.html', books=books, library=library))
    return resp


@app.route('/books/<int:book_id>')
def book(book_id):
    item = library.get_repository('books').find(book_id)
    resp = make_response(render_template('book.html', book=item, library=library))
    return resp


@app.route('/books/<int:book_id>/edit', methods=["GET", "POST"])
def book_edit(book_id):
    item = library.get_repository('books').find(book_id)
    form = BookEditForm(request.form, obj=item)
    if request.method == 'POST' and form.validate():
        try:
            result = library.get_repository('books').update(book_id, {
                'title': form.title.data,
                'author': form.author.data,
                'year': form.year.data
            })
        except DatabaseError:
            flash(f"Cannot update item {book_id}", category='error')
            return redirect(url_for('book', book_id=book_id))
        flash('Updated success', category='success')
        return redirect(url_for('book', book_id=book_id))
    return make_response(render_template('book_edit.html', book=item, form=form, library=library))


@app.route('/books/<int:book_id>/remove', methods=["GET", "POST"])
def book_remove(book_id):
    item = library.get_repository('books').find(book_id)
    form = BookRemoveForm(request.form, obj=item)
    if request.method == 'POST' and form.validate():
        try:
            library.get_repository('books').remove(book_id)
        except Exception:
            flash(f"Cannot remove item {book_id}", category='error')
            return redirect(url_for('book', book_id=book_id))
    flash('Removed success', category='success')
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    return render_template("profile.html", library=library)


@app.route('/settings', methods=["GET", "POST"])
def settings():
    form = NewNameForm(request.form)
    if request.method == 'POST' and form.validate():
        flash("Your name was successfully changed", category="success")
        session['username'] = form.newname.data
    return render_template("settings.html", library=library, form=form)


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('home')))
    return response


@app.route('/cart', methods=["GET", "POST"])
def cart_index():
    cart = library.cart

    if 'cart' in session and 'items' in session['cart']:
        cart.clear()
        cart_data = session['cart']
        for item in cart_data['items']:
            cart.add_item(item)

    if request.method == 'POST':
        if request.form.get('clear'):
            cart.clear()
            if 'cart' in session:
                session.pop('cart', None)
            flash("Cart cleared", category="success")
            return redirect(url_for('cart_index'))
        else:
            if 'cart' in session:
                # TODO: write cart into session or (and) into database
                cart_data = session['cart']
                for item in cart_data['items']:
                    cart.add_item(item)
                return redirect(url_for('cart_order'))
    return make_response(render_template('cart.html', library=library, cart=cart))


@app.route('/cart/order', methods=["GET", "POST"])
def cart_order():
    cart = library.cart
    if 'cart' in session and 'items' in session['cart']:
        cart.clear()
        cart_data = session['cart']
        for item in cart_data['items']:
            cart.add_item(item)

    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        order_id = library.get_repository('orders').add({
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'address': form.address.data,
            'period': form.period.data
        })
        for item in library.cart.items:
            library.get_repository('books_orders').add({
                'book_id': str(item['id']),
                'order_id': str(order_id),
            })
        result = Processing().send_order(form)
        if result:
            cart.clear()
            if 'cart' in session:
                session.pop('cart', None)
            flash('Thanks for order', category="success")
        else:
            flash("Processing failed", category="error")
        return redirect(url_for('order_confirm', order_id=order_id))
    return render_template('cart_order.html', form=form, library=library, cart=cart)


@app.route('/order/<int:order_id>/confirm', methods=["GET", "POST"])
def order_confirm(order_id):
    order_item = library.get_repository('orders').find(order_id)
    return make_response(render_template('order_confirm.html', library=library, order=order_item))


@app.route('/cart/<int:book_id>/add', methods=["POST"])
def add_to_cart(book_id):
    if 'cart' not in session:
        cart_data = {
            "count_items": 0,
            "items": []
        }
    else:
        cart_data = session['cart']

    book = library.get_repository('books').find(book_id)

    ids = [item['id'] for item in cart_data['items']]
    if book.id not in ids:
        cart_data['items'].append({'id': book.id, 'title': book.title})
        cart_data['count_items'] = len(cart_data['items'])
        session['cart'] = cart_data

    return {
        "result": cart_data['count_items'],
    }


@app.route('/cart/<int:book_id>/remove', methods=["POST"])
def remove_from_cart(book_id):
    book = library.get_repository('books').find(book_id)
    if 'cart' not in session:
        cart_data = {
            "count_items": 0,
            "items": []
        }
    else:
        cart_data = session['cart']

    for item in cart_data['items']:
        if item['id'] == book.id:
            cart_data['items'].remove(item)
            break
    cart_data['count_items'] = len(cart_data['items'])
    session['cart'] = cart_data

    return {
        "result": cart_data['count_items'],
    }


@app.route('/import', methods=["GET", "POST"])
def import_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', category="error")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            import_service = FileImport(app.config['UPLOAD_FOLDER'])
            amount = import_service.process_file(file, filename)
            flash(f"Your file was imported successfully. {amount} unique books imported", category='warning')
            return redirect(url_for('index'))
    user = request.cookies.get('SERVER_COOKIE')
    return render_template('import.html', library=library, user=user)


@app.route('/orders/<int:order_id>/confirm', methods=["POST"])
def confirm_order(order_id):
    return {
        "id": order_id,
        "status": "success"
    }


if __name__ == '__main__':
    app.run()
