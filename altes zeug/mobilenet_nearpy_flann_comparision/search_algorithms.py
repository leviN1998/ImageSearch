import numpy as np
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import EuclideanDistance
from nearpy.filters import NearestFilter
import mobilenet_extractor as mobile
import os
import pyflann
import mobilenet_extractor as mobile
from os import listdir


#loads mobilenet_features in an array
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

    dists = np.linalg.norm(features-img_feature, axis=1) #L2 distances to the mobilenet_features
    ids = np.argsort(dists)[:15] #top 15 resulsts --> should give back which indices are the best 
    print(np.shape(ids))

    scores = [(dists[id], img_paths[id]) for id in ids]
    return scores


def create_lsh_engine(dim, num_bits):
    # Create hash tables
    random_bin_hash1 = RandomBinaryProjections('random_bin_hash1', num_bits)
    random_bin_hash2 = RandomBinaryProjections('random_bin_hash2', num_bits)
    random_bin_hash3 = RandomBinaryProjections('random_bin_hash3', num_bits)
    random_bin_hash4 = RandomBinaryProjections('random_bin_hash4', num_bits)
    random_bin_hash5 = RandomBinaryProjections('random_bin_hash5', num_bits)

    # Create engine with pipeline configuration
    engine1 = Engine(dim, lshashes=[random_bin_hash1, random_bin_hash2, random_bin_hash3, random_bin_hash4, random_bin_hash5], distance=EuclideanDistance(), vector_filters=[NearestFilter(15)])

    return engine1


def lsh(query_vec, feature_dir, engine):
    '''
    input: Dimension of vector space
           feature of query vector
           how many bits the hash value has
    output: list of nearest neighbours (distance, img_path)
    '''
    features, img_paths = mobile.loadSavedFeatures(feature_dir)

    for i, vec in enumerate(features):
       
        engine.store_vector(vec, i) #vector im engine speichern --> im richtigen Bucket

    # Get number of candidates which are in the same bucket as query vector after hashing
    #print(engine1.candidate_count(query_vec))

    # Get 15 nearest neighbours
    N = engine.neighbours(query_vec)

    similar_img1 = [(list(item)[2], img_paths[list(item)[1]]) for item in N]

    return similar_img1


def kmeans(query_vector, feature_dir):
    features, img_paths = loadSavedFeatures(feature_dir)

    dataset = np.array(features, dtype=np.float32)

    flann = pyflann.FLANN()
    pyflann.set_distance_type("chi_square")
    # according to the dataset and desired precision a NN search algorithm will be automatically chosen.
    # available algorithm: linear(brute force), KD-tree, kmeans, composite(mix of kd-tree and kmeans)
    # results, dists = flann.nn(dataset, query_vec, 10, target_precision=0.6, algorithm="autotuned", memory_weight=0)
    results, dists = flann.nn(dataset, query_vector, 10, algorithm="kmeans",branching=16, iteration=5)
    '''
     results: indexes of vectors in dataset
     dists: list of distances between query vector and vectors in dataset. The shortest distance will be stored
               at the top of the list
     Default distance function: euclidean distance
    '''

    similar_img_paths = [(dists[0][i], img_paths[results[0][i]]) for i in range(len(results[0]))] #index error!

    return similar_img_paths
