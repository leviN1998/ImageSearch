import numpy
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import EuclideanDistance
from nearpy.filters import NearestFilter
import mobilenet_extractor as mobile
#import pymysql
import copy
import time
import os
import re

'''
db1 = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'Ying',
    passwd = 'Mumucy030927?',
    db = 'Img'
)

cursor = db1.cursor()
'''
num_bits = 8
random_bin_hash1 = RandomBinaryProjections('random_bin_hash1', num_bits)
random_bin_hash2 = RandomBinaryProjections('random_bin_hash2', num_bits)
random_bin_hash3 = RandomBinaryProjections('random_bin_hash3', num_bits)
random_bin_hash4 = RandomBinaryProjections('random_bin_hash4', num_bits)
random_bin_hash5 = RandomBinaryProjections('random_bin_hash5', num_bits)

def lsh(dim, query_vec, feature_dir, num_bits):
    '''
    input: Dimension of vector space
           feature of query vector
           how many bits the hash value has
    output: list of nearest neighbours (distance, img_path)
    '''
    features, img_paths = mobile.loadSavedFeatures(feature_dir)

    # Create hash tables
    #random_bin_hash1 = RandomBinaryProjections('random_bin_hash1', num_bits)
    #random_bin_hash2 = RandomBinaryProjections('random_bin_hash2', num_bits)
    #random_bin_hash3 = RandomBinaryProjections('random_bin_hash3', num_bits)
    #random_bin_hash4 = RandomBinaryProjections('random_bin_hash4', num_bits)
    #random_bin_hash5 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # random_bin_hash6 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # random_bin_hash7 = RandomBinaryProjections('random_bin_hash5', num_bits)
    # random_bin_hash8 = RandomBinaryProjections('random_bin_hash5', num_bits)

    # Create engine with pipeline configuration
    engine1 = Engine(dim, lshashes=[random_bin_hash1, random_bin_hash2, random_bin_hash3, random_bin_hash4, random_bin_hash5], distance=EuclideanDistance(), vector_filters=[NearestFilter(15)])

    for i, vec in enumerate(features):
        engine1.store_vector(vec, i) #vector im engine speichern --> im richtigen Bucket

    '''
    Hashwert in die Datenbank reinzuschreiben:
    
    for vec in mobile.loadSavedFeatures(feature_dir)[0]:
        for i, lshash in enumerate(engine1.lshashes):
            if i == 0:
                sql = "insert into hashes (Feature_vec, Hash1) values(%s, %s) "
            if i == 1:
                sql = "insert into hashes (Feature_vec, Hash2) values(%s, %s) "
            if i == 2:
                sql = "insert into hashes (Feature_vec, Hash3) values(%s, %s) "
            if i == 3:
                sql = "insert into hashes (Feature_vec, Hash4) values(%s, %s) "
            if i == 4:
                sql = "insert into hashes (Feature_vec, Hash5) values(%s, %s) "
            bucket_key = lshash.hash_vector(vec)
            cursor.execute(sql, (''.join(str(e) for e in vec), bucket_key))
    # cursor.close()
    # db1.commit()
    # db1.close()
    query_bucket_key = []
    for lshash in engine1.lshashes:
        for bucket_key in lshash.hash_vector(query_vec, querying=True):
            query_bucket_key.append(bucket_key)
    print(query_bucket_key)

    sql1 = "select Hash1 from hashes"
    cursor.execute(sql1)
    datalist = []
    alldata = cursor.fetchall()
    for s in alldata:
        datalist.append(s[0])
    print(len(datalist))

    c = 1
    count = 0
    j = 0
    for h in datalist:
        if c % 811 == 0:
            j += 1
        if h == ''.join(query_bucket_key[j]):
                count += 1

    print(count)
    cursor.close()
    db1.commit()
    db1.close()
    '''

    # Get number of candidates which are in the same bucket as query vector after hashing
    print(engine1.candidate_count(query_vec)) 

    # Get 15 nearest neighbours
    N = engine1.neighbours(query_vec)

    similar_img1 = [(list(item)[2], img_paths[list(item)[1]]) for item in N]

    return similar_img1

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

def getPredictionAccuracy(query_img_path, feature_dir):
    query_img_class = getClassName(query_img_path)
    print(query_img_class)

    query_feature = mobile.extractImage(query_img_path)
    start = time.time()
    results = lsh(1024, query_feature, feature_dir, 8)[1:]  # cut off first element, as this will be the query img itself
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
    img_dir = "./static/images/"
    feature_dir = "./static/features/"

    test_dir = "./static/testset/"
    #for img in os.listdir(test_dir):
    #    print("classification accuracy: " + str(getPredictionAccuracy(test_dir + img, feature_dir)))


    query_vec = mobile.extractImage(img_dir + "airplane36.jpg")
    print(lsh(1024, query_vec, feature_dir, 8))
