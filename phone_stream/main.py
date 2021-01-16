import cv2
import numpy as np
import time
import mss
import mss.tools
import pygetwindow
import pyautogui
import sys
from matplotlib import pyplot as plt
import math
from colorthief import ColorThief
import colors

# import string_detection as sd

with mss.mss() as sct:

    # You have to have the tab open for this to work
    try:
        x1, y1, width, height = pygetwindow.getWindowGeometry("Movie Recording")
    except:
        sys.exit("Please make sure to have your Quicktime Movie iPhone Recording open")

    # The screen part to capture
    monitor = {"top": y1, "left": x1, "width": width, "height": height}

    templates = []
    templ_shapes = []
    threshold = 0.47

    x_center = int(width)
    y_center = int(height)

    for i in range(2):
        templates.append(cv2.imread(f"image{i}.png",0))
        templ_shapes.append(templates[i].shape[::-1])

    while True:
        img = np.array(sct.grab(monitor))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for i in range(len(templates)): 
            template, shape = templates[i], templ_shapes[i]
            w, h = shape
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                pt_center = (pt[0] + int(w / 2), pt[1] + int(h / 2))
                cv2.circle(img, (x_center, y_center), 40, (0, 255, 0), 3)
                # cv2.circle(img, pt_center, 10, (255, 0, 0), -1)
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                distance = math.sqrt((pt_center[0]-x_center)**2 + (pt_center[1]-y_center)**2)

                if distance > 60:
                    print("distance: {}".format(distance))
                    print(img[pt_center[1] + 3, pt_center[0],])

                cropped = img[pt_center[1]:pt_center[1]+10, pt_center[0]-5:pt_center[0]+5]
                cv2.imwrite("cropped.png", cropped)
                rgb, color_name = colors.get_character_color('cropped.png')
                print(rgb, color_name)
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imshow("rect", img)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
