"""Example using opencv, from tutorial.
"""
import sys

import numpy as np
import cv2


def get_image(path):
    return cv2.imread(path, 0)


def show_image(img, name):
    cv2.imshow(name, img)


def save_image(img, path):
    cv2.imwrite(path, img)


def main(path):
    img = cv2.imread(path, 0)
    cv2.imshow('image',img)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite(path + 'gray.jpg', img)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
