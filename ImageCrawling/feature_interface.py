from tensorflow import keras
import numpy as np
import io
from PIL import Image
from . import toolbox


#wichtig:

# import extractors
from . import extractors

# M2 = extractors.MobileNetV2() zum Initialisieren
# M2.extractImg(binary_img)

#images sind binary images
def mobileNetV2_func(images):

    M2 = extractors.MobileNetV2() 
    features = []
    count = 0
    print("Staring to extract " + str(len(images)) + " features. This might take some time!")
    for image in images:
        feature = M2.extractImage(image)
        features.append(feature)
        if count % 100 == 0:
            print("Extracted features " + str(count) + "/" + str(len(images)))
        count += 1
    return features


def apply_extractor(images, extractor):
    '''
    Inputs: array of binary images, Extractor instance for desired Network
    Outputs: array of binary - features
    '''
    features = []
    count = 0
    print("Staring to extract " + str(len(images)) + " features. This might take some time!")
    for image in images:
        feature = extractor.extractImage(toolbox.binary_to_image(image))
        # Convert feature to binary
        buf = io.BytesIO()
        np.save(buf, feature)
        binary_feature =  buf.getvalue()
        features.append(binary_feature)
        if count % 100 == 0:
            print("Extracted features " + str(count) + "/" + str(len(images)))
        count += 1
    return features


def mobileNet_func(images):
    '''
    '''
    mobileNet = init_mobileNet()
    features = []
    count = 0
    print("Staring to extract " + str(len(images)) + " features. This might take some time!")
    for image in images:
        feature = mobile_extract_image(image, mobileNet)
        features.append(feature)
        if count % 100 == 0:
            print("Extracted features " + str(count) + "/" + str(len(images)))
        count += 1
    
    return features


def mobile_extract_image(image_data, mobileNet):
    preprocessed_image = mobile_prepare_image(image_data)
    feature = mobileNet.predict(preprocessed_image)[0]
    feature = feature / np.linalg.norm(feature)
    buf = io.BytesIO()
    np.save(buf, feature)
    return buf.getvalue()


def init_mobileNet():
    keras.applications.mobilenet.MobileNet()
    mobile = keras.applications.mobilenet.MobileNet(
        input_shape=None,
        alpha=1.0,
        depth_multiplier=1,
        dropout=0.001,
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        pooling="avg",
        classifier_activation="softmax",
    )
    return mobile


def mobile_prepare_image(image_data):
    image = toolbox.binary_to_image(image_data).resize((224, 224))
    # image.show()
    img_array = keras.preprocessing.image.img_to_array(image)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    # print(np.shape(img_array))
    # print(np.shape(img_array_expanded_dims))
    return keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)
