from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from kmeans import processImage


# defs
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
        global pillow_image_postcompress

        choice = Image.open(fp=filename).resize(size=(300, 300))
        compressed, centroids = processImage(choice, filename[-3:] == 'jpg', k)

        choice_tk = ImageTk.PhotoImage(choice)
        precompress_frame.config(image=choice_tk)
        precompress_frame.image = choice_tk

        compressed_tk = ImageTk.PhotoImage(Image.fromarray(compressed))
        postcompress_frame.config(image=compressed_tk)
        postcompress_frame.image = compressed_tk
        pillow_image_postcompress = Image.fromarray(compressed).resize((1000, 1000))

        count = 0
        for centroid in centroids:
            if count > 5:
                break

            centroid_color = ImageTk.PhotoImage(
                Image.new(
                    mode='RGB',
                    size=(50, 50),
                    color=tuple(centroid)
                )
            )
            color_boxes[count].config(image=centroid_color)
            color_boxes[count].image = centroid_color
            color_texts[count].set(f"#{centroid[0]:02x}{centroid[1]:02x}{centroid[2]:02x}")

            count += 1


def save():
    path = filedialog.asksaveasfilename(
        initialdir='/',
        title='Select a save location',
        confirmoverwrite=False,
        filetypes=[
            ('Image files', '.jpg')
        ]
    )
    if path == '':
        flavor_text.set("Must select directory location")
    else:
        pillow_image_postcompress.save(path + '.jpg')
        flavor_text.set("Saved!")


# globals ------------------------------------------------------------------------------------
back_col = '#343434'
filename = ''

# simple initializers ------------------------------------------------------------------------
root = Tk()
root.title('k-means image compression')
root.config(bg=back_col)
root.geometry('1000x600')

# pillowo ------------------------------------------------------------------------------------
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
# todo: maybe make this scroll to match user k
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


# spacing on outsides
root.grid_columnconfigure((0, 7), weight=1)


if __name__ == "__main__":
    root.mainloop()
