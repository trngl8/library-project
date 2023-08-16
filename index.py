import re
import dotenv
import os


from flask import Flask, request, make_response, redirect, url_for, flash
from flask import render_template
from flask import session
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename

from forms import OrderForm
from storage import DataStorage, FileLines
from library import Library
from processing import Processing
from file import FileImport


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
        return redirect(url_for('index'))

    return render_template('enter.html', library=library)


@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
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


@app.route('/books/<int:book_id>/borrow', methods=["GET", "POST"])
def order(book_id):
    item = library.get_repository('books').find(book_id)
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        result = Processing().create_order(form)
        if result:
            flash('Thanks for order')
        else:
            flash("Processing failed", category="error")
        return redirect(url_for('confirm', book_id=book_id))
    resp = make_response(render_template('book_order.html', book=item, form=form, library=library))
    return resp


@app.route('/orders/<int:order_id>/confirm', methods=["POST"])
def confirm_order(order_id):
    return {
        "status": "success"
    }

@app.route('/profile')
def profile():
    return render_template("profile.html", library=library)


@app.route('/settings')
def settings():
    return render_template("settings.html", library=library)


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('home')))
    return response


@app.route('/order/<int:book_id>/confirm', methods=["GET", "POST"])
def confirm(book_id):
    item = library.get_repository('books').find(book_id)
    return make_response(render_template('order_confirm.html', library=library, book=item))


@app.route('/cart', methods=["GET", "POST"])
def cart_index():
    cart = library.cart
    if request.method == 'POST':
        cart.clear()
        if 'cart' in session:
            session.pop('cart', None)
        flash("Cart cleared", category="success")
        return redirect(url_for('cart_index'))
    if 'cart' in session and 'items' in session['cart']:
        cart.clear()
        cart_data = session['cart']
        for item in cart_data['items']:
            cart.add_item(item)
    return make_response(render_template('cart.html', library=library, cart=cart))


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
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            import_service = FileImport(app.config['UPLOAD_FOLDER'])
            amount = import_service.process_file(file, filename)
            flash(f"Your file was imported successfully. {amount} unique books imported", category='success')
            return redirect(url_for('index'))
    user = request.cookies.get('SERVER_COOKIE')
    return render_template('import.html', library=library, user=user)


if __name__ == '__main__':
    app.run()
