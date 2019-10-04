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


def random_image_crop(img, img_path, crop_shape, N):

    # img_path is the full path of img
    img_name = img_path.split('/')[-1]  # img_name is like "MAXdjfirueb.jpg"
    filename = img_name.split('.')[0]  # filename is like "MAXdjfirueb"

    # height and width of original image
    org_shape = np.shape(img)
    height = org_shape[0]
    width = org_shape[1]

    # randomly choose a point as coordinate origin
    for index in range(0, N):
        new_x = random.randint(0, width - crop_shape[1])  # width
        new_y = random.randint(0, height - crop_shape[0])  # height

        # create, save and show image_crop
        image_crop = np.array(img[new_y:new_y + crop_shape[0], new_x:new_x + crop_shape[1]])
        new_filename = filename + "_" + str(index)
        cv2.imwrite("crop/" + new_filename + ".jpg", image_crop)
        # print("------------New points for each index----------")

        # crop txt
        new_points = crop_XY_coordinates(im_path.split('/')[0] + "/XYcoordinates_josh_compressed_notscaled_DONT_USE/XYcoordinates_josh_original_patch_1/" + img_name.replace(".jpg", ".txt"),
                            new_x, new_y, crop_shape, index)
        crop_density_map("density_map_processed_josh_original/density_map_processed_josh_original_patch_1/" + filename + ".txt", new_y, new_x, crop_shape, index)
        # print(new_points)
        # for p in new_points:
        #     cv2.circle(image_crop, (p[0], p[1]), 2, (255, 0, 0), 0)
        #     # print(p[0])
        #
        # cv2.imshow("crop image", image_crop)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


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
    new_points = np.array(new_points)
    new_points[:, 0] = new_points[:, 0] - new_x
    new_points[:, 1] = new_points[:, 1] - new_y

    # txt_path is the full path of XY
    txt_name = txt_path.split('/')[-1]  # new_txt_path is "MAXfjuaih.txt"
    new_txt_path = "crop_XY/" + txt_name.split('.')[0] + "_" + str(index) + ".txt"
    with open(new_txt_path, 'w') as file:
        for p in new_points:
            write_str = '%d %d\n' % (p[0], p[1])
            file.write(write_str)

    return new_points


"""
crop_densitymap()

"""

def crop_density_map(map_path, new_y, new_x, crop_shape, index):
    map_name = map_path.split('/')[-1]
    filename = map_name.split('.')[0]
    dmap = np.loadtxt(map_path)
    dmap_crop = np.array(dmap[new_y:new_y + crop_shape[0], new_x:new_x + crop_shape[1]])
    np.savetxt("crop_map/" + filename + "_" + str(index) + ".txt", dmap_crop)

    # file = open('crop_map/result.txt', 'w')
    # file.write(str(dmap_crop));
    # file.close()


if __name__ == "__main__":

    with open('all_processed_with_coords/redo_josh_new_md4/josh_processed_original_patch1/ls.txt') as f:
        paths = f.readlines()
    # print(paths)
    for path in paths:
        im_path = 'all_processed_with_coords/redo_josh_new_md4/josh_processed_original_patch1/' + path.strip('\n')
        print(im_path)
    #     im_path = 'all_processed_with_coords/redo_josh_new_md4/josh_processed_original_patch1/zoi_vim_ph_0uMHQ11x_20x_00004-nd2-T-0-1.jpg'
        img = cv2.imread(im_path, 0)  # this image should be preprocessed gray images
        if img.size == 0:
            continue
        if img.shape[0] >= 800 and img.shape[1] >= 800:
            print("---------------- Start Cropping ---------------")
            random_image_crop(img, im_path, (500, 500), 15)

# zoi_vim_ph_0uMHQ11x_20x_00004.nd2-T=0-1.txt not found
