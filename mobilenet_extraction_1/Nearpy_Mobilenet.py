import numpy
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import EuclideanDistance
import mobilenet_extractor as mobile
import copy

def lsh(dim, query_vec, feature_dir, num_bits):
    '''
    input: Dimension of vector space
    output: list of nearest neighbours
    '''
    # Create random binary hash with 10 bits
    random_bin_hash1 = RandomBinaryProjections('random_bin_hash1', num_bits)
    random_bin_hash2 = RandomBinaryProjections('random_bin_hash2', num_bits)
    random_bin_hash3 = RandomBinaryProjections('random_bin_hash3', num_bits)
    random_bin_hash4 = RandomBinaryProjections('random_bin_hash4', num_bits)
    random_bin_hash5 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # Create engine with pipeline configuration
    engine1 = Engine(dim, lshashes=[random_bin_hash1, random_bin_hash2, random_bin_hash3, random_bin_hash4, random_bin_hash5], distance=EuclideanDistance())

    for i, vec in enumerate(mobile.loadSavedFeatures(feature_dir)[0]):
        engine1.store_vector(vec, i)

    # Get nearest neighbours
    print(engine1.candidate_count(query_vec))
    N = engine1.neighbours(query_vec)

    similar_img1 = [(list(item)[2], mobile.loadSavedFeatures(feature_dir)[1][list(item)[1]]) for item in N]
    return similar_img1

if __name__ == "__main__":
    img_dir = "./static/images/"
    feature_dir = "./static/features/"
    query_vec = mobile.extractImage(img_dir + "airplane36.jpg")
    print(lsh(1024, query_vec, feature_dir, 10))