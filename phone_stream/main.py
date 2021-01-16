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
        x1, y1, width, height = pygetwindow.getWindowGeometry(
            'Movie Recording')

    except:
        sys.exit(
            "Please make sure to have your Quicktime Movie iPhone Recording open")

    print(x1, y1, width, height)

    # The screen part to capture
    monitor = {"top": y1, "left": x1, "width": width, "height": height}

    while "Screen capturing":

        last_time = time.time()
        img = np.array(sct.grab(monitor))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('amongus.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.45
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imshow("OpenCV/Numpy normal", img)

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
