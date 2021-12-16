from re import search
from PIL import Image
import mobilenet_extractor as mobilenet_extractor
from datetime import datetime
from flask import Flask, request, render_template
import time
import Nearpy_Mobilenet as nearpy
import flann as flann


app = Flask(__name__)


feature_dir = "./static/features/"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        #Save query image
        img = Image.open(file.stream)  #PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        #Extract using mobile net
        startTime = time.time()
        extractedImg = mobilenet_extractor.extractImage(uploaded_img_path)
        extractTime = str((time.time() - startTime))

        #Linear Search
        startTime = time.time()
        scores = mobilenet_extractor.compareImages(extractedImg, feature_dir)
        linearTime = str((time.time() - startTime))
        
        #Nearpy Search
        startTime = time.time()
        nearpy_results = nearpy.lsh(1024, extractedImg, feature_dir, 10)
        nearpyTime = str((time.time() - startTime))

        #Flann Search
        startTime = time.time()
        flann_results = flann.similiarImgPaths(extractedImg, feature_dir)
        flannTime = str((time.time() - startTime))

        
        return render_template('index.html',
                               query_path=uploaded_img_path,
                               extractTime = extractTime,
                               scores=scores,
                               linearTime = linearTime,
                               nearpy_results = nearpy_results,
                               nearpyTime = nearpyTime,
                               flann_results = flann_results,
                               flannTime = flannTime)
                        
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")