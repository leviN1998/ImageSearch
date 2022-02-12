from email.mime import image
import imp
from statistics import mean
import ImageCrawling
from ImageCrawling import extractors
from ImageCrawling import toolbox
import numpy as np
import os
from PIL import Image
import math
import bisect
from statistics import mean

'''def calc_distance(img_feature, other_feature):
    
    distance = np.linalg.norm(other_feature-img_feature, axis=1)    
    ids = np.argsort(dists)[:15] #top 15 resulsts --> should give back which indices are the best 
    print(np.shape(ids))

    scores = [(dists[id], img_paths[id]) for id in ids]

'''


def get_pil_img(img_dir):
    img_list = os.listdir(img_dir)
    images = []

    for img_name in img_list:
        img_path = os.path.join(img_dir, img_name)
        print(img_path)

        img = Image.open(img_path).convert('RGB')
        images.append(img)
    
    return images



def get_features(extractor, pil_img_array):
        #features berechnen
    img_features = []
    for img in pil_img_array:
        feature = extractor.extractImage(img)
        img_features.append(feature)
    
    return img_features


#features und umwandlung in b64
def b64_features(extractor, pil_img):
    results = []
    for img in pil_img:
        feature = extractor.extractImage(img)
        results.append((toolbox.image_to_base64(img), feature))

    return results

#es zählt die durchschnittliche Distanz zu den filter_img
#filter_img und all_img: (base64, features)
#scores: (base64, feature, distanz)
def filter_crawled_images(filter_features, all_img_features, size: int):
    
    #brauchen durchschnittl. Distanz jedes Bildes zu den Filter-Bildern
    res = []
    dists = []
    for img in all_img_features:
        
        dists_of_this_img = []
        for filter_img in filter_features:
            
            distance = np.linalg.norm(filter_img[1]-img[1])
            dists_of_this_img.append(distance)

        distance = mean(dists_of_this_img)
        res.append((img[0], img[1], distance))
        dists.append(distance)

    #nach geringster Distanz sortieren
    indexes = np.argsort(dists)[:size]

    scores = [(res[id][0], res[id][1], res[id][2]) for id in indexes]            
    
    return scores





if __name__ == "__main__":

    test_dir = './static/images/test_img/'

    filter_dir = './static/images/filter_img/'

    test_img = get_pil_img(test_dir)
    filter_img = get_pil_img(filter_dir)
    

    mex = extractors.MobileNetV2()
    images_feat = b64_features(mex, test_img)
    filter_feat = b64_features(mex, filter_img)

    print(filter_crawled_images(filter_feat, images_feat, 10))