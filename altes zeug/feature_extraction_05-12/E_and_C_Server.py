import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
import vgg16_extractor as extractor
import Extraction_and_Comparison as ec
import time

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
        
        extractedImg = extractor.extractImg(uploaded_img_path, feature_dir)
        
        # Run distance search 
        startTime = time.time()
        scores = extractor.compareImages(extractedImg, feature_dir) #scores[0] is feature, scores[1] is img path
        distanceTime = str((time.time() - startTime))
        #run lhs search
        startTime = time.time()
        lhs_results = ec.similiarImgPaths(extractedImg, feature_dir) #list of paths of sim images
        lhsTime = str((time.time() - startTime))

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               lhs_results = lhs_results,
                               distanceTime = distanceTime,
                               lhsTime = lhsTime
                               )
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")