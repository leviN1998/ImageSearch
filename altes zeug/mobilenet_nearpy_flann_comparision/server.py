from re import search
from PIL import Image
import mobilenet_extractor as mobilenet_extractor
from datetime import datetime
from flask import Flask, request, render_template
import time
import nearpy
import pyflann as flann
import search_algorithms 


app = Flask(__name__)


feature_dir = "./static/features/"

#load lsh_engine once with dimenstions for mobilenet
lsh_engine = search_algorithms.create_lsh_engine(1024, 8)

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
        scores = search_algorithms.compareImages(extractedImg, feature_dir)
        #scores = mobilenet_extractor.compareImages(extractedImg, feature_dir)
        linearTime = str((time.time() - startTime))
        
        #Nearpy Search
        startTime = time.time()
        nearpy_results = search_algorithms.lsh(extractedImg, feature_dir, lsh_engine) 
        nearpyTime = str((time.time() - startTime))

        #Flann Search
        startTime = time.time()
        #flann_results = search_algorithms.kmeans(extractedImg, feature_dir)
        flannTime = str((time.time() - startTime))

        
        return render_template('index.html',
                               query_path=uploaded_img_path,
                               extractTime = extractTime,
                               scores=scores,
                               linearTime = linearTime,
                               nearpy_results = nearpy_results,
                               nearpyTime = nearpyTime,
                               flann_results = nearpy_results,
                               flannTime = flannTime)
                        
    else:
        return render_template('index.html')


if __name__=="__main__":
    
    app.run("0.0.0.0")