import os
from os import listdir
from keras.applications import vgg16
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np

model = VGG16(weights='imagenet', include_top=False)
model.summary()

#extracts images from given img_dir and saves them to feature_dir as img_name.npy
'''def extractAllImg_alt(img_dir, feature_dir):
    imagesList = listdir(img_dir)
    
    for img_name in imagesList:

        img = image.load_img(img_dir+img_name, target_size=(224, 224))
        img_arr = image.img_to_array(img)
        img_arr = np.expand_dims(img_arr, axis=0)
        img_arr = preprocess_input(img_arr)
        vgg16_feature = model.predict(img_arr)
        #save feature 
        img_path = os.path.splitext(img_name)[0] #remove .jpg or jpeg
        feature_path = os.path.join(feature_dir, img_path)
        np.save(feature_path, vgg16_feature)'''



#extracts images from given img_dir and saves them to feature_dir as img_name.npy
def extractAllImg(img_dir, feature_dir):
    imagesList = listdir(img_dir)
    
    for img_name in imagesList:
        img_path = img_dir + img_name
        extractImg(img_path, feature_dir)


#loads features saved in feature_dir and returns 2d dict with names of picture and feature
#features: [img_name] --> [feature]; feature.shape = (1,7,7,512)
def loadSavedFeatures(feature_dir):
    featureList = listdir(feature_dir)
    numberOfFeatures = len(featureList)
    #features = {}
    features = []

    for i in range(numberOfFeatures):
        img_name = featureList[i]
        feature_path = os.path.join(feature_dir, img_name)
        feature = np.load(feature_path)
        features.append(feature)
        #features[img_name] = feature

    return features

#extracts feature of 1 img and saves it to feature_dir
def extractImg(img_path, feature_dir):
    img = image.load_img(img_path, target_size=(224, 224)) #bild in richtiges Format bringen
    img_arr = image.img_to_array(img) #img -> array
    img_arr = np.expand_dims(img_arr, axis=0) #?
    img_arr = preprocess_input(img_arr) #?
    vgg16_feature = model.predict(img_arr) #feature berechnen

    #save feature:
    img_name = os.path.basename(img_path) #"./static/img/bla.jpg" --> bla.jpg
    img_name = os.path.splitext(img_name)[0] #remove .jpg or jpeg
    feature_path = os.path.join(feature_dir, img_name) #bla -> './static/features/bla.npy'
    np.save(feature_path, vgg16_feature)
    return vgg16_feature



#funktioniert nicht
def compareImages(img_feature, features):
    dists = np.linalg.norm(features - img_feature, axis=1) #L2 distances to the features    
    ids = np.argsort(dists)[:30] #top 30 resulsts
    print(ids)
    #scores = [(dists[id], img_paths[id]) for id in ids]



if __name__ == "__main__":

    img_dir = "./static/img/"
    feature_dir = "./static/features/"

    #extractAllImg(img_dir, feature_dir)
    #loadSavedFeatures(feature_dir)
    #compareImages()
    #compareImages(extractImg("./static/img/beats.jpg"),loadSavedFeatures(feature_dir))
    
    #extractImg("./static/img/hund1.jpg", feature_dir) #neues Bild