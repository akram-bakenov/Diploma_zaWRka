import cv2
import numpy as np


# Red color
h_min_red = np.array((0, 137, 167), np.uint8)
h_max_red = np.array((9, 206, 245), np.uint8)

# Blue color
h_min_blue = np.array((97, 127, 0), np.uint8)
h_max_blue = np.array((121, 255, 255), np.uint8)


def hsv_filter(img, hsv, thresh):
    print('HSV!!!')
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # the biggest contour
    c = max(contours, key=cv2.contourArea)

    # rect = ((center_x,center_y),(width,height),angle)
    rect = cv2.minAreaRect(c)

    center = int(rect[0][0]), int(rect[0][1])

    # little center circle
    cv2.circle(img, center, 3, (0, 255, 0), 2)

    # 4 corners to draw rectangle
    b = cv2.boxPoints(rect)
    b = np.int0(b)

    cv2.drawContours(img, [b], 0, (0, 255, 0), 2)

    cv2.imshow('HSV', img)

def hough_circle():
    try:
        img = cv2.imread('blue_circle_far.jpg', cv2.IMREAD_REDUCED_COLOR_2)

        # convert from BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # applying colour filter (one channel)
        thresh = cv2.inRange(hsv, h_min_blue, h_max_blue)

        blur = cv2.GaussianBlur(thresh, (3, 3), 0)
        canny = cv2.Canny(image = blur, threshold1 = 245, threshold2 = 255, apertureSize = 3, L2gradient = True)
        circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=300, param1=250, param2=20, minRadius=10, maxRadius=300)

        # search all circles
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            # draw big cirlce
            cv2.circle(img, center, radius, (0, 255, 0), 2)
            # draw little circle
            cv2.circle(img, center, 1, (0, 255, 0), 2)

        cv2.imshow('Hough_circle', img)
    except TypeError:
        hsv_filter(img, hsv, thresh)


hough_circle()

cv2.waitKey(0)
