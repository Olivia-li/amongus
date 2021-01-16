from colorthief import ColorThief
import webcolors 
color_thief = ColorThief('image0.png')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# color = rgb_to_name(dominant_color)
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - dominant_color[0]) ** 2
        gd = (g_c - dominant_color[1]) ** 2
        bd = (b_c - dominant_color[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(dominant_color)
    except ValueError:
        closest_name = closest_colour(dominant_color)
        actual_name = None
    return actual_name, closest_name

requested_colour = (119, 172, 152)
actual_name, closest_name = get_colour_name(dominant_color)
print(dominant_color)

print(closest_name)

# print(dominant_color)