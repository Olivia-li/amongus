import cv2
import numpy as np
import time
import mss
import mss.tools
import pygetwindow
import pyautogui
import sys
from matplotlib import pyplot as plt
from discord_handler import DiscordHandler

def run(dh, monitor, big, big_grey, color, img_stream):
    img = np.copy(big)
    img_gray = np.copy(big_grey)
    last_time = time.time()

    small = img_stream
    small = small[40:-40, 200:-200]
    small_grey = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    w, h = small_grey.shape[::-1]
    res = cv2.matchTemplate(img_gray, small_grey, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc 

    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)

    cv2.imshow("Spectator View", img)
    cv2.imshow("screen", small)

    x_center = int((bottom_right[0]-top_left[0])/2 + top_left[0])
    y_center = int((bottom_right[1]-top_left[1])/2 + top_left[1])
    if (x_center and y_center and color):
        dh.update_map_coords(x_center, y_center, color)
        print(x_center, y_center)
    
    # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
