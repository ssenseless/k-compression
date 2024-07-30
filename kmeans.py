import numpy as np

#defs
def find_closest_centroids(data, centroids):
    # todo: probably vectorize this too
    k = centroids.shape[0]
    idx = np.zeros(data.shape[0], dtype=int)

    for i in range(data.shape[0]):
        distance = []
        for j in range(k):
            norm_ij = np.linalg.norm(data[i] - centroids[j])
            distance.append(norm_ij)

        idx[i] = np.argmin(distance)

    return idx


def compute_centroids(data, idx, k):
    # todo: vectorize this pls
    m, n = data.shape
    centroids = np.zeros((k, n))

    for i in range(k):
        count = 0
        centroid_val = 0
        for j in range(m):
            if idx[j] == i:
                count += 1
                centroid_val += data[j]

        if count == 0:
            centroids[i] = 0
        else:
            centroids[i] = centroid_val / count

    return centroids


def find_k_means(data, initial_centroids, max_iters=10):
    m, n = data.shape
    k = initial_centroids.shape[0]
    centroids = initial_centroids
    idx = np.zeros(m)

    for i in range(max_iters):
        idx = find_closest_centroids(data, centroids)
        centroids = compute_centroids(data, idx, k)

    return centroids, idx


def initialize_rand_centroids(data, k):
    return data[np.random.permutation(data.shape[0])[:k]]


def processImage(image, is_jpg, k):
    processing = np.array(image)

    if is_jpg:
        processing = processing / 255

    processing_reshape = np.reshape(processing, (processing.shape[0] * processing.shape[1], 3))
    centroids, idx = find_k_means(
        data=processing_reshape,
        initial_centroids=initialize_rand_centroids(
            data=processing_reshape,
            k=k
        ),
        max_iters=5
    )

    idx = find_closest_centroids(processing_reshape, centroids)
    processed = np.uint8(np.reshape(centroids[idx, :], processing.shape) * 255)

    return processed, np.uint8(centroids * 255)
