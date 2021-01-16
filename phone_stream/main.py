import cv2 as cv
import numpy as np
from time import time
import mss
import mss.tools

import pygetwindow
import pyautogui

with mss.mss() as sct:
    
    x1, y1, width, height = pygetwindow.getWindowGeometry('Movie Recording')
    print(x1, y1, width, height)

    # The screen part to capture
    monitor = {"top": y1, "left": x1, "width": width, "height": height}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

print('Done.')