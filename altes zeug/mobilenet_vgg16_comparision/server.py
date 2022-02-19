from re import search
from PIL import Image
import mobilenet_extractor as mobilenet_extractor
import vgg16_extractor as vgg16_extractor
from datetime import datetime
from flask import Flask, request, render_template
import time


app = Flask(__name__)


mobilenet_feature_dir = "./static/m_features/"
vgg16_feature_dir = "./static/vgg16_features/"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        #Save query image
        img = Image.open(file.stream)  #PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        #Extract using mobilenet
        startTime = time.time()
        extractedImg = mobilenet_extractor.extractImage(uploaded_img_path)
        mobilenetTime = str((time.time() - startTime))

        mobilenet_results = mobilenet_extractor.compareImages(extractedImg, mobilenet_feature_dir)
        
        #Extract using vgg16
        startTime = time.time()
        vgg_extractedImg = vgg16_extractor.extractImg(uploaded_img_path)
        vgg16Time = str((time.time() - startTime))

        vgg16_results = vgg16_extractor.compareImages(vgg_extractedImg, vgg16_feature_dir)

        
        return render_template('index.html',
                               query_path=uploaded_img_path,
                               mobilenet_results = mobilenet_results,
                               mobilenetTime = mobilenetTime,
                               vgg16_results = vgg16_results,
                               vgg16Time = vgg16Time)
                        
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")