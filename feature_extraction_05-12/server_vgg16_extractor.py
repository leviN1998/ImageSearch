import numpy as np
from PIL import Image
import vgg16_extractor as extractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path

app = Flask(__name__)

#img_dir = "./static/image_set_1/"
feature_dir = "./static/features/"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        extractedImg = extractor.extractImg(uploaded_img_path, feature_dir)
        scores = extractor.compareImages(extractedImg, feature_dir)
        

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")