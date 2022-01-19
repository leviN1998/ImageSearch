import numpy as np
import mobilenet_extractor as mobile
import pymysql
import time
import ast
import os
import re

def store_hv_as_bu(fea_vec):
    # store hash value as buckets: {'hash_name': hash value}    5 pairs key and value in one bucket

    plane1 = np.load('plane1.npy')
    plane2 = np.load('plane2.npy')
    plane3 = np.load('plane3.npy')
    plane4 = np.load('plane4.npy')
    plane5 = np.load('plane5.npy')
    hash_planes = [(plane1, 'normal1'), (plane2, 'normal2'), (plane3, 'normal3'), (plane4, 'normal4'), (plane5, 'normal5')]

    bucket = {}
    for plane in hash_planes:
        hash_value = np.dot(fea_vec, plane[0].T)
        bucket[plane[1]] = ''.join(['1' if x > 0.0 else '0' for x in hash_value])
    return bucket

def store_hv_as_l(fea_vec):
    # input: feature vector
    # store hash values as list like ['00111110', '10101110', '01011110', '11011110', '00111110']

    plane1 = np.load('plane1.npy')
    plane2 = np.load('plane2.npy')
    plane3 = np.load('plane3.npy')
    plane4 = np.load('plane4.npy')
    plane5 = np.load('plane5.npy')
    hash_planes = [(plane1, 'normal1'), (plane2, 'normal2'), (plane3, 'normal3'), (plane4, 'normal4'), (plane5, 'normal5')]

    l = []
    for plane in hash_planes:
        hash_value = np.dot(fea_vec, plane[0].T)
        l.append(''.join(['1' if x > 0.0 else '0' for x in hash_value]))
    return l

def store_in_db(fea_vec, plane):
    hash_value = np.dot(fea_vec, plane.T)
    return ''.join(['1' if x > 0.0 else '0' for x in hash_value])

def euclidean_dist(x, y):
    return np.linalg.norm(x-y)
'''
def search(query_vec):
    # select features with same hash value at same position as query vector
#   select all rows from column hashing as list
    query_list = store_hv_as_l(query_vec)     # hash values for query vector
    candidates = []    # list of tuples(distance, image_name)
    ids = []
    for item in list:         # list: all lists of hash values
        for i in range(len(query_list)):
            if item[i] == query_list[i]:
            # get id of the item from db
            if id not in ids:
                ids.append(id)
                candidates.append(euclidean_dist(query_vec, feature of the item), image_name with id)

    sorted_list = sorted(candidates, key=lambda x: x[0])
    print(len(sorted_list))
    try:
        return sorted_list[:15]   # 15 nearest neighbours
    except:
        return sorted_list
'''

def search_for_neighbours(query_vec, db1):
    plane1 = np.load('plane1.npy')
    plane2 = np.load('plane2.npy')
    plane3 = np.load('plane3.npy')
    plane4 = np.load('plane4.npy')
    plane5 = np.load('plane5.npy')
    q1 = store_in_db(query_vec, plane1)   # hash1
    q2 = store_in_db(query_vec, plane2)
    q3 = store_in_db(query_vec, plane3)
    q4 = store_in_db(query_vec, plane4)
    q5 = store_in_db(query_vec, plane5)
    cursor1 = db1.cursor()
    sql1 = "select id from img_search where hash1=10100111 or hash2=11111000 or hash3=10001000 or hash4=01000111 or hash5=10111001"
    cursor1.execute(sql1)
    id_as_tuple = cursor1.fetchall()
    cursor1.close()
    db1.commit()
    db1.close()

    # get indexes of candidates(vectors) for further linear search
    indexes = []
    for tu in id_as_tuple:
        indexes.append(int(''.join(map(str, tu))))
    print(indexes)

    dist_img = []
    for index in indexes:
        dist_img.append((euclidean_dist(features[index], query_vec), img_paths[index]))

    sorted_list = sorted(dist_img, key=lambda x: x[0])
    print(len(sorted_list))
    try:
        return sorted_list[:15]
    except:
        return sorted_list


if __name__ == "__main__":
    db1 = pymysql.connect(
        host=,
        port=,
        user=,
        passwd=,
        db=
    )
    img_dir = "./static/images/cifar10_200/"
    feature_dir = "./static/features/m_features/cifar10_200"

    features, img_paths = mobile.loadSavedFeatures(feature_dir)

    query_vec = mobile.extractImage(img_dir + "airplane36.jpg")
    print(search_for_neighbours(query_vec, db1))


'''
    cursor = db1.cursor()
    sql = "insert into img_search (id, img_path, feature, hash1, hash2, hash3, hash4, hash5) values (%s, %s, %s, %s, %s, %s, %s, %s) "

    # for i, vec in enumerate(features):
    #     l = store_hv_as_l(vec)
    #     cursor.execute(sql, (i, img_paths[i], ''.join(str(e) for e in vec), l))

    plane1 = np.load('plane1.npy')
    plane2 = np.load('plane2.npy')
    plane3 = np.load('plane3.npy')
    plane4 = np.load('plane4.npy')
    plane5 = np.load('plane5.npy')

    for i, vec in enumerate(features):
        hash1 = store_in_db(vec, plane1)
        hash2 = store_in_db(vec, plane2)
        hash3 = store_in_db(vec, plane3)
        hash4 = store_in_db(vec, plane4)
        hash5 = store_in_db(vec, plane5)
        cursor.execute(sql, (i, img_paths[i], ''.join(str(e) for e in vec), hash1, hash2, hash3, hash4, hash5))
        
    cursor.close()
    db1.commit()
    db1.close()
'''



