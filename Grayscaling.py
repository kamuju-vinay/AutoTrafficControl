from skimage import io
from tkinter import filedialog
import tkinter as tk
import matplotlib.pyplot as plt
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean

# Create a simple Tkinter window to open the file dialog
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open a file dialog for the user to select an image
file_path = filedialog.askopenfilename()

# Check if the user selected a file
if file_path:
    # Load the selected image
    original = io.imread(file_path)
    image = color.rgb2gray(original)


    image_rescaled = rescale(image, 0.25, anti_aliasing=False)

    image_resized = resize(image, (image.shape[0] // 4, image.shape[1] // 4),anti_aliasing=True)

    image_downscaled = downscale_local_mean(image, (4, 3))


    fig, axes = plt.subplots(nrows=2, ncols=2)

    ax = axes.ravel()

    ax[0].imshow(image, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(image_rescaled, cmap='gray')
    ax[1].set_title("Rescaled image (aliasing)")

    ax[2].imshow(image_resized, cmap='gray')
    ax[2].set_title("Resized image (no aliasing)")

    ax[3].imshow(image_downscaled, cmap='gray')
    ax[3].set_title("Downscaled image (no aliasing)")

    ax[0].set_xlim(0, 512)
    ax[0].set_ylim(512, 0)
    plt.tight_layout()
    plt.show()
