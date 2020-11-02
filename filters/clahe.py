import numpy as np
import cv2

def adjust_gamma(image, gamma=1):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invgamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

img = cv2.imread('bright_red.jpg', cv2.IMREAD_REDUCED_GRAYSCALE_2)

adjusted = adjust_gamma(img, gamma=0.5)

cv2.imshow('adj', adjusted)
cv2.waitKey(0)

cl = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
cl1 = cl.apply(img)

cv2.imshow('clahe', cl1)
cv2.imshow('orig', img)
cv2.waitKey()