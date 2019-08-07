import numpy as np
import cv2
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
build_gaussian_layer

Imput:

1, mean_X and mean_Y: X and Y cordinations of each annotation dot
2, img_width and img_height: size of a training image
3, standard_deviation: decide the deviation of the gaussian layer

Output:
x,y: a meshgrid in size of img_width by img_height
z: a img_width by img_height matrix with each value equals 3D gaussian distribution
"""


def build_gaussian_layer(mean_x, mean_y, img_width, img_height, standard_deviation):
    x = np.arange(0, img_width, 1)
    y = np.arange(0, img_height, 1)
    x, y = np.meshgrid(x, y)
    z = np.exp(-(np.square(y - mean_y) + np.square(x - mean_x))/(2 * np.square(standard_deviation)))
    z = z/(2 * np.pi * np.square(standard_deviation))
    return x, y, z


"""
get_density_map

Input:
img_path: relative/absolute path of target image
annotation_path: relative/absolute path of annotation txt file

Output:
density_map: a m by n matrix

"""


def get_density_map(img_path, annotation_path):

    """
    load an image and get size
    """
    im_gray = cv2.imread(img_path, 0)
    im_shape = im_gray.shape
    rows = im_shape[0]
    cols = im_shape[1]

    """
    load X, Y cordinations for this image
    """
    x_array = np.loadtxt(annotation_path, delimiter=',', dtype='int', usecols=(0,))
    y_array = np.loadtxt(annotation_path, delimiter=',', dtype='int', usecols=(1,))

    """
    traverse XY cordinations and generate gauss for each annotation
    """
    density_map = [[0 for i in range(rows)] for j in range(cols)]
    # print(density_map)
    cur_x = 0
    cur_y = 0
    for i in range(len(x_array)):
        cur_x, cur_y, cur_gauss = build_gaussian_layer(x_array[i], y_array[i], rows, cols, 5)
        print(np.sum(cur_gauss))
        density_map += cur_gauss

    print('whole sum')
    print(np.sum(density_map))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(cur_x, cur_y, density_map, rstride=1, cstride=1, cmap='rainbow')
    plt.show()
    
    # return density_map


get_density_map('MAX_BALBC-6m-ND-ph-H-0001.nd2-T_0-1-ph.jpg', '0001.txt')

