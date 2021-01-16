import cv2 
import pytesseract 

def get_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    thresh1 = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY_INV)[1]

    text = pytesseract.image_to_string(thresh1)
    print(text) 

    return text