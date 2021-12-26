import os
from os import listdir
from keras.applications import vgg16
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
import numpy as np


base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)
# model.summary()

#extracts images from given img_dir and saves them to feature_dir as img_name.npy
def extractAllImg(img_dir, feature_dir):
    for img_name in listdir(img_dir):
        print(img_name)  
        feature = extractImg(img_dir + img_name)
        img_name = os.path.splitext(img_name)[0] #remove file extension
        np.save(feature_dir + img_name, feature)




#loads features in an array
#loads img names in an array
def loadSavedFeatures(feature_dir):
    featureList = listdir(feature_dir)
    numberOfFeatures = len(featureList)
    #features = {}
    features = []
    img_paths = []

    for i in range(numberOfFeatures):
        img_name = featureList[i]
        img_paths.append("./static/images/" + os.path.splitext(img_name)[0] + ".jpg") #save img path at position i 
        feature_path = os.path.join(feature_dir, img_name)
        feature = np.load(feature_path)
        #feature = feature / np.linalg.norm(feature) # Normalize
        features.append(feature) #save feature at position i
        
        #features[img_name] = feature

    return features, img_paths

#extracts feature of 1 img and saves it to feature_dir
def extractImg(img_path):
    img = image.load_img(img_path, target_size=(224, 224)) #bild in richtiges Format bringen
    img_arr = image.img_to_array(img) #img -> array
    img_arr = np.expand_dims(img_arr, axis=0) #?
    img_arr = preprocess_input(img_arr) #?
    vgg16_feature = model.predict(img_arr)[0] #feature berechnen, este dim auswählen, damit shape = 7*7*512 
    vgg16_feature = vgg16_feature / np.linalg.norm(vgg16_feature) #normieren
    return vgg16_feature
 

def compareImages(img_feature, feature_dir):
    features, img_paths = loadSavedFeatures(feature_dir)

    dists = np.linalg.norm(features-img_feature, axis=1) #L2 distances to the features    
    ids = np.argsort(dists)[:16] #top 15 resulsts --> should give back which indices are the best 
    #print(np.shape(ids))
    
    scores = [(dists[id], img_paths[id]) for id in ids]
    return scores



if __name__ == "__main__":

    img_dir = "./static/images/"
    feature_dir = "./static/vgg16_features/"

    #extractAllImg(img_dir, feature_dir)
    #print(loadSavedFeatures(feature_dir))
    #compareImages()
    print(compareImages(extractImg("./static/images/airplane0.jpg", feature_dir), feature_dir))
    
    #extractImg("./static/img/hund1.jpg", feature_dir) #neues Bild