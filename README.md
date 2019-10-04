# Retina-Image-Analysis
This repository included code I completed during mice retina image analysis project.

generate_gauss.py create a 2D gaussian distribution for each label dot and integral over the whole image to get the number of cells. It will return/produce a density map for each image and plot it to show the distribution.

data_augmentation included methods including random image cropping, transposing and flipping which can help us enlarge the dataset/training set. I also integrated croping to corresponding density map and XY coordinates.

GUI is a simple user interface which can do simple image processing and count cell numbers in a image.
