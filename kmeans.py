import time
import numpy as np
from PIL import Image


def timer(f, comment="not given"):
    """
    simple function that times other functions
    mostly utilized to test different vectorizations for optimality
    :param f: function to be timed
    :param comment: some helpful identifying information about the function in console
    :return: identical to the return of the timed function
    """
    a = time.time()
    retval = f()
    b = time.time()

    print(f"Time difference (Func: {comment}): {round(b - a, 4)} sec.")
    return retval


def find_closest_centroids(data: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """
    uses L2 norm to calculate the closest centroid to each data point
    :param data: input data (image) of shape [height * width, 3]
    :param centroids: current k centroids to map pixels to
    :return: the centroid indices of each pixel (shape identical to data)
    """
    return np.argmin(  # minimal index
        np.linalg.norm(  # of the l2 norm between
            np.tile(  # each data point
                A=data[..., None],
                reps=centroids.shape[0]
            ) - centroids.T,  # and each centroid
            axis=1
        ),
        axis=1
    )


def compute_centroids(data: np.ndarray, idx: np.ndarray, k: int) -> np.ndarray:
    """
    creates new centroids by computing the mean of
    the pixels assigned to each current centroid
    :param data: input data (image) of shape [height * width, 3]
    :param idx: array of indices mapping [index (pixel) -> value at index (centroid)]
    :param k: number of centroids
    :return: new centroids
    """
    # m is height * width   (pixels)
    # n SHOULD be 3         (R G B)
    m, n = data.shape
    centroids = np.zeros((k, n))

    # make a dictionary pointing from each unique centroid (0 to k - 1)
    # to the amount of pixels associated with that centroid
    # if count is zero then the centroid will not exist
    unique, counts = np.unique(idx, return_counts=True)
    counts = dict(zip(unique, counts))

    # first add each data value to its associated centroid
    for i in range(m):
        centroids[idx[i]] += data[i]

    # then subtract it by the amount of pixels associated with the centroid
    missing_centroid = 0
    for index in unique:
        # catch up from missing indices and correctly report centroid value as zero
        while missing_centroid != index:
            centroids[missing_centroid] = 0
            missing_centroid += 1

        centroids[index] /= counts[index]
        missing_centroid += 1

    return centroids


def top_centroid_percent(idx: np.ndarray, centroids: np.ndarray) -> (np.ndarray, list):
    """
    return the most prevalent six centroids (colors) and the corresponding percentage
    of the total picture they color in
    :param idx: array of indices mapping [index (pixel) -> value at index (centroid)]
    :param centroids: current k centroids (colors)
    :return: the most used six centroids and the percentage of the picture they color in
    """
    # total number of pixels in image
    total = idx.shape[0]

    # make a dictionary pointing from each unique centroid (0 to k - 1)
    # to the amount of pixels associated with that centroid
    unique, counts = np.unique(idx, return_counts=True)
    counts = dict(zip(unique, counts))

    # get most prevalent values from dictionary
    # (sort dictionary by value, backwards, and return top six keys)
    top_6 = sorted(counts, key=counts.get, reverse=True)[:6]

    # get centroids at each key and calculate respective percentages
    centroids = np.array([centroids[index] for index in top_6])
    percents = [(counts[index] / total) * 100 for index in top_6]

    return centroids, percents


def find_k_means(data: np.ndarray, initial_centroids: np.ndarray, max_iters=10) -> (np.ndarray, np.ndarray):
    """
    finds the closest centroids and the pixels
    associated with them in under (max_iters) iterations
    :param data: input data (image) of shape [height * width, 3]
    :param initial_centroids: some initialization of centroids (see initialize_rand_centroids())
    :param max_iters: maximal number of iterations that the algorithm will take before stopping
                      (max_iters is the only stopping condition for this function as there is no
                      epsilon/delta termination functionality)
    :return: k centroids (colors), and the indices of the pixels associated with them
    """
    centroids = initial_centroids

    # iterate back and forth, replacing the indices, then the centroids, until (max_iters)
    for i in range(max_iters):
        idx = find_closest_centroids(data, centroids)
        centroids = compute_centroids(data=data, idx=idx, k=initial_centroids.shape[0])

    return centroids, idx


def initialize_rand_centroids(data: np.ndarray, k: int) -> np.ndarray:
    """
    returns k randomly selected centroids from (data)
    :param data: input data (image) of shape [height * width, 3]
    :param k: number of centroids
    :return: random permutation of (k) pixels from (data)
    """
    return data[np.random.permutation(data.shape[0])[:k]]


def process_image(image: Image, is_jpg: bool, k: int) -> (np.ndarray, np.ndarray, list):
    """
    given an image, return six centroids, the percentage of
    the image that they make up, and the image (as an array)
    with the centroid colors replacing their respective pixels
    (this function is the entry point for the file)
    :param image: a pillow Image containing all pixel data, height, width, etc...
    :param is_jpg: whether the image is a .jpg or .png file (.png colormaps are already 0 - 1)
    :param k: number of centroids (colors) to compress image into
    :return:
             the processed image (as an array with shape [height * width, 3]),
             the six most prevalent centroids (colors),
             the centroids respective percentage of the image
    """
    # need numpy goodness instead of whatever pillow offers
    processing = np.array(image)

    # .png colormaps are 0 - 1 scaled already
    if is_jpg:
        processing = processing / 255

    # turn 2d image into height * width list of pixels
    processing_reshape = np.reshape(processing, (processing.shape[0] * processing.shape[1], 3))

    # get the centroids, map the original pixels to a centroid, reshape back into a 2d image
    centroids, idx = find_k_means(
        data=processing_reshape,
        initial_centroids=initialize_rand_centroids(
            data=processing_reshape,
            k=k
        ),
        max_iters=10
    )
    processed = np.uint8(np.reshape(centroids[idx, :], processing.shape) * 255)

    # quickly grab the top six centroids and their percentage of the image
    centroids, percents = top_centroid_percent(idx, centroids)

    return processed, np.uint8(centroids * 255), percents
