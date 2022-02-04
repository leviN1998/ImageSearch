import imp
import time
from datetime import datetime

from PIL import Image
from flask import Flask, request, render_template

import ImageCrawling
from ImageCrawling import extractors
import extractors_alt as extractors_alt
from ImageCrawling import feature_interface
from ImageCrawling import toolbox
import io

app = Flask(__name__)

# set feature directories
mobilenet_feature_dir = "./static/features/m_features/cifar10_200/"
vgg16_feature_dir = "./static/features/vgg16_features/cifar10_200/"
mobilenetv2_feature_dir = "./static/features/m2_features/cifar10_200/"
nasnet_feature_dir = "./static/features/nasnet_features/cifar10_200/"
xception_feature_dir = "./static/features/xception_features/cifar10_200/"

# instanciate extractors
mobilenet_extractor = extractors.MobileNet()
mobilenetv2_extractor = extractors.MobileNetV2()
vgg16_extractor = extractors.VGG16Extractor()
nasnet_extractor = extractors.NasNet()
xception_extractor = extractors.Xception()


@app.route('/test', methods=['POST', 'GET'])
def test1():
    if request.method == 'POST':
        file = request.files['query_img']
        search_algorithm = request.form.get('search')
	
        if(search_algorithm == 'hashing' ):
            checked = 'hashing'
            #results = ...
            img = Image.open(file.stream).convert("RGB")  # PIL image
            feature = mobilenet_extractor.extractImage(img)
            uploaded_img = toolbox.image_to_base64(img)

            image = toolbox.image_to_binary(img)
            startTime = time.time()

            results = ImageCrawling.get_nearest_images_2("final.db", image, "big", "mobile_net", feature, count=30)

            t = str((time.time() - startTime))
            checked = 'euklid'
        
        else: #lineare Suche
        
            img = Image.open(file.stream).convert("RGB")  # PIL image
            uploaded_img = toolbox.image_to_base64(img)

            image = toolbox.image_to_binary(img)
            startTime = time.time()
            results = ImageCrawling.get_nearest_images("light_database.db",
                                                    image,
                                                    "cifar10",
                                                    "mobileNet",
                                                    mobilenet_extractor.extractImage(img), #feature
                                                    count=30)
            t = str((time.time() - startTime))
            checked = 'euklid'

        return render_template('test.html', query_img=uploaded_img, checked = checked, scores=results, t=t)
    else:
        return render_template('algorithm.html', extractor="MobileNet", checked = '' )


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
        extractedImg = mobilenet_extractor.extractImage_by_path(uploaded_img_path)
        scores = mobilenet_extractor.linearSearch(extractedImg, mobilenet_feature_dir)
        t = str((time.time() - startTime))

        return render_template('algorithm.html',
                               extractor="MobileNet",
                               query_path=uploaded_img_path,
                               checked = '',
                               scores=scores,
                               t=t)
    else:
        return render_template('algorithm.html', extractor="MobileNet", checked = '' )


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
        extractedImg = mobilenetv2_extractor.extractImage_by_path(uploaded_img_path)
        scores = mobilenetv2_extractor.linearSearch(extractedImg, mobilenetv2_feature_dir)
        t = str((time.time() - startTime))

        return render_template('algorithm.html',
                               extractor="MobileNet Version 2",
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('algorithm.html', extractor="MobileNet Version 2", )


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
        extractedImg = nasnet_extractor.extractImage_by_path(uploaded_img_path)
        scores = nasnet_extractor.linearSearch(extractedImg, nasnet_feature_dir)
        t = str((time.time() - startTime))

        return render_template('algorithm.html',
                               extractor="NasNet",
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('algorithm.html', extractor="NasNet", )


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
        extractedImg = xception_extractor.extractImage_by_path(uploaded_img_path)
        scores = xception_extractor.linearSearch(extractedImg, xception_feature_dir)
        t = str((time.time() - startTime))

        return render_template('algorithm.html',
                               extractor="Xception",
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)
    else:
        return render_template('algorithm.html', extractor="Xception", )


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
        extractedImg = vgg16_extractor.extractImage_by_path(uploaded_img_path)
        t = str((time.time() - startTime))
        scores = vgg16_extractor.linearSearch(extractedImg, vgg16_feature_dir)

        return render_template('algorithm.html',
                               extractor="VGG16",
                               query_path=uploaded_img_path,
                               scores=scores,
                               t=t)

    else:
        return render_template('algorithm.html', extractor="VGG16", )


@app.route('/')
def second():
    return render_template('home.html')


@app.route('/impressum')
def third():
    return render_template('impressum.html')


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='134.2.56.169')
