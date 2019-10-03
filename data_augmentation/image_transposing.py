import cv2
import numpy as np

"""
image_trans_flip

doing transposing and flippings for an image and its corresponding txt file.

Input: 
im_path: image path
Output:
None
"""


def image_trans_flip(im_path):

    img = cv2.imread(im_path)
    img_trans = cv2.transpose(img)  # mode = 2
    img_flip0 = cv2.flip(img, 0)
    img_flip1 = cv2.flip(img, 1)
    img_flip2 = cv2.flip(img, -1)

    img_shape = img.shape
    filename = im_path.split('/')[-1]
    txtname = filename.replace('.jpg', '.txt')
    txt_path = "for dot annotation/XYcoordinates/" + txtname

    points = np.loadtxt(txt_path)
    points = points.astype(np.int32)
    new_points = np.ones((4, points.shape[0], points.shape[1]), dtype=np.int32)
    # print(points.shape)
    new_points[0] = txt_trans_flip(points, img_shape[0], img_shape[1], 0)
    new_points[1] = txt_trans_flip(points, img_shape[0], img_shape[1], 1)
    new_points[2] = txt_trans_flip(points, img_shape[0], img_shape[1], -1)
    new_points[3] = txt_trans_flip(points, img_shape[0], img_shape[1], 2)
    # print(new_points[3])
    cv2.imwrite("transNflip/" + str(0) + "_" + filename, img_flip0)
    cv2.imwrite("transNflip/" + str(1) + "_" + filename, img_flip1)
    cv2.imwrite("transNflip/" + str(2) + "_" + filename, img_flip2)
    cv2.imwrite("transNflip/" + str(3) + "_" + filename, img_trans)

    new_txt_path = []
    for i in range(0, 4):
        new_txt_path.append("new_XY/" + str(i) + "_" + txtname)

    for i in range(0, 4):
        with open(new_txt_path[i], 'w') as file:
            # print("------------Below is new points-------------")
            # print(i)
            # print(new_points[i])
            for p in new_points[i]:
                write_str = '%d %d\n' % (p[0], p[1])
                file.write(write_str)

    """
    Visualizations
    """
    # print(points)
    # for p in points:
    #     cv2.circle(img, (p[0], p[1]), 6, (255, 255, 255), 0)
    # for p0 in new_points[0]:
    #     cv2.circle(img_flip0, (p0[0], p0[1]), 2, (255, 255, 255), 0)
    # for p in new_points[1]:
    #     cv2.circle(img_flip1, (p[0], p[1]), 2, (255, 255, 255), 0)
    # for p in new_points[2]:
    #     cv2.circle(img_flip2, (p[0], p[1]), 2, (255, 255, 255), 0)
    # for p in new_points[3]:
    #     cv2.circle(img_trans, (p[0], p[1]), 2, (255, 255, 255), 0)
    #
    # cv2.imshow('img', img)
    # cv2.imshow('img_trans', img_trans)
    # cv2.imshow('img_flip0', img_flip0)
    # cv2.imshow('img_flip1', img_flip1)
    # cv2.imshow('img_flip_1', img_flip2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

"""
txt flip

Input:
txt_path: relative path of txt file
mode: flip mode. the same as the second arg of cv2.flip()

Output:
new_points: transformed coordinates
"""


def txt_trans_flip(points, height, width, mode):
    new_points = np.array(points)
    if mode == 0:
        new_points[:, 0] = points[:, 0]
        new_points[:, 1] = height - points[:, 1]
    if mode == 1:
        new_points[:, 0] = width - points[:, 0]
        new_points[:, 1] = points[:, 1]
    if mode == -1:
        new_points[:, 0] = width - points[:, 0]
        new_points[:, 1] = height - points[:, 1]
    if mode == 2:
        new_points[:, 0] = points[:, 1]
        new_points[:, 1] = points[:, 0]

    return new_points


if __name__ == "__main__":

    image_trans_flip('for dot annotation/MAX_WT_ph_ZoI_H_20x 0034-1.jpg')



