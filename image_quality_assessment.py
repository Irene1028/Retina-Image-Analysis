import cv2
import numpy as np
import math
# 2019/08/01

"""
Sharpness detection
"""


def get_image_var(img):
    new_img = cv2.Laplacian(img, cv2.CV_64F)
    cv2.imwrite("edge.jpg", new_img)
    return new_img.var()


"""
open an image
"""
im_gray = cv2.imread('MAX_BALBC-0b-ND-ph-H-0006.nd2-T_0-1-ph.jpg', 0)

im_shape = im_gray.shape
rows = im_shape[0]
cols = im_shape[1]


"""
Calculate Brightness

average gray values over the whole img
"""
brightness = 0
for i in range(rows):
    for j in range(cols):
        brightness += im_gray[i][j]
brightness = 1.0 * brightness / (rows * cols)
print(brightness)

"""
Calculate Contract
"""
contract = np.var(im_gray)
print(contract)

"""
Calculate Sharpness

sharpness can only applied to images without noise.
"""
sharpness = get_image_var(im_gray)
print(sharpness)

