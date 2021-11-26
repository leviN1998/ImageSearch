from flask import Flask, request, render_template, url_for


app = Flask(__name__)


@app.route('/')
def first():
    return render_template('home.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/algorithm')
def second():
    return render_template('algorithm.html')


@app.route('/impressum')
def third():
    return render_template('impressum.html')


if __name__ == "__main__":
    app.run(debug=True)
