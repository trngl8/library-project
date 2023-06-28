from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    name = 'Library "3 Books"'
    return render_template('enter.html', name=name)


if __name__ == '__main__':
    app.run()
