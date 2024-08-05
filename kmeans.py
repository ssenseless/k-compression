import time
import numpy as np


# defs
def timer(f, comment="not given"):
    a = time.time()
    retval = f()
    b = time.time()

    print(f"Time difference (Func: {comment}): {round(b - a, 6)} sec.")
    return retval


def find_closest_centroids(data, centroids):
    return np.argmin(
        np.linalg.norm(
            np.tile(
                A=data[..., None],
                reps=centroids.shape[0]
            ) - centroids.T,
            axis=1
        ),
        axis=1
    )


def compute_centroids(data, idx, k):
    m, n = data.shape
    centroids = np.zeros((k, n))
    unique, counts = np.unique(idx, return_counts=True)
    counts = dict(zip(unique, counts))

    for i in range(m):
        centroids[idx[i]] += data[i]

    missing_centroid = 0
    for index in unique:
        while missing_centroid != index:
            centroids[missing_centroid] = 0
            missing_centroid += 1
        centroids[index] /= counts[index]
        missing_centroid += 1


    return centroids


def find_k_means(data, initial_centroids, max_iters=10):
    idx = np.zeros(data.shape[0])
    centroids = initial_centroids

    for i in range(max_iters):
        idx = find_closest_centroids(data, centroids)
        compute_centroids(data=data, idx=idx, k=initial_centroids.shape[0])

    return centroids, idx


def initialize_rand_centroids(data, k):
    return data[np.random.permutation(data.shape[0])[:k]]


def process_image(image, is_jpg, k):
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
