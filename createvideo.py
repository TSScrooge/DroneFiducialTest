import cv2
import os
import numpy as np
import glob

img_array = []
length = len(os.listdir("framesRect"))
for count in range(length):
    filename = "framesRect/frame%d.jpg" % count
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    print("{:.2f}".format(count/length * 100) + "%")

out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

for i in range(len(img_array)):
    out.write(img_array[i])
    print("{:.2f}".format(i/length * 100) + "%")
out.release()