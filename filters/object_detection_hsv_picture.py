import cv2
import numpy as np

# Red bright color
h_min_red_bright = np.array((0, 0, 108), np.uint8)
h_max_red_bright = np.array((183, 25, 170), np.uint8)

# Red color
h_min_red = np.array((0, 88, 12), np.uint8)
h_max_red = np.array((14, 255, 255), np.uint8)

i1 = cv2.imread('Norway.jpg', cv2.IMREAD_REDUCED_COLOR_2)

# hsv = cv2.cvtColor(i1, cv2.COLOR_BGR2)
#
# thresh = cv2.inRange(hsv, h_min_red, h_max_red)
# # res = cv2.bitwise_and(i1, i1, mask=thresh)
#
# th1 = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
#
# _, new = cv2.threshold(thresh, 240, 250, cv2.THRESH_BINARY_INV)
# print(np.shape(new))

cv2.imshow('object', i1)
# cv2.imshow('ot', thresh)
# cv2.imshow('c', new)
cv2.waitKey(0)


