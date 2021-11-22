from flask import Flask, request, render_template, url_for


app = Flask(__name__)


@app.route('/')
def first():
    return render_template('first_page.html')

@app.route('/1')
def test():
    return render_template('base.html')


@app.route('/2')
def second():
    return render_template('second_page.html')


@app.route('/3')
def third():
    return render_template('third_page.html')


if __name__ == "__main__":
    app.run(debug=True)
