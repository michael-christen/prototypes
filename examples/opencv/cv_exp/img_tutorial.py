"""Example using opencv, from tutorial.
"""
import sys

import numpy as np
import cv2 as cv


def get_image(path):
    return cv.imread(path, cv.IMREAD_COLOR)


def show_image(img, name):
    cv.imshow(name, img)


def save_image(img, path):
    cv.imwrite(path, img)


def main(path):
    img = cv.imread(path, cv.IMREAD_COLOR)
    cv.imshow('image',img)
    k = cv.waitKey(0)
    if k == 27 or k == ord('q'):  # wait for ESC key to exit
        cv.destroyAllWindows()
    elif k == ord('s'): # wait for 's' key to save and exit
        cv.imwrite(path + 'gray.jpg', img)
        cv.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
