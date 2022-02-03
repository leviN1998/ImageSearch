from json import tool
from random import sample
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os
from os import listdir
from keras.preprocessing import image
from PIL import Image
# import toolbox 
from . import toolbox

class Extractor:

    def __init__(self):
        '''
        Extractor is a base class for all the sub classes like MobileNet, VGG16 etc

        each Extractor has a specific target_size to prepare the images before the features are calculated
        also a network with specific parameters (like include_top = False)
        and net is the network itself, which we need for preprocessing the input
        '''
        self.target_size = None
        self.extracting_network = None
        self.net = None
       
	
    #Methoden:
    #brauchen wir für extractImage
    def preprocessImage(self, pil_img):

        resized_img = pil_img.resize(self.target_size)
        img_array = image.img_to_array(resized_img)
        np.shape(img_array)
        img_array_expanded = np.expand_dims(img_array, axis=0)
        return self.net.preprocess_input(img_array_expanded)


    #eigentliche extractImage(binary_img)-Funktion:
    #binary_img --> 1D feature array, length depending on network
    def extractImage(self, pil_img):

        #pil_img = toolbox.binary_to_image(binary_img)
        preprocessed_image = self.preprocessImage(pil_img)
        feature = self.extracting_network.predict(preprocessed_image)[0]
        # print(np.shape(feature))
        return feature / np.linalg.norm(feature)









    
    #methods for storing and loading features in filesystem:



        # prepares image for the network: changes size of image to specific target_size
    def preprocessImage_by_path(self, img_path):
        img = image.load_img(img_path, target_size = self.target_size)
        img_array = image.img_to_array(img)
        np.shape(img_array)
        img_array_expanded = np.expand_dims(img_array, axis=0)
        return self.net.preprocess_input(img_array_expanded)

    #img -> 1D feature array, length depending on network
    def extractImage_by_path(self, img_path):
        preprocessed_image = self.preprocessImage_by_path(img_path)
        feature = self.extracting_network.predict(preprocessed_image)[0]
        print(np.shape(feature))
        return feature / np.linalg.norm(feature)
    

    #extracts all images from a given image directory and saves them to feature dir
    def extractAllImg(self, img_dir, feature_dir):
        for img_name in listdir(img_dir):
            print(img_name)  
            feature = self.extractImage(img_dir + img_name)
            img_name = os.path.splitext(img_name)[0] #remove .jpg
            np.save(feature_dir + img_name, feature)



    #loads features in an array: features = loadSavedFeatures[0]
    #loads img names in an array: images = loadSavedFeatures[1]
    def loadSavedFeatures(self, feature_dir):
        featureList = listdir(feature_dir)
        features = []
        img_paths = []

        for feature_name in featureList:
            feature_path = os.path.join(feature_dir, feature_name)
            feature = np.load(feature_path)

            features.append(feature)
            img_paths.append("./static/images/cifar10_200/" + os.path.splitext(feature_name)[0] + ".jpg")
        
        return features, img_paths


    #simple linear search 
    #returns 15 similar images
    def linearSearch(self, img_feature, feature_dir):
        features, img_paths = self.loadSavedFeatures(feature_dir)

        dists = np.linalg.norm(features-img_feature, axis=1)    
        ids = np.argsort(dists)[:15] #top 15 resulsts --> should give back which indices are the best 
        print(np.shape(ids))

        scores = [(dists[id], img_paths[id]) for id in ids]
        return scores







'''
subclasses: the actual networks for extracting features

'''

from keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model

class VGG16Extractor(Extractor):
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        
        self.extracting_network = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    
        self.target_size = (224,224)

        self.net = tf.keras.applications.vgg16 


class MobileNet(Extractor):
    def __init__(self):
        
        self.extracting_network = tf.keras.applications.mobilenet.MobileNet(
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
        
        self.net = tf.keras.applications.mobilenet    

        self.target_size = (224,224)


class MobileNetV2(Extractor):
    def __init__(self):
        
        self.extracting_network = tf.keras.applications.mobilenet_v2.MobileNetV2(
            input_shape=None,
            alpha=1.0,
            #depth_multiplier=1,
            #dropout=0.001,
            include_top=False,
            weights="imagenet",
            input_tensor=None,
            pooling="avg",
            classifier_activation="softmax",
        )

        self.net = tf.keras.applications.mobilenet_v2

        self.target_size = (224,224)

class Xception(Extractor):
    def __init__(self):
        
        self.extracting_network = tf.keras.applications.xception.Xception(
            input_shape=None,
            #alpha=1.0,
            #depth_multiplier=1,
            #dropout=0.001,
            include_top=False,
            weights="imagenet",
            input_tensor=None,
            pooling="avg",
            classifier_activation="softmax",
        )

        self.net = tf.keras.applications.xception

        self.target_size = (224, 224)

class NasNet(Extractor):
    def __init__(self):
        
        self.extracting_network = tf.keras.applications.nasnet.NASNetLarge(
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

        self.net = tf.keras.applications.nasnet

        self.target_size = (331, 331)

        










if __name__ == "__main__":

    img = image.load_img('airplane2.jpg') #pil
    binary_img = toolbox.image_to_binary(img)
    M2 = MobileNetV2()
    M2.extractImage(binary_img)
