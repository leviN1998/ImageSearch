import time
from datetime import datetime

from PIL import Image
from flask import Flask, request, render_template

import mobilenet_extractor as extractor

app = Flask(__name__)

feature_dir = "./static/mobilenet_features/"


@app.route('/', methods=['POST', 'GET'])
def first():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        startTime = time.time()
        extractedImg = extractor.extractImage(uploaded_img_path)
        scores = extractor.compareImages(extractedImg, feature_dir)
        t = str((time.time() - startTime))

        return render_template('home.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('home.html')


@app.route('/1')
def test():
    return render_template('test.html')


@app.route('/2')
def second():
    return render_template('algorithm.html')


@app.route('/3')
def third():
    return render_template('impressum.html')


if __name__ == "__main__":
    app.run(debug=True)
