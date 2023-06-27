from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    name = 'Library "3 Books"'
    return render_template('enter.html', name=name)


if __name__ == '__main__':
    app.run()
