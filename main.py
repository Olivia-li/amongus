import cv2
import numpy as np
import time
import mss
import pygetwindow
import sys
from matplotlib import pyplot as plt
import math
import phone_stream.colors as colors
import string_detection as sd
import spectator_view.main3 as map_view

from discord_handler import DiscordHandler

IGNORE_COLORS = ("black", "darkslategrey", "dimgrey")

class Client:
    def setup(self):
        self.get_window()
        self.color = ""
        self.room_id = ""
        self.templates = []
        self.templ_shapes = []
        self.threshold = 0.47

        for i in range(2):
            self.templates.append(cv2.imread(f"image{i}.png", 0))
            self.templ_shapes.append(self.templates[i].shape[::-1])

        # Map setup
        self.big = cv2.imread(f"spectator_view/amongus_map_mod.png")
        # Resize big to get best algorithm
        og_dimensions = [8565, 4794]
        width_factor = height_factor = 1 / (0.1775 * 4794 / 368)
        new_dimensions = tuple(
            (int(og_dimensions[0] * width_factor), int(og_dimensions[1] * height_factor)))
        self.big = cv2.resize(self.big, new_dimensions)
        self.big_grey = cv2.cvtColor(self.big, cv2.COLOR_BGR2GRAY)
            
    def get_window(self):
        try:
            x1, y1, self.x_center, self.y_center = pygetwindow.getWindowGeometry("Movie Recording")
            self.x_center, self.y_center = int(self.x_center), int(self.y_center)
        except:
            sys.exit("Please make sure to have your Quicktime Movie iPhone Recording open")

        self.monitor = {"top": y1, "left": x1, "width": self.x_center, "height": self.y_center}

    def add_discord_handler(self, dh):
        self.dh = dh

    def run(self):
        self.setup()

        with mss.mss() as sct:
            while True:
                time.sleep(0.1)
                img = np.array(sct.grab(self.monitor))

                self.compute(img)
                map_view.run(self.monitor, self.big, self.big_grey, self.color, img)

                cv2.imshow("rect", img)

                # Press "q" to quit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break


    def overlappingRectangles(self, distinct_rectangles, rect2_top, rect2_bot):
        for rectangle in distinct_rectangles:
            rect1_top = rectangle[0]
            rect1_bot = rectangle[1]
            side_by_side = rect1_top[0] >= rect2_bot[0] or rect2_top[0] >= rect1_bot[0]
            stacked = rect1_top[1] >= rect2_bot[1] or rect2_top[1] >= rect1_bot[1]
            # rectangles overlap
            if not (side_by_side or stacked):
                return True

        return False
    
    def get_room_id(self, img):
        if (pygetwindow.getWindowGeometry("Movie Recording") is not None):
            x1, y1, x_center, y_center = pygetwindow.getWindowGeometry("Movie Recording")
            img = img[int(y_center*2)-int(y_center*0.2):int(y_center*2)-int(y_center*0.05), int(x_center)-int(x_center*0.1):int(x_center)+int(x_center*0.1)]
            string = sd.get_text(img)
            if (len(string) == 6 and string.upper() == string):
                self.room_id = string
                return string
            else:
                return ""
  
    def compute(self, img):
        distinct_rectangles = []

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ANTOINE YOU PROBABLY WANNA PUT THIS SOMEWHERE ELSE. AND STOP RUNNING IT AFTER I
        if not self.room_id:
            self.get_room_id(img)

        if self.room_id and not self.dh.room_id and not self.dh.lobby_id:
            dh.setup(self.room_id)
            dh.run()
            return

        for i in range(len(self.templates)): 
            template, shape = self.templates[i], self.templ_shapes[i]
            w, h = shape
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)

            for pt in zip(*loc[::-1]):
                rect_top = (pt[0], pt[1])
                rect_bot = (pt[0] + w, pt[1] + h)
                if len(distinct_rectangles) == 0 or not self.overlappingRectangles(distinct_rectangles, rect_top, rect_bot):
                    distinct_rectangles.append((rect_top, rect_bot))
                
            for pt, _ in distinct_rectangles:
                self.process_frame(img, pt, w, h)

    def process_frame(self, img, pt, w, h):
        if not self.dh.lobby_id:
            return

        pt_center = (pt[0] + int(w / 2), pt[1] + int(h / 2))
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        distance = math.sqrt((pt_center[0]-self.x_center)**2 + (pt_center[1]-self.y_center)**2)

        color = self.get_character_color(img, pt, w, h)

        if distance > 60 and color in self.dh.color_mapping:
            user_id = int(self.dh.color_mapping[color])
            volume = int(min(max(250 - distance, 0), 100))  # keeping other player's volumes between 0 and 100
            print(f"COLOR {color}: DISTANCE {distance} | VOLUME {volume}")
            self.dh.adjust_user_volume(user_id, volume)
        elif distance < 60 and not color in self.dh.color_mapping and not color in IGNORE_COLORS:
            self.update_color_map(color)
        # elif distance < 60:
            

    def update_color_map(self, color):
        self.color = color
        self.dh.update_color_map(color)
    

    def get_character_color(self, img, pt, w, h):
        pt_center = (pt[0] + int(w / 2), pt[1] + int(h / 2))

        cropped = img[pt_center[1]:pt_center[1]+10, pt_center[0]-5:pt_center[0]+5]
        cv2.imwrite("ignore/cropped.png", cropped)
        rgb, color_name = colors.get_character_color('ignore/cropped.png')

        return color_name


if __name__ == "__main__":
    dh = DiscordHandler()

    client = Client()
    client.setup()
    client.add_discord_handler(dh)
    client.run()
