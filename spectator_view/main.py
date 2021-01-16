import numpy as np
import time
import cv2

RED = (0, 0, 255)


recording = cv2.VideoCapture('/Users/olivia/Documents/amongus/spectator_view/recording.mkv')
amongus_map = cv2.imread('amongus_map_mod.png')

w, h = [480, 300]

width_map = 1683
width_video = w
width_factor = width_video / width_map

height_map = 1093
height_video = h
height_factor = height_video / height_map

og_dimensions = [8565, 4794]
new_dimensions = tuple((int(og_dimensions[0] * width_factor), int(og_dimensions[1] * height_factor)))
# amongus_map = cv2.resize(amongus_map, new_dimensions)
frame_counter = 0

while(recording.isOpened()):
    frame_counter += 1
    ret, frame = recording.read()
    frame = cv2.resize(frame, (w, h))

    if frame_counter < 25:
        continue

    method = cv2.TM_CCOEFF
    
    start = time.monotonic()
    res = cv2.matchTemplate(amongus_map, frame, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    end = time.monotonic()

    delta = end - start
    print(f"frame idx {frame_counter} that took {delta*1000:.2f}ms")

    
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    
    bottom_right = (top_left[0] + w, top_left[1] + h)
    midpoint = (top_left[0] + int(w/2), top_left[1] + int(h/2))
    print(top_left)
    map_copy = amongus_map.copy()
    cv2.rectangle(map_copy, top_left, bottom_right, RED, 8)
    cv2.circle(map_copy, midpoint, 10, RED, -1)

    map_display = cv2.resize(map_copy, (int(new_dimensions[0] * 0.4), int(new_dimensions[1] * 0.4)))
    frame_display = cv2.resize(frame, (int(w * 0.4), int(h * 0.4)))

    cv2.imshow('template', map_display)
    cv2.imshow('frame', frame_display)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

recording.release()
cv2.destroyAllWindows()