import pyflann
import numpy as np
import mobilenet_extractor as mobile

def similiarImgPaths(query_vector, feature_dir):
    embedding_features = mobile.loadSavedFeatures(feature_dir)[0] # list of 4096 dimensional mobilenet_features
    dataset = np.array(embedding_features, dtype=np.float32)

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

    similar_img_paths = [(dists[0][i], mobile.loadSavedFeatures(feature_dir)[1][results[0][i]]) for i in range(len(results[0]))]
    return similar_img_paths

if __name__ == "__main__":
    img_dir = "./static/images/"
    feature_dir = "./static/features/"

    query_vec = mobile.extractImage(img_dir + "horse40.jpg")
    print(similiarImgPaths(query_vec, feature_dir))





