import numpy as np
import mobilenet_extractor as mobile
import time
import os
import re


def hash(fea_vec, plane):
    dp = np.dot(fea_vec, plane.T)   # dot product of feature vector and the normal vector of hyperplane
    # Return binary key
    return ''.join(['1' if x > 0.0 else '0' for x in dp])


def euclidean_dist(x, y):
    return np.linalg.norm(x-y)

# 5 buckets
def store_in_bucket(buckets, hash_name, bucket_key, index):
    # buckets = {}
    if not hash_name in buckets:
        buckets[hash_name] = {}
    if bucket_key not in buckets[hash_name]:
        buckets[hash_name][bucket_key] = []
    buckets[hash_name][bucket_key].append(index)

def lsh(feature_dir, query_vec, hash_tables):
    features, img_paths = mobile.loadSavedFeatures(feature_dir)

    buckets = {}
    for h in hash_tables:
        for i, vec in enumerate(features):
            bucket_key = hash(vec, h[0])
            store_in_bucket(buckets, h[1], bucket_key, i)

    hashes_query = []
    for t in hash_tables:
        hashes_query.append((t[1], hash(query_vec, t[0])))
    print(hashes_query)

    dists = []
    indexes = []
    for h_query in hashes_query:
        for i in buckets[h_query[0]][h_query[1]]:
            if i not in indexes:
                indexes.append(i)
                dists.append((euclidean_dist(features[i], query_vec), img_paths[i]))

    sorted_list = sorted(dists, key=lambda x:x[0])
    print(len(sorted_list))
    try:
        return sorted_list[:15]
    except:
        return sorted_list

# checks if given string is equal to one of the classes or not
def isClass(name):
    classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    return True if (name in classes) else False

# retrieves classname (or name of img) of a given img_path
def getClassName(path):
    basename = os.path.basename(path)
    classname = os.path.splitext(basename)[0]
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    classname = temp.match(classname).groups()[0]
    return classname

def getPredictionAccuracy(query_img_path, feature_dir, hash_tables):
    query_img_class = getClassName(query_img_path)
    print(query_img_class)

    query_feature = mobile.extractImage(query_img_path)
    start = time.time()
    results = lsh(feature_dir, query_feature, hash_tables)[1:]  # LSH FOR MOBILENET
    end = time.time()
    cost1 = end-start
    print("runtime using lsh:" + str(cost1))

    # start = time.time()
    # results_l = mobile.compareImages(query_feature,feature_dir)
    # end = time.time()
    # cost2 = end-start
    # print("runtime using linear search" + str(cost2))
    #
    # print("speedup:" + str(cost2/cost1))


    # percentage of how many of the results have the same class as query img
    c = 0;
    top5 = 0;
    top10 = 0

    for i in range(len(results)):

        result_class = getClassName(results[i][1])
        if (result_class == query_img_class):
            c = c + 1

        if (i == 4):
            top5 = (c / 5)
        if (i == 9):
            top10 = (c / 10)  # '{:.2%}'.format

    return [top5, top10, (c / len(results))]


if __name__ == "__main__":
    img_dir = "./static/images/cifar10_200/"
    feature_dir = "./static/features/m_features/cifar10_200"

    # plane1 = np.random.rand(8, 1024) - 0.5
    # np.save('plane1.npy', plane1)
    plane1 = np.load('plane1.npy')
    plane_normal1 = (plane1, 'norm1')
    # plane2 = np.random.rand(8, 1024) - 0.5
    # np.save('plane2.npy', plane2)
    plane2 = np.load('plane2.npy')
    plane_normal2 = (plane2, 'norm2')
    # plane3 = np.random.rand(8, 1024) - 0.5
    # np.save('plane3.npy', plane3)
    plane3 = np.load('plane3.npy')
    plane_normal3 = (plane3, 'norm3')
    # plane4 = np.random.rand(8, 1024) - 0.5
    # np.save('plane4.npy', plane4)
    plane4 = np.load('plane4.npy')
    plane_normal4 = (plane4, 'norm4')
    # plane5 = np.random.rand(8, 1024) - 0.5
    # np.save('plane5.npy', plane5)
    plane5 = np.load('plane5.npy')
    plane_normal5 = (plane5, 'norm5')


    hash_tables = [plane_normal1, plane_normal2, plane_normal3, plane_normal4, plane_normal5]

    query_vec = mobile.extractImage(img_dir + "cat182.jpg")

    # start = time.time()
    # print(lsh(feature_dir, query_vec, hash_tables))
    # end = time.time()
    # print(end-start)

    test_dir = "./static/testset/"
    for img in os.listdir(test_dir):
        print("classification accuracy: " + str(getPredictionAccuracy(test_dir + img, feature_dir, hash_tables)))



