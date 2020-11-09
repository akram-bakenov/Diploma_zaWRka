from __future__ import print_function
import numpy as np
import cv2


def steering_angle(center):
    # coefficient
    k = 0.091
    b = -29.14
    angle = (center[0] * k + b)
    if angle > 20:
        angle = 20
    elif angle < -20:
        angle = -20
    color_yellow = (0, 255, 255)
    cv2.putText(original, "Steering Angle = %ddeg" % (angle), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_yellow, 2)
    print(angle)


# Red bright color
h_min_red_bright = np.array((0, 0, 109), np.uint8)
h_max_red_bright = np.array((183, 20, 208), np.uint8)

# Red bright color
h_min_red_bright04 = np.array((0, 0, 29), np.uint8)
h_max_red_bright04 = np.array((216, 49, 65), np.uint8)

# Red dark color
h_min_red_bright2 = np.array((63, 0, 46), np.uint8)
h_max_red_bright2 = np.array((255, 255, 255), np.uint8)

# Red dark color
h_min_red_bright27 = np.array((58, 0, 40), np.uint8)
h_max_red_bright27 = np.array((255, 255, 255), np.uint8)


def hough(img, gamma, h_min, h_max):


    # hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    # thresh = cv2.inRange(hsv, h_min, h_max)
    # cv2.imshow('vfffffff', thresh)
    # cv2.waitKey()
    kernel = np.ones((1, 1), np.uint8)
    # adjusted = adjust_gamma(img, gamma=gamma)
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    erode = cv2.erode(blur, kernel)
    dilation = cv2.dilate(erode, kernel)
    adjusted = adjust_gamma(dilation, gamma=gamma)
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, h_min, h_max)
    cv2.imshow('vfffffff', thresh)
    cv2.waitKey()
    cv2.imshow('вавав', adjusted)
    cv2.waitKey()
    canny = cv2.Canny(image = thresh, threshold1 =5, threshold2 = 10, apertureSize = 3, L2gradient = True)
    cv2.imshow('canny', canny)
    cv2.waitKey()
    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=250, param2=20, minRadius=10, maxRadius=100)
    print(circles)
    if circles is not None:
        # search all circles
        for i in circles[0, :]:
            center = (i[0], i[1])
            # steering_angle(img, center)
            radius = i[2]
            # draw big cirlce
            cv2.circle(img, center, radius, (0, 255, 0), 3)
            # draw little circle
            cv2.circle(img, center, 1, (0, 255, 0), 5)
            # cv2.putText(original, "Gamma coef.={}".format(gamma), (10, 30),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            # steering_angle(center)
        # res = cv2.bitwise_and(adjusted, adjusted, mask=thresh)
        # cv2.imshow('Hough_circle', img)
    return(circles)


def adjust_gamma(image, gamma=1):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invgamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


original = cv2.imread('dark_red_2.jpg', cv2.IMREAD_REDUCED_COLOR_2)

if hough(original, 0.4, h_min_red_bright04, h_max_red_bright04) is None:
    print('1st')
    if hough(original, 1.95, h_min_red_bright2, h_max_red_bright2) is None:
        hough(original, 3, h_min_red_bright27, h_max_red_bright27)
cv2.imshow('adj', original)
cv2.waitKey(0)
