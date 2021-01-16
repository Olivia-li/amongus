# import cv2
# import numpy as np
# import pytesseract

# img = cv2.imread("test.jpg")
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower_white = np.array([0,0,0], dtype=np.uint8)
# upper_white = np.array([0,0,255], dtype=np.uint8)

# # Threshold the HSV image to get only white colors
# mask = cv2.inRange(hsv, lower_white, upper_white)
# # Bitwise-AND mask and original image
# res = cv2.bitwise_and(img,img, mask= mask)

# cv2.imshow('mask',mask)
# cv2.imshow('res',res)


# print(pytesseract.image_to_string(img))
# #cv2.imshow("Result", img)
# cv2.waitKey(0)
