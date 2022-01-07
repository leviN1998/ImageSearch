import time
from datetime import datetime

from PIL import Image
from flask import Flask, request, render_template

import mobilenet_extractor as mobilenet_extractor
import vgg16_extractor as vgg16_extractor
import mobilenetv2_extractor as mobilenetv2_extractor
import nasnet_extractor as nasnet_extractor
import xception_extractor as xception_extractor

app = Flask(__name__)

mobilenet_feature_dir = "./static/features/m_features/cifar10_200/"
vgg16_feature_dir = "./static/features/vgg16_features/cifar10_200/"
mobilenetv2_feature_dir = "./static/features/m2_features/cifar10_200/"
nasnet_feature_dir = "./static/features/nasnet_features/cifar10_200/"
xception_feature_dir = "./static/features/xception_features/cifar10_200/"


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


@app.route('/mobilenetv2', methods=['POST', 'GET'])
def mobilenetv2():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        startTime = time.time()
        extractedImg = mobilenetv2_extractor.extractImage(uploaded_img_path)
        scores = mobilenetv2_extractor.compareImages(extractedImg, mobilenetv2_feature_dir)
        t = str((time.time() - startTime))

        return render_template('mobilenetv2.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('mobilenetv2.html')


@app.route('/nasnet', methods=['POST', 'GET'])
def nasnet():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        startTime = time.time()
        extractedImg = nasnet_extractor.extractImage(uploaded_img_path)
        scores = nasnet_extractor.compareImages(extractedImg, nasnet_feature_dir)
        t = str((time.time() - startTime))

        return render_template('nasnet.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('nasnet.html')


@app.route('/xception', methods=['POST', 'GET'])
def xception():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        startTime = time.time()
        extractedImg = xception_extractor.extractImage(uploaded_img_path)
        scores = xception_extractor.compareImages(extractedImg, xception_feature_dir)
        t = str((time.time() - startTime))

        return render_template('xception.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('xception.html')


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
        extractedImg = vgg16_extractor.extractImg(uploaded_img_path)
        t = str((time.time() - startTime))
        scores = vgg16_extractor.compareImages(extractedImg, vgg16_feature_dir)

        return render_template('vgg16.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)

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
