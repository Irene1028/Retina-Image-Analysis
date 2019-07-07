import cv2
import numpy as np
import math
import operator
from functools import reduce
from itertools import chain


def value_pick(block, f_size, percentile):
    index = math.floor(pow(f_size, 2) * percentile)
    # print(index)
    return block[index]


"""
self-defined filter
"""


def optimal_median(img, f_size, thres, up_pctile, down_pctile):
    """
    get rows and columns and depth
    """
    im_shape = img.shape
    rows = im_shape[0]
    cols = im_shape[1]
    print(rows, cols, rows * cols - 1)
    # pix_line = reduce(operator.add, img)
    pix_line = list(chain(*img))
    pix_line = sorted(pix_line)

    med = .5 * (pix_line[rows * cols - 1] - pix_line[0])
    print(pix_line[rows * cols - 1], pix_line[0], med)
    """
    create a new image
    """
    new_im = np.zeros([rows, cols], np.uint8)

    """
    fill the image
    """
    cp_num = int((f_size - 1) / 2)
    # print(cp_num)
    for i in range(rows):
        for j in range(cols):
            """
            for the peripheral (f_size-1)/2 rows and cols, copy initial value
            """
            if i < cp_num or i > rows - cp_num - 1:
                new_im[i, j] = img[i, j]
            elif j < cp_num or j > cols - cp_num - 1:
                new_im[i, j] = img[i, j]
            else:
                """
                median filter
                """
                block = img[i - cp_num: i + cp_num + 1, j - cp_num: j + cp_num + 1]
                block = sorted(list(chain(*block)))
                # sorted from small to large
                count = 0.0
                for m in range(len(block)):
                    if block[m] > med:
                            count += 1
                if count / pow(f_size, 2) >= thres:
                    """
                    do down_percentile
                    """
                    #print(count)
                    # cv2.waitKey(0)
                    new_im[i, j] = value_pick(block, f_size,  down_pctile)
                else:
                    """
                    do up_percentile
                    """
                    new_im[i, j] = value_pick(block, f_size, up_pctile)
    return new_im


"""
open an image
"""
im_gray = cv2.imread('MAX_BALBC-0b-ND-ph-H-0005.nd2-T_0-1-ph.jpg', 0)

"""
filter size:
"""
# if cells are small, boundaries are thin, use small number like 3 as f_size
# as f_size increases, computational time increases
f_size = 7
kernel5 = np.ones((5, 5))
kernel3 = np.ones((3, 3))
kernel4 = np.ones((4, 4))
kernel2 = np.ones((2, 2))
"""
method 1
"""
im_md = optimal_median(im_gray, f_size, .7, .8, .3)
cv2.imwrite("op_md.jpg", im_md)
mdblur = cv2.medianBlur(im_md, 7)
cv2.imwrite("mdblur.jpg", mdblur)
im_bin = cv2.adaptiveThreshold(mdblur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 69, 0)
cv2.imwrite("binary.jpg", im_bin)
erosion = cv2.erode(im_bin, kernel3)
cv2.imwrite("erode_op.jpg", erosion)

# method 4 above
# blur = cv2.blur(erosion, (5, 5))
# cv2.imwrite("blur.jpg", blur)

# im_md2 = optimal_median(blur, f_size, .9, .6, 0.2)
# cv2.imwrite("op_md2.jpg", im_md2)
# im_bin2 = cv2.adaptiveThreshold(im_md2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 69, 0)
# cv2.imwrite("binary2.jpg", im_bin2)

"""
method 2
"""
# im_bin = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 69, 0)
# cv2.imwrite("binary.jpg", im_bin)
#
# erosion = cv2.erode(im_bin, kernel2)
# cv2.imwrite("erode.jpg", erosion)
#
# im_md = optimal_median(erosion, f_size, .8, .8, 0.4)
# cv2.imwrite("op_md.jpg", im_md)
#
# im_md2 = optimal_median(im_md, 9, .5, .5, .5)
# cv2.imwrite("op_md2.jpg", im_md2)


"""
method 3

binarization + erode + medianBlur + blur + second binarization + medianBlur

worked well for images with great Gaussian noise
"""
#
# im_bin = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 69, 0)
# cv2.imwrite("binary.jpg", im_bin)
# erosion = cv2.erode(im_bin, kernel2)
# cv2.imwrite("erode.jpg", erosion)
# mdblur = cv2.medianBlur(erosion, 3)
# cv2.imwrite("mdblur.jpg", mdblur)
# blur = cv2.blur(mdblur, (5, 5))
# cv2.imwrite("blur.jpg", blur)
# im_bin2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 69, 0)
# cv2.imwrite("binary2.jpg", im_bin2)
# mdblur = cv2.medianBlur(im_bin2, 5)
# cv2.imwrite("mdblur2.jpg", mdblur)

"""
method 1

binarization + augment + erode

worked well for images with unclear boundaries and median noise
"""

# im_bin = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 69, 0)
# cv2.imwrite("binary.jpg", im_bin)
# im_md = optimal_median(im_bin, f_size, .6, .8, .2)
# cv2.imwrite("op_md.jpg", im_md)
# erosion = cv2.erode(im_md, kernel2)
# cv2.imwrite("erode_op.jpg", erosion)
# mdblur = cv2.medianBlur(erosion, 3)
# cv2.imwrite("mdblur.jpg", mdblur)
