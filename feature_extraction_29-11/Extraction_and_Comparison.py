import os
from os import listdir
from keras.applications import vgg16
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import heapq
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


def lsh(embedding_vectors):
    random_plane = np.random.rand(num_bits, dim) - 0.5
    # print(random_plane)

    # Convert feature vector to bit string

    arr_vector = []
    for vector in embedding_vectors:
        arr_vector.append(np.asarray(vector))

    # lists of dot products
    vector_dp = []
    for v in arr_vector:
        vector_dp.append(np.dot(v, random_plane.T))

    # transform dot products into boolean, then into bit
    bool_dp = []
    for dp in vector_dp:
        bool_dp.append(dp > 0)
    bits = []
    for item in bool_dp:
        bits.append(item.astype(int))

    # create lsh buckets {bit string: list of vectors}
    buckets = {}
    for i in range(len(bits)):
        hash_str = ''.join(bits[i].astype(str))
        if hash_str not in buckets.keys():
            buckets[hash_str] = []
        buckets[hash_str].append(i)

    return buckets

# the number of positions at which they have different characters
def hamming_dist(str1, str2):    #str1, str2 have same length
    dist = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            dist += 1
    return dist

# compare the Similarity of query vector and feature vectors in our database
# compare their corresponding bit-strings, if some feature vectors have the same bit-string as the query vector
# they are likely to be similar with the query vector. If there is no vectors in the database which has same bit-string
# then we try to find vectors with the most similar bit-string using hamming distance.
def query(vector, embedding_vectors):
    embedding_vectors.append(vector)
    b = lsh(embedding_vectors)
    num_similar_feature = 5
    index = []
    for item in b.values():
        if len(embedding_vectors)-1 in item:
            if len(item) > num_similar_feature:     # if there exists vector which has same bit-string as query vector
                for i in range(num_similar_feature):
                    index.append(item[i])
                return index
            goal_str = list(b.keys())[list(b.values()).index(item)]
            break

    bit_str_list = list(b.keys())
    # bit_str_list.remove(goal_str)
    hamming = []
    for k in b.keys():
        # if hamming_dist(goal_str, k) < min_dist:
        #     similar_bit_str = k
        hamming.append(hamming_dist(goal_str, k))
    print(len(hamming))
    min_hammings = heapq.nsmallest(num_similar_feature, hamming)
    min_indexes = list(map(hamming.index, min_hammings))
    for n in min_indexes:
        index.append(n)
    return index


if __name__ == "__main__":
    img_dir = "./static/images/"
    feature_dir = "./static/features/"
    embedding_features = loadSavedFeatures(feature_dir)[0]  # list of 4096 dimensional features
    print(len(embedding_features))

    # number of hyperplanes
    num_bits = 256
    # dimension of feature vector
    dim = 4096

    # query_vector = embedding_features[4]
    query_vector = embedding_features[300]
    print(loadSavedFeatures(feature_dir)[1][300])   # name of query image
    indexes = query(query_vector, embedding_features)
    print(indexes)
    similar_feature_vector = []
    for i in indexes:
        similar_feature_vector.append(embedding_features[i])
        print(loadSavedFeatures(feature_dir)[1][i])    # name of the similar image
