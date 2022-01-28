import numpy as np


def dummy_hashing_func(images):
    hashes = []
    for image in images:
        hashes.append(bin(255))
    return hashes


def dummy_calc_distance(feature_a, feature_b):
    return np.linalg.norm(feature_a - feature_b)