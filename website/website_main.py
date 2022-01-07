import time
from datetime import datetime

from PIL import Image
from flask import Flask, request, render_template

import mobilenet_extractor as mobilenet_extractor
import vgg16_extractor as vgg16_extractor


app = Flask(__name__)

mobilenet_feature_dir = "./static/mobilenet_features/"
vgg16_feature_dir = "./static/vgg16_feature/"


@app.route('/mobilenet', methods=['POST', 'GET'])
def first():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        startTime = time.time()
        extractedImg = mobilenet_extractor.extractImage(uploaded_img_path)
        scores = mobilenet_extractor.compareImages(extractedImg, mobilenet_feature_dir)
        t = str((time.time() - startTime))

        return render_template('mobilenet.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('mobilenet.html')


@app.route('/vgg16', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Extract using vgg16
        startTime = time.time()
        vgg_extractedImg = vgg16_extractor.extractImg(uploaded_img_path)
        vgg16Time = str((time.time() - startTime))

        vgg16_results = vgg16_extractor.compareImages(vgg_extractedImg, vgg16_feature_dir)

        return render_template('vgg16.html',
                               query_path=uploaded_img_path,
                               vgg16_results=vgg16_results,
                               vgg16Time=vgg16Time)

    else:
        return render_template('vgg16.html')


@app.route('/')
def second():
    return render_template('home.html')


@app.route('/impressum')
def third():
    return render_template('impressum.html')


if __name__ == "__main__":
    app.run(debug=True)
