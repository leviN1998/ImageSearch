import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import os
from os import listdir

tf.keras.applications.nasnet.NASNetLarge()

nasnet = tf.keras.applications.nasnet.NASNetLarge(
    input_shape=None,
    #alpha=1.0,
    #depth_multiplier=1,
    #dropout=0.001,
    include_top=False,
    weights="imagenet",
    input_tensor=None,
    pooling="avg",
    #classifier_activation="softmax",
)

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(331, 331))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.nasnet.preprocess_input(img_array_expanded_dims)

#img -> 1D feature array with length = 1024
def extractImage(img_path):
    preprocessed_image = prepare_image(img_path)
    feature = nasnet.predict(preprocessed_image)[0]
    print(np.shape(feature))
    return feature / np.linalg.norm(feature)


#extracts all images from a given image directory and saves them to feature dir
def extractAllImg(img_dir, feature_dir):
    for img_name in listdir(img_dir):
        print(img_name)  
        feature = extractImage(img_dir + img_name)
        img_name = os.path.splitext(img_name)[0] #remove file extension
        np.save(feature_dir + img_name, feature)

#loads features in an array
#loads img names in an array
def loadSavedFeatures(feature_dir):
    featureList = listdir(feature_dir)
    #print(featureList)
    numberOfFeatures = len(featureList)
    features = []
    img_paths = []

    for i in range(numberOfFeatures):
        img_name = featureList[i]
        feature_path = os.path.join(feature_dir, img_name)
        feature = np.load(feature_path)
        
        features.append(feature) #save feature at position i
        img_paths.append("./static/images/" + os.path.splitext(img_name)[0] + ".jpg") #save img path at position i 
        
    return features, img_paths


#simple linear search for similar images
def compareImages(img_feature, feature_dir):
    features, img_paths = loadSavedFeatures(feature_dir)

    dists = np.linalg.norm(features-img_feature, axis=1) #L2 distances to the features    
    ids = np.argsort(dists)[:15] #top 15 resulsts --> should give back which indices are the best 
    print(np.shape(ids))

    scores = [(dists[id], img_paths[id]) for id in ids]
    return scores


if __name__ == "__main__":

    img_dir = "./static/images/"
    feature_dir = "./static/nasnet_features/"

    extractAllImg(img_dir, feature_dir)

    #samplequery = extractImage(img_dir + "horse22.jpg")

    #np.shape(samplequery)
    #list = compareImages(samplequery, feature_dir)
    #print(list)

