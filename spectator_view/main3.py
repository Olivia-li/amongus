import cv2
import numpy as np
import time
import mss
import mss.tools
import pygetwindow
import pyautogui
import sys
from matplotlib import pyplot as plt

def run():
    with mss.mss() as sct:
        # You have to have the tab open for this to work
        try:
            x1, y1, width, height = pygetwindow.getWindowGeometry("Movie Recording")
        except:
            sys.exit("Please make sure to have your Quicktime Movie iPhone Recording open")
        # The screen part to capture
        monitor = {"top": y1, "left": x1, "width": width, "height": height}
        big = cv2.imread(f"spectator_view/amongus_map_mod.png")
        screen_w, screen_h = 0, 0
        og_dimensions = [8565, 4794]
        # width_factor, height_factor = 0.1775 * 1.5666, 0.1775 * 1.5666
        width_factor = height_factor = 1 / (0.1775 * 4794 / 368)
        new_dimensions = tuple((int(og_dimensions[0] * width_factor), int(og_dimensions[1] * height_factor)))
        big = cv2.resize(big, new_dimensions)
        big_grey = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY) 
        threshold = 0.5

        while True:
            img = np.copy(big)
            img_gray = np.copy(big_grey)
            last_time = time.time()
            small = np.array(sct.grab(monitor))
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
            if (x_center and y_center):
                print(x_center, y_center)
            
            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break