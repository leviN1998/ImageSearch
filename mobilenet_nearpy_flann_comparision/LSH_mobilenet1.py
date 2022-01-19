from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import EuclideanDistance
from nearpy.filters import NearestFilter
import mobilenet_extractor as mobile


def lsh(dim, query_vec, feature_dir, num_bits):
    '''
    input: Dimension of vector space
           feature of query vector
           how many bits the hash value has
    output: list of nearest neighbours (distance, img_path)
    '''
    features, img_paths = mobile.loadSavedFeatures(feature_dir)

    # Create hash tables
    random_bin_hash1 = RandomBinaryProjections('random_bin_hash1', num_bits)
    random_bin_hash2 = RandomBinaryProjections('random_bin_hash2', num_bits)
    random_bin_hash3 = RandomBinaryProjections('random_bin_hash3', num_bits)
    random_bin_hash4 = RandomBinaryProjections('random_bin_hash4', num_bits)
    random_bin_hash5 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # random_bin_hash6 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # random_bin_hash7 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # random_bin_hash8 = RandomBinaryProjections('random_bin_hash5', num_bits)

    print(random_bin_hash5)


    # Create engine with pipeline configuration
    engine1 = Engine(dim, lshashes=[random_bin_hash1, random_bin_hash2, random_bin_hash3, random_bin_hash4, random_bin_hash5], distance=EuclideanDistance(), vector_filters=[NearestFilter(15)])

    for i, vec in enumerate(features):
        engine1.store_vector(vec, i)

    # Get number of candidates which are in the same bucket as query vector after hashing
    print(engine1.candidate_count(query_vec))

    # Get 15 nearest neighbours
    N = engine1.neighbours(query_vec)

    similar_img1 = [(list(item)[2], img_paths[list(item)[1]]) for item in N]

    return similar_img1



if __name__ == "__main__":
    img_dir = "./static/images/cifar10_200/"
    feature_dir = "./static/features/m_features/cifar10_200"

    # test_dir = "./static/testset/"
    # for img in os.listdir(test_dir):
    #     print("classification accuracy: " + str(getPredictionAccuracy(test_dir + img, feature_dir)))


    query_vec = mobile.extractImage(img_dir + "airplane36.jpg")
    print(lsh(1024, query_vec, feature_dir, 8))
