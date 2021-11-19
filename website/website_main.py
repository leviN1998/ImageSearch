import os
from flask import Flask, request, render_template, url_for

app = Flask(__name__)


@app.route('/picture')
def index():
    return render_template('index.html')


@app.route('/first page')
def first():
    return 'this is the first page'


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello_world.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'accepted'
    else:
        return 'rejected'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


if __name__ == "__main__":
    app.run(debug=True)
