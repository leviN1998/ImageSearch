from flask import Flask, request, render_template, url_for, redirect
from PIL import Image
import vgg16_extractor as extractor
from datetime import datetime


app = Flask(__name__)

feature_dir = "./static/features/"


@app.route('/', methods=['POST', 'GET'])
def first():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        extractedImg = extractor.extractImg(uploaded_img_path, feature_dir)
        scores = extractor.compareImages(extractedImg, feature_dir)

        return render_template('home.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
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
