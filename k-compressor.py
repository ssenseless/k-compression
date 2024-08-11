from tkinter import *
from tkinter import filedialog  # don't know why this has to be separate, but it does
import numpy as np
from PIL import Image, ImageTk
from kmeans import process_image


# defs ---------------------------------------------------------------------------------------
def choose_file() -> None:
    """
    helper function to set the global filename for the gui
    """
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


def resize_image(unaltered: Image) -> Image:
    """
    helper function to resize images and retain aspect ratio
    :param unaltered: unsized image
    :return: resized image
    """
    aspect = 300 / max(unaltered.height, unaltered.width)

    return unaltered.resize(
        size=(
            int(unaltered.width * aspect),
            int(unaltered.height * aspect)
        )
    )


def reset_colors() -> None:
    """
    helper function to reset color boxes and texts so
    they properly update when changing k or image
    """
    for i in range(6):
        reset_image = ImageTk.PhotoImage(
            Image.new(
                mode='RGB',
                size=(50, 50),
                color=(200, 200, 200)
            )
        )
        color_boxes[i].config(image=reset_image)
        color_boxes[i].image = reset_image
        color_texts[i].set("")

        percent_texts[i].set("")


def set_colors(centroids: np.ndarray, percents: np.ndarray, k: int) -> None:
    """
    helper function to update the color boxes, texts, and
    percent texts after they have been reset
    :param centroids: six most prevalent centroids (colors)
    :param percents: percentage of pixels associated with each centroid
    :param k: total number of centroids (colors)
    """
    # make an image, hex tag, and percentage for each centroid
    for i, centroid in enumerate(centroids):
        centroid_color = ImageTk.PhotoImage(
            Image.new(
                mode='RGB',
                size=(50, 50),
                color=tuple(centroid)
            )
        )
        color_boxes[i].config(image=centroid_color)
        color_boxes[i].image = centroid_color
        color_texts[i].set(f"#{centroid[0]:02x}{centroid[1]:02x}{centroid[2]:02x}")

        percent_texts[i].set(f"{round(percents[i], 2)}%")

    # set remaining percentage for remaining (nonspecific) "centroids"
    if k > 6:
        remaining_explain.set(f"Remaining {k - 6} colors")
    else:
        remaining_explain.set(f"Remaining 0 colors")
    remaining_percent.set(f"{round(100 - sum(percents), 2)}%")


def compress() -> None:
    """
    general function to run kmeans compression and 
    helper functions on click
    """
    k = k_input.get()
    
    # catch user edge cases
    if filename == '':
        flavor_text.set('Must select a photo before confirming pixel amount')
    elif k == 0:
        flavor_text.set('Color number must be greater than zero')
    else:
        # once again not entirely sure why these two specifically need to be here
        global pillow_image_postcompress
        global image_to_save
        
        # get user selected image, resize, run kmeans, update application with helper functions
        choice = Image.open(fp=filename)
        choice_resized = resize_image(choice)
        compressed, centroids, percents = process_image(
            image_unsized=choice,
            image_sized=choice_resized,
            is_jpg=filename[-3:] == 'jpg',
            k=k
        )

        image_to_save = Image.fromarray(compressed)

        choice_tk = ImageTk.PhotoImage(choice_resized)
        precompress_frame.config(image=choice_tk)
        precompress_frame.image = choice_tk

        compressed_tk = ImageTk.PhotoImage(
            image_to_save.resize(
                size=(
                    choice_resized.width,
                    choice_resized.height
                )
            )
        )
        postcompress_frame.config(image=compressed_tk)
        postcompress_frame.image = compressed_tk
        pillow_image_postcompress = Image.fromarray(compressed)

        reset_colors()
        set_colors(centroids, percents, k)


def save() -> None:
    """
    allow users to save compressed photos as .jpg or .png
    """
    path = filedialog.asksaveasfilename(
        initialdir='/',
        title='Select a save location',
        confirmoverwrite=True,
        filetypes=[
            ('Image files', '.jpg')
        ],
        defaultextension="*.*"
    )
    
    # user edge case handle
    if path == '':
        flavor_text.set("Must select directory location")
    else:
        image_to_save.save(path)
        flavor_text.set("Saved!")


# globals ------------------------------------------------------------------------------------
back_col = '#343434'
filename = ''
image_to_save = None

# simple initializers ------------------------------------------------------------------------
root = Tk()
root.title('k-means image compression')
root.config(bg=back_col)
root.geometry('1000x600')

# pillowo ------------------------------------------------------------------------------------

# images and image frames
image_precompress = ImageTk.PhotoImage(
    Image.new(
        mode='RGB',
        size=(300, 300),
        color=(200, 200, 200)
    )
)
pillow_image_postcompress = Image.new(
    mode='RGB',
    size=(300, 300),
    color=(200, 200, 200)
)
image_postcompress = ImageTk.PhotoImage(pillow_image_postcompress)

precompress_frame = Label(image=image_precompress)
postcompress_frame = Label(image=image_postcompress)

# color boxes and images
image_colors = [
    ImageTk.PhotoImage(
        Image.new(
            mode='RGB',
            size=(50, 50),
            color=(200, 200, 200)
        )
    )
    for _ in range(6)
]
color_boxes = [Label(image=image_colors[i]) for i in range(6)]

# component initializers ---------------------------------------------------------------------
# labels for images
save_image = Button(
    root,
    text="Save compressed image",
    command=save
)
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

# helper text for user
flavor_text = StringVar()
flavor_text_label = Label(
    root,
    bg=back_col,
    textvariable=flavor_text
)
flavor_text.set('Select an image below to get started')

# button to select image
image_button = Button(
    root,
    text='Browse Files',
    command=choose_file
)

# input box and button to choose k for k-means
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

# color boxes to show user (up to) 6 colors in photo
color_box_label = Label(
    root,
    bg=back_col,
    text='Colors',
    font=('Arial', 10)
)
color_texts = [StringVar() for _ in range(6)]
color_text_labels = [
    Label(
        root,
        bg=back_col,
        textvariable=color_texts[i]
    )
    for i in range(6)
]

# percentage of centroids in picture labels
percent_texts = [StringVar() for _ in range(6)]
percent_text_labels = [
    Label(
        root,
        bg=back_col,
        textvariable=percent_texts[i]
    )
    for i in range(6)
]
remaining_percent = StringVar()
remaining_percent_label = Label(
    root,
    bg=back_col,
    textvariable=remaining_percent
)
remaining_explain = StringVar()
remaining_explain_label = Label(
    root,
    bg=back_col,
    textvariable=remaining_explain
)

# grid ---------------------------------------------------------------------------------------
# images
precompress_frame.grid(column=1, row=0, columnspan=3, padx=5, pady=(5, 0))
postcompress_frame.grid(column=4, row=0, columnspan=3, padx=5, pady=(5, 0))
save_image.grid(column=7, row=0)

# image labels
immutable1.grid(column=1, row=1, columnspan=3, padx=5)
immutable2.grid(column=4, row=1, columnspan=3, padx=5)

# user helper text
flavor_text_label.grid(column=1, row=2, columnspan=6, pady=3)

# image selection button
image_button.grid(column=1, row=3, columnspan=6, pady=5)

# user input k
k_input_entry.grid(column=1, row=4, columnspan=3, sticky='e', pady=5, padx=(0, 5))
confirm_button.grid(column=4, row=4, columnspan=3, sticky='w', pady=5, padx=(5, 0))

# color boxes
color_box_label.grid(column=1, row=5, columnspan=6, pady=(1, 4))
for i in range(6):
    color_boxes[i].grid(column=i + 1, row=6)
    color_text_labels[i].grid(column=i + 1, row=7)
    percent_text_labels[i].grid(column=i + 1, row=8)

remaining_explain_label.grid(column=7, row=7)
remaining_percent_label.grid(column=7, row=8)


# spacing on outsides
root.grid_columnconfigure((0, 7), weight=1)


if __name__ == "__main__":
    root.mainloop()
