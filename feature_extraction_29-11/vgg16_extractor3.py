import os
from os import listdir
from keras.applications import vgg16
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
import numpy as np

#model = VGG16(weights='imagenet', include_top=False)
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)
# model.summary()

#extracts images from given img_dir and saves them to feature_dir as img_name.npy
def extractAllImg(img_dir, feature_dir):
    imagesList = listdir(img_dir)
    
    for img_name in imagesList:
        img_path = img_dir + img_name
        extractImg(img_path, feature_dir)


#loads features in an array
#loads img names in an array
def loadSavedFeatures(feature_dir):
    featureList = listdir(feature_dir)
    numberOfFeatures = len(featureList)
    #features = {}
    features = []
    img_names = []

    for i in range(numberOfFeatures):
        img_name = featureList[i]
        img_names.append(img_name) #save img name at position i 
        feature_path = os.path.join(feature_dir, img_name)
        feature = np.load(feature_path)
        #feature = feature / np.linalg.norm(feature) # Normalize
        features.append(feature) #save feature at position i
        
        #features[img_name] = feature

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


#funktionert nicht wegen dimensionen
def compareImages(img_feature, feature_dir):
    features, img_names = loadSavedFeatures(feature_dir)
    img_names = np.array(img_names) #convert img_names to numpy array
    features = np.array(features)

    dists = np.linalg.norm(features-img_feature, axis=1) #L2 distances to the features    
    ids = np.argsort(dists)[:5] #top 5 resulsts --> should give back which indices are the best 
    #shape(ids) = 5,7,7,512 --> jetzt 5,7,512
    print(np.shape(ids))
    
    scores = [(dists[id], img_names[id]) for id in ids]
    print(scores)



if __name__ == "__main__":

    img_dir = "./static/img/"
    feature_dir = "./static/features/"

    #extractAllImg(img_dir, feature_dir)
    #print(loadSavedFeatures(feature_dir))
    #compareImages()
    compareImages(extractImg("./static/img/beats.jpg", feature_dir), feature_dir)
    
    #extractImg("./static/img/hund1.jpg", feature_dir) #neues Bild