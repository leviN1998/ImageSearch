import pyflann
import numpy as np
import os
from os import listdir
from keras.applications import vgg16
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model


#model = VGG16(weights='imagenet', include_top=False)
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)
# model.summary()

# extracts images from given img_dir and saves them to feature_dir as img_name.npy
def extractAllImg(img_dir, feature_dir):
    imagesList = listdir(img_dir)

    for img_name in imagesList:
        img_path = img_dir + img_name
        extractImg(img_path, feature_dir)


# loads features in an array
# loads img names in an array
def loadSavedFeatures(feature_dir):
    featureList = listdir(feature_dir)
    numberOfFeatures = len(featureList)
    # features = {}
    features = []
    img_names = []

    for i in range(numberOfFeatures):
        img_name = featureList[i]
        img_names.append(img_name)  # save img name at position i
        feature_path = os.path.join(feature_dir, img_name)
        feature = np.load(feature_path)
        # feature = feature / np.linalg.norm(feature) # Normalize
        features.append(feature)  # save feature at position i

        # features[img_name] = feature

    return features, img_names


#extracts feature of 1 img and saves it to feature_dir
def extractImg(img_path, feature_dir):
    img = image.load_img(img_path, target_size=(224, 224)) #bild in richtiges Format bringen
    img_arr = image.img_to_array(img) #img -> array
    img_arr = np.expand_dims(img_arr, axis=0) #?
    img_arr = preprocess_input(img_arr) #?
    vgg16_feature = model.predict(img_arr)[0] #feature berechnen, este dim auswählen, damit shape = 7*7*512
    vgg16_feature = vgg16_feature / np.linalg.norm(vgg16_feature) #normieren

    #save feature:
    img_name = os.path.basename(img_path) #"./static/img/bla.jpg" --> bla.jpg
    img_name = os.path.splitext(img_name)[0] #remove .jpg or jpeg
    feature_path = os.path.join(feature_dir, img_name) #bla -> './static/features/bla.npy'
    np.save(feature_path, vgg16_feature)
    print(np.shape(vgg16_feature))
    return vgg16_feature


def extract_single_Img(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # bild in richtiges Format bringen
    img_arr = image.img_to_array(img)  # img -> array
    img_arr = np.expand_dims(img_arr, axis=0)  # ?
    img_arr = preprocess_input(img_arr)  # ?
    vgg16_feature = model.predict(img_arr)[0]  # feature berechnen, este dim auswählen, damit shape = 7*7*512
    vgg16_feature = vgg16_feature / np.linalg.norm(vgg16_feature)  # normieren
    return vgg16_feature


if __name__ == "__main__":
    img_dir = "./static/images/"
    feature_dir = "./static/features/"
    embedding_features = loadSavedFeatures(feature_dir)[0]  # list of 4096 dimensional features
    print(len(embedding_features))

    dataset = np.array(embedding_features, dtype=np.float32)

    # query_vec = np.array(embedding_features[15], dtype=np.float32)
    # print(loadSavedFeatures(feature_dir)[1][15])
    query_vec = extract_single_Img("./static/query/images (2).jpg")

    flann = pyflann.FLANN()

    # according to the dataset and desired precision a NN search algorithm will be automatically chosen.
    # available algorithm: linear(brute force), KD-tree, kmeans, composite(mix of kd-tree and kmeans)
    results, dists = flann.nn(dataset, query_vec, 10, target_precision = 0.9, algorithm="autotuned")
    # dists: list of distances between query vector and vectors in dataset. The shortest distance will be stored
    # at the top of the list
    print(results)           # indexes of vectors in dataset
    for n in range(len(results[0])):
        print(loadSavedFeatures(feature_dir)[1][results[0][n]] + ' ' + str(dists[0][n]))