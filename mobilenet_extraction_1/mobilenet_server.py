from PIL import Image
import mobilenet_extractor as extractor
from datetime import datetime
from flask import Flask, request, render_template
import time


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

        #Extract
        startTime = time.time()
        extractedImg = extractor.extractImage(uploaded_img_path)
        extracttime = str((time.time() - startTime))
        #Linear Search
        startTime = time.time()
        scores = extractor.compareImages(extractedImg, feature_dir)
        searchtime = str((time.time() - startTime))
        

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores,
                               extracttime=extracttime,
                               searchtime=searchtime)
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")