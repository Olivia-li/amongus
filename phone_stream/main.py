import cv2
import numpy 
import time
import mss
import mss.tools
import pygetwindow
import pyautogui
import sys

with mss.mss() as sct:
  
    # You have to have the tab open for this to work

    try:
        x1, y1, width, height = pygetwindow.getWindowGeometry('Movie Recording')

    except:
        sys.exit("Please make sure to have your Quicktime Movie iPhone Recording open")
        

    print(x1, y1, width, height)

    # The screen part to capture
    monitor = {"top": y1, "left": x1, "width": width, "height": height}

    while "Screen capturing":
        last_time = time.time()

        img = numpy.array(sct.grab(monitor))
        
        cv2.imshow("OpenCV/Numpy normal", img)

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
