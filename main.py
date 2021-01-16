import cv2
import numpy as np
import time
import mss
import pygetwindow
import sys
from matplotlib import pyplot as plt
import math
import phone_stream.colors as colors

from discord_handler import DiscordHandler

class Client:
    def setup(self):
        self.get_window()

        self.templates = []
        self.templ_shapes = []
        self.threshold = 0.47

        for i in range(2):
            self.templates.append(cv2.imread(f"image{i}.png", 0))
            self.templ_shapes.append(self.templates[i].shape[::-1])

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

                cv2.imshow("rect", img)

                # Press "q" to quit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break


    def overlappingRectangles(distinct_rectangles, rect2_top, rect2_bot):
        for rectangle in distinct_rectangles:
            rect1_top = rectangle[0]
            rect1_bot = rectangle[1]
            # one rectangle is on left side of other 
            if(rect1_top.x >= rect2_bot.x or rect2_top.x >= rect1_bot.x): 
                return False
        
            # one rectangle is above other 
            if(rect2_top.y <= rect1_bot.y or rect1_top.y <= rect2_bot.y): 
                return False
        return True
  
    def compute(self, img):
        distinct_rectangles = []

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for i in range(len(self.templates)): 
            template, shape = self.templates[i], self.templ_shapes[i]
            w, h = shape
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)

            for pt in zip(*loc[::-1]):
                pt_center = (pt[0] + int(w / 2), pt[1] + int(h / 2))
                cv2.circle(img, (self.x_center, self.y_center), 40, (0, 255, 0), 3)
                # cv2.circle(img, pt_center, 10, (255, 0, 0), -1)
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                distance = math.sqrt((pt_center[0]-self.x_center)**2 + (pt_center[1]-self.y_center)**2)
                # self.process_frame(img, pt, w, h) 
                
                image = cv2.circle(img, (pt[0],pt[1]), radius=3, color=(0, 0, 255),thickness=3)
                image = cv2.circle(img, (pt[0] + w,pt[1] + h), radius=3, color=(0, 0, 255),thickness=3)
                pt_center = (pt[0] + int(w / 2), pt[1] + int(h / 2))
                cv2.circle(img, (self.x_center, self.y_center), 40, (0, 255, 0), 3)
                # cv2.circle(img, pt_center, 10, (255, 0, 0), -1)
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                distance = math.sqrt((pt_center[0]-self.x_center)**2 + (pt_center[1]-self.y_center)**2)

                if distance > 60:
                    color = self.get_character_color(img, pt, w, h)
                    username = self.get_username_from_color(color)

                    if username:
                        volume = int(min(max(300 - distance, 0), 150))  # keeping other player's volumes between 0 and 150
                        # print(f"distance, volume from {username} ({color}): {distance} {volume}")
                        self.dh.adjust_user_volume(username, volume)

                        break


    def get_username_from_color(self, color):
        mapping = {
            "palevioletred": "Olive",
            "firebrick": "Antoine",
            "marroon": "Antoine",
            "brown": "Antoine",
            "mediumblue": "nicky",
            "darkblue": "nicky",
            "midnightblue": "nicky"
        }

        return mapping.get(color)

    def get_character_color(self, img, pt, w, h):
        pt_center = (pt[0] + int(w / 2), pt[1] + int(h / 2))

        cropped = img[pt_center[1]:pt_center[1]+10, pt_center[0]-5:pt_center[0]+5]
        cv2.imwrite("ignore/cropped.png", cropped)
        rgb, color_name = colors.get_character_color('ignore/cropped.png')
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        return color_name

        #Antoine
        # return img[pt_center[1] + 3, pt_center[0],]  # convert this to actually color like blue or red


if __name__ == "__main__":

    host = input("Are you the host? y/n") == "y"
    # color = input("Input your character color: ")
    username = input("Input your username: ")

    dh = DiscordHandler(username)

    if host:
        dh.create_lobby()
    else:
        activity_secret = input("Please enter the activity secret given by the host").strip()
        dh.join_lobby(activity_secret)

    dh.run()

    client = Client()
    client.setup()
    client.add_discord_handler(dh)
    client.run()