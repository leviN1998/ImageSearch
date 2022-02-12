import time
from datetime import datetime

from PIL import Image
from flask import Flask, request, render_template

import ImageCrawling
from ImageCrawling import extractors
from ImageCrawling import toolbox

import os
import crawling_filter

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

# Text for each extractor
mobilenet_txt = "The full architecture of MobileNet V1 consists of a regular 3×3 convolution as the very " \
                "first layer, followed by 13 times the above building block." \
                "There are no pooling layers in between these depthwise separable blocks. Instead, some of the " \
                "depthwise layers have a stride of 2 to reduce the spatial dimensions of the data. When that happens, " \
                "the corresponding pointwise layer also doubles the number of output channels. If the input image " \
                "is 224×224×3 then the output of the network is a 7×7×1024 feature map. Thanks to the innovation" \
                " of depthwise separable convolutions, MobileNet has to do about 9 times less work than comparable " \
                "neural nets with the same accuracy."
mobilenetv2_txt = "In comparison to mobilenetv1, in the second version  there are three convolutional layers in the " \
                  "block. The last two are the ones we already know: a depthwise convolution that filters the inputs, "\
                  "followed by a 1×1 pointwise convolution layer. However, this 1×1 layer now has a different job. " \
                  "The second new thing in MobileNet V2’s building block is the residual connection. This works " \
                  "just like in ResNet and exists to help with the flow of gradients through the network. The full " \
                  "MobileNet V2 architecture, then, consists of 17 of these building blocks in a row. This is " \
                  "followed by a regular 1×1 convolution, a global average pooling layer, and a classification layer."
nasnet_txt = "Learning a model architecture directly on a large dataset can be a lengthy process. " \
             "NASNet addressed this issue by transferring a building block designed for a small dataset " \
             "to a larger dataset. The design was constrained to use two types of convolutional cells to return " \
             "feature maps that serve two main functions when convoluting an input feature map: " \
             "normal cells that return maps of the same extent (height and width) and reduction cells in which " \
             "the returned feature map height and width is reduced by a factor of two. For the reduction cell, " \
             "the initial operation applied to the cell’s inputs uses a stride of two (to reduce the height and width)." \
             "The learned aspect of the design included elements such as which lower layer(s) each higher layer " \
             "took as input, the transformations applied at that layer and to merge multiple outputs at each layer. " \
             "In the studied example, the best convolutional layer was designed for the CIFAR-10 dataset and " \
             "then applied to the ImageNet dataset by stacking copies of this cell, each with its own parameters. " \
             "The approach yielded accuracy of 82.7% top-1 and 96.2% top-5. This exceeded the best human-invented" \
             " architectures at a cost of 9 billion fewer FLOPS—a reduction of 28%. The system continued " \
             "to exceed the manually-designed alternative at varying computation levels. The image features " \
             "learned from image classification can be transferred to other computer vision problems. E.g., " \
             "for object detection, the learned cells integrated with the Faster-RCNN framework improved " \
             "performance by 4.0% on the COCO dataset."
xception_txt = "Xception is a convolutional neural network that is 71 layers deep. You can load a " \
               "pretrained version of the network trained on more than a million images from the " \
               "ImageNet database. The pretrained network can classify images into 1000 object categories, " \
               "such as keyboard, mouse, pencil, and many animals. As a result, the network has learned rich " \
               "feature representations for a wide range of images. The network has an image input size of 299-by-299."
vgg16_txt = "VGG16 is a simple and widely used Convolutional Neural Network (CNN) Architecture used for ImageNet, " \
            "a large visual database project used in visual object recognition software research. During training, " \
            "the input to the convnets is a fixed-size 224 x 224 RGB image. Subtracting the mean RGB value " \
            "computed on the training set from each pixel is the only pre-processing done here. The image is " \
            "passed through a stack of convolutional (conv.) layers, where filters with a very small receptive " \
            "field: 3 × 3 (which is the smallest size to capture the notion of left/right, up/down, center and has " \
            "the same effective receptive field as one 7 x 7), is used. It is deeper, has more non-linearities, and " \
            "has fewer parameters. In one of the configurations, 1 × 1 convolution filters, which can be seen as a " \
            "linear transformation of the input channels (followed by non-linearity), are also utilized."


@app.route('/mobilenet', methods=['POST', 'GET'])
def mobilenet():
    if request.method == 'POST':
        file = request.files['query_img']
        search_algorithm = request.form.get('search')

        if search_algorithm == 'hashing':
            'hashing'
            # results = ...
            img = Image.open(file.stream).convert("RGB")  # PIL image
            feature = mobilenet_extractor.extractImage(img)
            uploaded_img = toolbox.image_to_base64(img)

            image = toolbox.image_to_binary(img)
            startTime = time.time()

            results = ImageCrawling.get_nearest_images_2("final.db", image, "big", ImageCrawling.mobileNet, feature,
                                                         count=50)

            t = str((time.time() - startTime))
            checked = 'hashing'

        else:  # lineare Suche

            img = Image.open(file.stream).convert("RGB")  # PIL image
            uploaded_img = toolbox.image_to_base64(img)

            image = toolbox.image_to_binary(img)
            startTime = time.time()
            results = ImageCrawling.get_nearest_images("final.db",
                                                       image,
                                                       "big",
                                                       "mobile_net",
                                                       mobilenet_extractor.extractImage(img),  # feature
                                                       count=50)
            t = str((time.time() - startTime))
            checked = 'euklid'

        return render_template('algorithm.html', query_img=uploaded_img, checked=checked, scores=results, t=t,
                               extractor_text=mobilenet_txt)
    else:
        return render_template('algorithm.html', extractor="MobileNet", checked='',
                               extractor_text=mobilenet_txt)


@app.route('/mobilenetv2', methods=['POST', 'GET'])
def mobilenetv2():

    if request.method == 'POST':
        file = request.files['query_img']

        # results = ...
        img = Image.open(file.stream).convert("RGB")  # PIL image
        feature = mobilenetv2_extractor.extractImage(img)
        uploaded_img = toolbox.image_to_base64(img)
        image = toolbox.image_to_binary(img)
        startTime = time.time()
        results = ImageCrawling.get_nearest_images_2("final.db", image, "big", ImageCrawling.mobileV2, feature,
                                                     count=50)
        t = str((time.time() - startTime))
        checked = 'hashing'

        return render_template('algorithm.html', query_img=uploaded_img, checked=checked, scores=results, t=t,
                               extractor_text=mobilenetv2_txt)
    else:
        return render_template('algorithm.html', extractor="MobileNet Version 2", extractor_text=mobilenetv2_txt)


@app.route('/nasnet', methods=['POST', 'GET'])
def nasnet():
    if request.method == 'POST':
        file = request.files['query_img']

        # results = ...
        img = Image.open(file.stream).convert("RGB")  # PIL image
        feature = nasnet_extractor.extractImage(img)
        uploaded_img = toolbox.image_to_base64(img)
        image = toolbox.image_to_binary(img)
        startTime = time.time()
        results = ImageCrawling.get_nearest_images_2("final.db", image, "big", ImageCrawling.nas, feature, count=50)
        t = str((time.time() - startTime))
        checked = 'hashing'

        return render_template('algorithm.html', query_img=uploaded_img, checked=checked, scores=results, t=t,
                               extractor_text=nasnet_txt)
    else:
        return render_template('algorithm.html', extractor="NasNet", extractor_text=nasnet_txt)


@app.route('/xception', methods=['POST', 'GET'])
def xception():
    if request.method == 'POST':
        file = request.files['query_img']

        # results = ...
        img = Image.open(file.stream).convert("RGB")  # PIL image
        feature = xception_extractor.extractImage(img)
        uploaded_img = toolbox.image_to_base64(img)
        image = toolbox.image_to_binary(img)
        startTime = time.time()
        results = ImageCrawling.get_nearest_images_2("final.db", image, "big", ImageCrawling.xcep, feature, count=50)
        t = str((time.time() - startTime))
        checked = 'hashing'

        return render_template('algorithm.html', query_img=uploaded_img, checked=checked, scores=results, t=t,
                               extractor_text=xception_txt)
    else:
        return render_template('algorithm.html', extractor="Xception", extractor_text=xception_txt)


@app.route('/vgg16', methods=['GET', 'POST'])
def vgg16():
    if request.method == 'POST':
        file = request.files['query_img']

        # results = ...
        img = Image.open(file.stream).convert("RGB")  # PIL image
        feature = vgg16_extractor.extractImage(img)
        uploaded_img = toolbox.image_to_base64(img)
        image = toolbox.image_to_binary(img)
        startTime = time.time()
        results = ImageCrawling.get_nearest_images_2("final.db", image, "big", ImageCrawling.vgg, feature, count=50)
        t = str((time.time() - startTime))
        checked = 'hashing'

        return render_template('algorithm.html', query_img=uploaded_img, checked=checked, scores=results, t=t
                               , extractor_text=vgg16_txt)

    else:
        return render_template('algorithm.html', extractor="VGG16", extractor_text=vgg16_txt)



@app.route('/crawling', methods=['POST', 'GET'])
def crawling():

    if request.method == 'POST':

        if(request.form.get('keyword') != None):
            keyword = request.form['keyword'].lower()
            crawled_img = ImageCrawling.get_images("final.db", keyword)
            return render_template('image-picker.html', keyword=keyword, images=crawled_img)

        else: #save & show selected_img
            selected_img = []
            keyword = request.form['kword']
            crawled_img = ImageCrawling.get_images("final.db", keyword)
            path = "./static/images/filter_img/" + keyword + "_" + datetime.now().isoformat().replace(":", ".") + "/"
            os.makedirs(path, exist_ok=True)

            for i in range(len(crawled_img)):

                img = crawled_img[i]
                if(request.form.get(img) != None):                                         
                    selected_img.append(img)
                    pil_img = toolbox.base64_to_image(img)
                    pil_img.save(path + "/" + keyword + "_" + str(i), 'JPEG')
                   
            return render_template('show-images.html', keyword = keyword, selected_img=selected_img, path = path, filtered_img=None)

    else:
        return render_template('enter-keyword.html')


@app.route('/')
def second():
    return render_template('home.html')


@app.route('/impressum')
def third():
    return render_template('impressum.html')


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='134.2.56.169')
