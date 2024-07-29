import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


# defs
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
        max_iters=2
    )

    idx = find_closest_centroids(processing_reshape, centroids)
    processed = Image.fromarray(np.uint8(np.reshape(centroids[idx, :], processing.shape) * 255))

    return processed, centroids


def choose_file():
    global filename
    filename = filedialog.askopenfilename(
        initialdir='/',
        title='Select an image',
        filetypes=[
            ('Image files', '*.png *.jpg')
        ]
    )

    if filename != '':
        flavor_text.set('Now change the amount of colors to compress to, then confirm')

    else:
        flavor_text.set('Must select either .png or .jpg')


def compress():
    k = k_input.get()
    if filename == '':
        flavor_text.set('Must select a photo before confirming pixel amount')
    elif k == 0:
        flavor_text.set('Color number must be greater than zero')
    else:
        choice = Image.open(fp=filename).resize(size=(300, 300))
        choice_tk = ImageTk.PhotoImage(choice)
        precompress_frame.config(image=choice_tk)
        precompress_frame.image = choice_tk

        compressed, centroids = processImage(choice, filename[-3:] == 'jpg', k)
        compressed_tk = ImageTk.PhotoImage(compressed)
        postcompress_frame.config(image=compressed_tk)
        postcompress_frame.image = compressed_tk


# globals
back_col = '#343434'
filename = ''

# simple initializers
root = Tk()
root.title('k-means image compression')
root.config(bg=back_col)
root.geometry('1000x600')

# pillowo
image_precompress = Image.new(
    mode='RGB',
    size=(300, 300),
    color=(200, 200, 200)
)
precompress_tk = ImageTk.PhotoImage(image_precompress)

image_postcompress = Image.new(
    mode='RGB',
    size=(300, 300),
    color=(200, 200, 200)
)
postcompress_tk = ImageTk.PhotoImage(image_postcompress)

precompress_frame = Label(image=precompress_tk)
postcompress_frame = Label(image=postcompress_tk)

# component initializers
flavor_text = StringVar()
flavor_text_label = Label(
    root,
    bg=back_col,
    textvariable=flavor_text
)
flavor_text.set('Select an image below to get started')

immutable1 = Label(
    root,
    bg=back_col,
    text='Uncompressed image',
    font=('Arial', 7)
)
immutable2 = Label(
    root,
    bg=back_col,
    text='Compressed image',
    font=('Arial', 7)
)

image_label = Label(
    root,
    bg=back_col,
    text='Select image',
)
image_button = Button(
    root,
    text='Browse Files',
    command=choose_file
)

k_input = IntVar()
k_input_entry = Entry(
    root,
    textvariable=k_input
)
confirm_button = Button(
    root,
    text='Confirm',
    command=compress
)

# grid
precompress_frame.grid(column=1, row=0, columnspan=2, padx=5, pady=(5, 0))
postcompress_frame.grid(column=3, row=0, columnspan=2, padx=5, pady=(5, 0))

immutable1.grid(column=1, row=1, columnspan=2, padx=5)
immutable2.grid(column=3, row=1, columnspan=2, padx=5)

flavor_text_label.grid(column=1, row=2, columnspan=4, pady=3)

image_button.grid(column=1, row=3, columnspan=4, pady=5)

k_input_entry.grid(column=1, row=4, columnspan=2, sticky='e', pady=5, padx=(0, 5))
confirm_button.grid(column=3, row=4, columnspan=2, sticky='w', pady=5, padx=(5, 0))

root.grid_columnconfigure((0, 5), weight=1)


if __name__ == "__main__":
    root.mainloop()
