import cv2
import numpy 
import time
import mss
import mss.tools


with mss.mss() as sct:
  # The screen part to capture
  monitor = {"top": 0, "left": 0, "width": 500, "height": 500}

  while "Screen capturing":
    last_time = time.time()

    img = numpy.array(sct.grab(monitor))

    cv2.imshow("OpenCV/Numpy normal", img)

    print("fps: {}".format(1 / (time.time() - last_time)))

    # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
      cv2.destroyAllWindows()
      break
