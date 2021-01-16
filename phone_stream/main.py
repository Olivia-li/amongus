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

    for i in range(2):
        templates.append(cv2.imread(f"image{i}.png",0))
        templ_shapes.append(templates[i].shape[::-1])

    while True:

        last_time = time.time()
        img = np.array(sct.grab(monitor))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        x_center = 500
        y_center = 200

        for i in range(len(templates)): 
            template, shape = templates[i], templ_shapes[i]
            w, h = shape
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

                # trying to detect colour of character behind the rectangle but it's too slow
                # cropped = img[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
                # cv2.imwrite("cropped.png", cropped)
                # color_cropped = ColorThief('cropped.png')
                # dominant_color = color_cropped.get_color(quality=1)
                # print(dominant_color)

                # Logic to calculate distance between other characters and yourself
                distance = math.sqrt((pt[0]-x_center)**2 + (pt[1]-y_center)**2)
                if (pt[0] in range(470, 530) and pt[1] in range(170, 230)) or distance < 70:
                    x_center = pt[0]
                    y_center = pt[1]
                else:
                    distance = math.sqrt((pt[0]-x_center)**2 + (pt[1]-y_center)**2)
                    print("distance: {}".format(distance))

        cv2.imshow("Character Recognition", img)

        # print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
