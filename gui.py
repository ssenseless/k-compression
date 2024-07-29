from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


# defs
def openExplorer():
    global precompress_frame
    filename = filedialog.askopenfilename(
        initialdir='/',
        title='Select an image',
        filetypes=[
            ('Image files', '*.png *.jpg')
        ]
    )

    choice = Image.open(fp=filename).resize(size=(200, 200))
    choice_tk = ImageTk.PhotoImage(choice)

    precompress_frame.config(image=choice_tk)
    precompress_frame.image = choice_tk


# globals
back_col = '#343434'

# simple initializers
root = Tk()
root.title('k-means image compression')
root.config(bg=back_col)
root.geometry('500x500')

# pillowo
image_precompress = Image.new(
    mode='RGB',
    size=(200, 200),
    color=(200, 200, 200)
)
precompress_tk = ImageTk.PhotoImage(image_precompress)

image_postcompress = Image.new(
    mode='RGB',
    size=(200, 200),
    color=(200, 200, 200)
)
postcompress_tk = ImageTk.PhotoImage(image_postcompress)

precompress_frame = Label(image=precompress_tk)
postcompress_frame = Label(image=postcompress_tk)

# component initializers
get_image_label = Label(
    root,
    bg=back_col,
    text='Select image',
)
get_image_button = Button(
    root,
    text='Browse Files',
    command=openExplorer
)
exit_button = Button(
    root,
    text='Exit',
    command=exit
)

# grid
precompress_frame.grid(column=1, row=0, columnspan=2, padx=5, pady=5)
postcompress_frame.grid(column=3, row=0, columnspan=2, padx=5, pady=5)

get_image_label.grid(column=1, row=1, sticky='e', padx=3)
get_image_button.grid(column=2, row=1, sticky='w')

exit_button.grid(column=1, row=2, columnspan=4)

root.grid_columnconfigure((0, 5), weight=1)


if __name__ == "__main__":
    root.mainloop()
