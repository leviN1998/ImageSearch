import numpy as np


def lsh(embedding_vectors):
    random_plane = np.random.rand(num_bits, dim) - 0.5
    print(random_plane)

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


# feature vectors in the same buckets are similar
def query(vector, embeddingvectors):
    embedding_vectors.append(vector)
    b = lsh(embedding_vectors)
    for item in b.values():
        if len(embeddingvectors)-1 in item:
            return item      # item is list of indexes of vectors which are in the same bucket as the query vector


if __name__ == "__main__":
    # number of hyperplanes
    num_bits = 4
    # dimension of feature vector
    dim = 2
    embedding_vectors = [[1, 2], [1, 1], [1.5, 2], [10, 1], [9,2]]
    query_vector = [9,1]
    indexes = query(query_vector, embedding_vectors)
    for i in indexes:
        if embedding_vectors[i] != query_vector:
            print(embedding_vectors[i])