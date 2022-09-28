from PIL import Image
import os
import cv2
import numpy as np
from past_model import PatchAir
import argparse

# Useful Constants and Variables


class SyntheticDataGeneration:
    def __init__(self, opt):
        self.cropping_list = []
        self.IMG_NAME = opt.input_image.split('/')[-1]
        self.IMG_EXTENSION = '.' + self.IMG_NAME.split('.')[-1]
        self.infile = opt.input_image
        infile = self.infile
        self.DATASET_DIR = '/'.join(infile.split('/')[-1])

        self.CHOP_SIZE = opt.CHOP_SIZE
        Image.MAX_IMAGE_PIXELS = None
        self.model_path = opt.input_model
        self.save_data = opt.save_crops
        self.save_results = opt.save_results


    def click_func(self,event, x, y, flags, param):
        """
        Click function that fire-up against the user click event
        :param event:
        :param x:
        :param y:
        :param flags:
        :param param:
        :return:
        """
        #global cropping_list
        if event == cv2.EVENT_LBUTTONDOWN:
            x1 = x - self.CHOP_SIZE // 2
            x2 = x + self.CHOP_SIZE // 2
            y1 = y - self.CHOP_SIZE // 2
            y2 = y + self.CHOP_SIZE // 2

            cv2.rectangle(param, (x1, y1), (x2, y2), (0, 255, 0), thickness=6)
            cv2.imshow(self.IMG_NAME, param)
            self.cropping_list.append([x1, y1, x2, y2])



    def crop_patch(self,image, cr_item):
        """
        Function to crop the patch from the loaded image
        :param image: Pillow image
        :param cr_item: Box coordinates
        :return:
        """
        width, height = image.size
        box = (cr_item[0], cr_item[1],
               cr_item[0] + self.CHOP_SIZE if cr_item[0] + self.CHOP_SIZE < width else width - 1,
               cr_item[1] + self.CHOP_SIZE if cr_item[1] + self.CHOP_SIZE < height else height - 1)
        # try:
        fname = 'slice_%s_x%03d_y%03d.jpg' % (self.IMG_NAME.replace(self.IMG_EXTENSION, ''), cr_item[0], cr_item[1])
        new_name = os.path.sep.join([self.DATASET_DIR, fname])
        print(new_name)
        image.crop(box).save(self.save_data+ fname)
        image.crop(box).save(self.save_results + fname)
        #return image.crop(box)

    def show_loading(self):
        """
        Display the loadingIMG_NAMEas a feedback for the user
        :return:
        """
        img_progress = np.ones(shape=(64, 64, 1))
        cv2.putText(img_progress, 'WORKING ON IMAGE, PLEASE WEIGHT',
                    (0, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255,), 1, cv2.LINE_AA, False)
        cv2.imshow('Loading', img_progress)


    def main(self):
        """
        Main function to load the image and process it using the loop
        :return:
        """
        print(self.infile)
        img = cv2.imread(self.infile)
        height, width, _ = img.shape
        cv2.namedWindow(self.IMG_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.IMG_NAME, (3000,2000))
        cv2.setMouseCallback(self.IMG_NAME, self.click_func, param=img)
        patchair = PatchAir(self.model_path, self.save_data, self.save_results)

        while True:
            cv2.imshow(self.IMG_NAME, img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                self.show_loading()
                img_clone = Image.open(self.infile)
                for crop_item in self.cropping_list:
                    self.crop_patch(img_clone, crop_item)
                #patchair.main()
                img_clone.close()
                self.cropping_list.clear()
                break  # or load next image

            elif key == ord('q'):
                break
        cv2.destroyAllWindows()
        patchair.main()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_image', type=str, default='Input/test.jpg', help='large dimenssion satellite image')
    parser.add_argument('--input_model', type=str, default='models/car_white.png', help='synthetic image of the object')
    parser.add_argument('--CHOP_SIZE', type=int, default=608, help='size of the cropping patch')
    parser.add_argument('--save_crops', type=str, default='crops/', help='path to save the crops')
    parser.add_argument('--save_results', type=str, default='results/', help='path to save the crops with synthetic data')

    opt = parser.parse_args()
    load = SyntheticDataGeneration(opt)
    load.main()
