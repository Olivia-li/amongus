import cv2
import numpy as np
import time
import mss
import mss.tools
import pygetwindow
import pyautogui
import sys
from matplotlib import pyplot as plt

with mss.mss() as sct:

    # You have to have the tab open for this to work
    try:
        x1, y1, width, height = pygetwindow.getWindowGeometry("Movie Recording")

    except:
        sys.exit("Please make sure to have your Quicktime Movie iPhone Recording open")

    # The screen part to capture
    monitor = {"top": y1, "left": x1, "width": width, "height": height}

    big = cv2.imread(f"spectator_view/amongus_map_mod.png", 0)

    # 262 × 240
    # 2414 × 1352
    # 414 × 376

    # 240 / 1352 = 0.1775
    # 376 / 240 = 1.5666
    
    screen_w, screen_h = 0, 0
    og_dimensions = [8565, 4794]
    # width_factor, height_factor = 0.1775 * 1.5666, 0.1775 * 1.5666
    width_factor = height_factor = 1 / (0.1775 * 4794 / 368)
    new_dimensions = tuple((int(og_dimensions[0] * width_factor), int(og_dimensions[1] * height_factor)))
    big = cv2.resize(big, new_dimensions)

    threshold = 0.3

    while "Screen capturing":
        img = np.copy(big)
        last_time = time.time()
        small = np.array(sct.grab(monitor))
        print(small.shape, big.shape)
        small = small[40:-40, 200:-200]
        small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        w, h = small.shape[::-1]
        res = cv2.matchTemplate(img, small, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imshow("OpenCV/Numpy normal", img)
        cv2.imshow("screen", small)
        cv2.imshow("res", res)

        print(small.shape, big.shape)

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
