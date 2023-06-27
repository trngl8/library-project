from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Library "3 Books"</h1>'


if __name__ == '__main__':
    app.run()
