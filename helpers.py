from colorthief import ColorThief
import webcolors 
import cv2 
import pytesseract 

def get_character_color(img_path):
    color_image = ColorThief(img_path)
    requested_colour = color_image.get_color(quality=6)
    actual_name, closest_name = get_colour_name(requested_colour)
    return requested_colour, closest_name

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def get_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    thresh1 = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY_INV)[1]

    text = pytesseract.image_to_string(thresh1)
    # print("Found in image: " + text.strip()) 
    print(text.strip())

    return text.strip()