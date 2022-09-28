# import the necessary packages
import argparse
import cv2
import numpy as np
from PIL import Image
import os
import glob
import time

class PatchAir():

    def __init__(self, model_path, save_data_path, save_results):
        #self.input_img = input_img
        self.refPtx = []
        self.refPty = []
        self.model_name = model_path
        self.data_folder = save_results + '*'
        self.save_results = save_results

    def click_and_crop(self, event, x, y, flags, param):
        # grab references to the global variables
        global refPtx, refPty, cropping

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPtx.append(x)
            self.refPty.append(y)

    def main(self):
        
        # image = cv2.imread('2.png')
        # MIragesize = Lergth=14.36m, Width=9.13m
        # RafaleSize = W=10.30m   L=15.30m
        # Su30MKI Length=21.9 WIdth=14.7m
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        img = Image.open(self.model_name).convert('RGBA')
        size = int(8 * (1 / 0.25)),int(12* (1 / 0.25))
        #size = int(14.36 * (1 / 0.25)),int(9.13* (1 / 0.25))
        img = img.rotate(angle=180, expand=1).resize(size)

        for file in glob.glob(self.data_folder):

            width, height = img.size
            background = Image.open(file)
            image = cv2.imread(file)
            path, name = os.path.split(file)
            print(path, name)

            # keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", image)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    image = clone.copy()

                # if the 'c' key is pressed, break from the loop
                elif key == ord("c"):
                    # img = Image.open('1.jpg')
                    # width,height = img.size
                    # background = Image.open('2.png')
                    # print(refPt)

                    # background.paste(img, (refPt[0], refPt[1], refPt[0] + width, refPt[1]+height ))
                    # background.save('out.png')

                    break

            # if there are two reference points, then crop the region of interest
            # from teh image and display it

            # close all open windows
            print(self.refPtx)
            print(self.refPty)
            # for i in range(len(refPt)):

            # 	print(refPt[])

            for x, y in zip(self.refPtx, self.refPty):
                #print(img.shape)
                background.paste(img, (x, y), img)

            #background.show('image')
            time.sleep(2)

            background.save(self.save_results + name)
            image_re = cv2.imread(file)
            cv2.imshow('image',image_re)
            cv2.waitKey(1000)
            self.refPty = []
            self.refPtx = []

        cv2.destroyAllWindows()

