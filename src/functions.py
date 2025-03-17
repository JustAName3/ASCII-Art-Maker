from PIL import Image
import pathlib
import time

# This file contains all the raw functions to create the ASCII art.

ASCII_chars = list("#@%*=/!+~:-,. ")[::-1] # All ASCII characters I am going to use. Sorted (by me) form high density [0] to low density [-1]. Note the space at the end!
# Max width and height of the characters. Measured in notepad. 
char_width = 8
char_height = 13



def open_img(path: str | pathlib.Path) -> Image:
    """
    Opens and checks the mode of the image.
    If the mode is not the desired mode, img gets converted.

    :returns: Image

    :raises: FileNotFoundError if path is invalid.
    """
    path = pathlib.Path(path)

    if path.exists():
        with Image.open(path) as img:
            if img.mode != "RGB" or img.mode != "RGBA":
                new = img.convert(mode= "RGB")
                return new
            else:
                return img
    else:
        raise FileNotFoundError
    

def parse_image(img: Image) -> list[list[tuple[int, int, int]]]:
    """
    Loads the image data. Creates a list with all pixel RGB values inside.
    Each row of the image has its own list:

        row 1, pixel 1 == pixels[0][0] -> tuple

    Image width == len(pixels[x][x])
    Image height == len(pixels)
    
    :returns: Pixel RGB values as tuples (int, int, int) inside list. 
    """
    pixels = img.load()
    size = img.size
    
    # Append empty list for each row of pixels in the image.
    px_data = [[] for i in range(size[1])]
    
    # Looping over each pixel from left to right, top to bottom.
    for h in range(size[1]):
        for w in range(size[0]):
            px_data[h].append(pixels[w, h][:3]) # First 3 ints are RGB values

    return px_data


def grayify(pixel_data: list) -> list[list[int]]:
    """
    Takes in pixel data (-> parse_image()) with RGB values. Adds RGB values and divides them by 3.
    
    :returns: Lists with lists for every row, in which are the gray values. Only one per pixel. 
    """
    pixels = [[] for row in range(len(pixel_data))]

    index = 0
    for row in pixel_data:
        for pixel in row:
            gray_px = (pixel[0] + pixel[1] + pixel[2]) /3 
            gray_px = round(gray_px)
            
            pixels[index].append(gray_px)
    	
        index += 1

    return pixels


# I dont plan on using this. Maybe this comes in handy in certain situations.
def make_gray_img(pixel_data: list) -> Image:
    """
    Makes a new Image object.
    Takes the grayscale pixel data in. 
    
    :returns: Image
    """
    img_size = (len(pixel_data[0]), len(pixel_data))
    new_img = Image.new(mode= "L", size= img_size)
    
    # Lopping over each pixel and setting the corresponding pixel of new_img to the right "color". 
    for h in range(len(pixel_data)):
        for w in range(len(pixel_data[h])):
            new_img.putpixel(xy= (w, h), value= pixel_data[h][w])


    return new_img


def get_char(gray_value: int, chars: list):
    """
    Calculates which of the given chars represents the value best.
    Takes the gray value and a list of the ASCII chars.
    
    Splits the chars list into pieces. Checks in which piece the gray value is located.

    :returns: str 
    """
    space = 255 / len(chars) # How many pixel values are represented by one character.

    index = round(gray_value / space) -1


    return chars[index]


def make_ASCII(pixel_data: list, chars: list) -> str:
    """
    Converts the image from grayscale into ASCII art.
    Takes the grayscale pixel data and the available chars.
        
    :returns: str
    """
    raw = [] # Stores the raw ASCII art before it is joined into one string.
    start = time.time()

    for row in pixel_data:
        for pixel in row:
            char = get_char(gray_value= pixel, chars= chars)
            raw.append(char)
        
        raw.append("\n")    # New line after each row.

    del raw[-1] # Deletes \n after last row.
    # Joining the list of chars into one big string.
    ASCII_art: str = "".join(raw)

    end = time.time()
    print("time: ", end - start, "sec.")

    return ASCII_art


def Steam_size(width: int, height: int, nl_chars: int) -> tuple[int, int]:
    """
    Calculates the new width and height of an image to stay below 1.001 pixels while saving aspect ratio.
    Steam profile comments are limited to 1.000 characters.

    Takes the newline characters into account.
    Newlines are placed after every row except the last one (see: make_ASCII()).
    
    :returns: tuple[int, int] -> [0] == width, [1] == height
    """
    area = width * height
    target_area = 1000 - nl_chars
    scale_factor = (target_area / area) ** 0.5 # A * s² = 1.000

    new_w = int(width * scale_factor)
    new_h = int(height * scale_factor)


    return new_w, new_h