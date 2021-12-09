import numpy as np
from PIL import Image
import mobilenet_extractor as extractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
import time


app = Flask(__name__)


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
        startTime = time.time()
        extractedImg = extractor.extractImage(uploaded_img_path)
        scores = extractor.compareImages(extractedImg, feature_dir)
        t = str((time.time() - startTime))
        

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               time=t)
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")