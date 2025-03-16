from PIL import Image
import pathlib

# This file contains all the raw functions to create the ASCII art.


def get_image(img_path: str | pathlib.Path) -> list[list[tuple[int, int, int]]]:
    """
    Opens and loads the image data. Creates a list with all pixel RGB values inside.
    Each row of the image has its own list:

        row 1, pixel 1 == pixels[0][0] -> tuple

    Image width == len(pixels[x][x])
    Image height == len(pixels)
    
    :returns: Pixel RGB values as tuples (int, int, int) inside list. 
    """
    path = pathlib.Path(img_path)    

    with Image.open(path) as img:
        pixels = img.load()
        size = img.size
    
    # Append empty list for each row of pixels in the image.
    px_data = [[] for i in range(size[1])]
    
    # Looping over each pixel from left to right, top to bottom.
    for h in range(size[1]):
        for w in range(size[0]):
            px_data[h].append(pixels[w, h][:3]) # First 3 ints are RGB values

    return px_data