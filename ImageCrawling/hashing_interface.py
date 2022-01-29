import numpy as np
import io


def dummy_hashing_func(images):
    hashes = []
    for image in images:
        hashes.append(bin(255))
    return hashes


def dummy_calc_distance(feature_a, feature_b):
    return np.linalg.norm(feature_a - feature_b)


def store_in_db(fea_vec, plane):
    hash_value = np.dot(fea_vec, plane.T)
    return ''.join(['1' if x > 0.0 else '0' for x in hash_value])


def calculate_hashes(network: str, features):
    '''
    '''
    plane1 = np.load('ImageDatabases/' + network + '1.npy')
    plane2 = np.load('ImageDatabases/' + network + '2.npy')
    plane3 = np.load('ImageDatabases/' + network + '3.npy')
    plane4 = np.load('ImageDatabases/' + network + '4.npy')
    plane5 = np.load('ImageDatabases/' + network + '5.npy')

    hashes = []
    for f in features:
        feature = np.load(io.BytesIO(f))
        hashes.append((store_in_db(feature, plane1), store_in_db(feature, plane2), store_in_db(feature, plane3), store_in_db(feature, plane4), store_in_db(feature, plane5)))

    return hashes