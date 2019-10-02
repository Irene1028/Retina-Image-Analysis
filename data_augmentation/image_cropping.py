import numpy as np
import cv2
import random
# import Image
from PIL import Image

"""
random_image_crop()

Input:
im_path: relative path of original images
crop_shape: [x, y], the resolution you desired
N: the number of new images you want to get

Output: None
"""


def random_image_crop(im_path, crop_shape, N):

    img = cv2.imread(im_path, 0)  # this image should be preprocessed gray images
    filename = im_path.split('/')[-1]

    # height and width of original image
    org_shape = np.shape(img)
    height = org_shape[0]
    width = org_shape[1]

    # randomly choose a point as coordinate origin
    for index in range(0, N):
        new_x = random.randint(0, width - crop_shape[1])  # width
        new_y = random.randint(0, height - crop_shape[0])  # height

        # create, save and show image_crop
        image_crop = img[new_y:new_y + crop_shape[0], new_x:new_x + crop_shape[1]]
        cv2.imwrite("crop/" + str(index) + "_" + filename, image_crop)
        print(index)
        print(new_x)
        print(new_x + crop_shape[1])
        print(new_y)
        print(new_y + crop_shape[0])
        # crop txt
        new_points = crop_XY_coordinates(im_path.split('/')[0] + "/XYcoordinates/" + filename.replace(".jpg", ".txt"),
                            new_x, new_y, crop_shape, index)

        # 画圆，圆心为：(160, 160)，半径为：60，颜色为：point_color，实心线
        for p in new_points:
            cv2.circle(image_crop, (p[0]-new_x, p[1]-new_y), 6, (255, 255, 255), 0)
            # print(p[0])

        cv2.imshow("crop image", image_crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


"""
crop XY coordinates

Input: 
txt_path
new_x, new_y
crop_shape
"""


def crop_XY_coordinates(txt_path, new_x, new_y, crop_shape, index):
    # for xy_coordinates, x is for width, y is for height
    points = np.loadtxt(txt_path)
    points = points.astype(np.int32)
    new_points = list(filter(lambda p: (p[0] >= new_x) and (p[0] < new_x + crop_shape[1]) and (p[1] >= new_y) and (p[1] < new_y + crop_shape[0]), points))
    # print(a)
    new_txt_path = str(index) + "_" + txt_path.split('/')[-1]
    with open(new_txt_path, 'w') as file:
        for p in new_points:
            write_str = '%d %d\n' % (p[0], p[1])
            file.write(write_str)

    return new_points


if __name__ == "__main__":

    random_image_crop('for dot annotation/MAX_BALBC 6m ND ph H 0004-1 ph.jpg', (224, 224), 2)

