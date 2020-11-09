from __future__ import print_function
import cv2
import numpy as np
import serial


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invgamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def serial_data(angle):
    ser = serial.Serial('COM1', baudrate=115200, timeout=1)
    # first 4 bytes for angle
    ser.write(angle)
    # second 4 bytes for speed
    ser.write(angle)
    print(ser)


def steering_angle(center):
    # coefficient
    k = 0.091
    b = -29.14
    angle = (center[0] * k + b)
    if angle > 20:
        angle = 20
    elif angle < -20:
        angle = -20
    color_yellow = (0, 0, 255)
    cv2.putText(img, "Steering Angle = %ddeg" % (angle), (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
    print(angle)

def hsv_filter(img, hsv):
    print('HSV!!!')
    # applying colour filter (one channel)
    thresh = cv2.inRange(hsv, h_min_green, h_max_green)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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


def gamma_hough(img, gamma, h_min, h_max):
    adjusted = adjust_gamma(img, gamma=gamma)
    hsv1 = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv1, h_min, h_max)
    kernel = np.ones((5, 5), np.uint8)
    blur = cv2.GaussianBlur(thresh, (3, 3), 0)
    erode = cv2.erode(blur, kernel)
    dilation = cv2.dilate(erode, kernel)
    canny = cv2.Canny(image = dilation, threshold1 = 5, threshold2 = 130, apertureSize = 3, L2gradient = True)
    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=700, param1=250, param2=10, minRadius=10, maxRadius=70)
    print(circles)
    if circles is not None:
        # search all circles
        for i in circles[0, :]:
            center = (i[0], i[1])
            # steering_angle(img, center)
            radius = i[2]
            # draw big cirlce
            cv2.circle(img, center, radius, (0, 255, 0), 3)
            # draw center circle
            cv2.circle(img, center, 1, (0, 255, 0), 5)
            steering_angle(center)
            cv2.putText(img, "gamma coef.={}".format(gamma), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        # res = cv2.bitwise_and(adjusted, adjusted, mask=thresh)
    return(circles)


def hough_circle(hsv, min, max):

    # applying colour filter (one channel) ...
    thresh = cv2.inRange(hsv, min, max)

    kernel = np.ones((5, 5), np.uint8)

    blur = cv2.GaussianBlur(thresh, (3, 3), 0)
    erode = cv2.erode(blur, kernel)
    dilation = cv2.dilate(blur, kernel)

    canny = cv2.Canny(image=erode, threshold1=245, threshold2=255, apertureSize=3, L2gradient=True)
    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=1000, param1=250, param2=20, minRadius=10, maxRadius=100)
    print(circles)
    if circles is not None:
        # search all circles
        for i in circles[0, :]:
            center = (i[0], i[1])
            steering_angle(center)
            cv2.putText(img, "gamma coef. = 1", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            radius = i[2]
            # draw big cirlce
            cv2.circle(img, center, radius, (0, 255, 0), 2)
            # draw little circle
            cv2.circle(img, center, 1, (0, 255, 0), 2)
    return (circles)


if __name__ == '__main__':

    # webcam capture
    cap = cv2.VideoCapture(0)

    # Red color
    h_min_red = np.array((0, 47, 0), np.uint8)
    h_max_red = np.array((22, 255, 255), np.uint8)

    # Red bright color
    h_min_red_bright = np.array((0, 0, 109), np.uint8)
    h_max_red_bright = np.array((183, 24, 161), np.uint8)

    # Red bright color
    h_min_red_bright04 = np.array((0, 0, 29), np.uint8)
    h_max_red_bright04 = np.array((216, 49, 65), np.uint8)

    # Red dark color
    h_min_red_bright2 = np.array((63, 0, 46), np.uint8)
    h_max_red_bright2 = np.array((255, 255, 255), np.uint8)

    while (cap.isOpened()):
        _, img = cap.read()
        # convert from BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if hough_circle(hsv, h_min_red, h_max_red) is None:
            if gamma_hough(img, 0.4, h_min_red_bright04, h_max_red_bright04) is None:
                gamma_hough(img, 2, h_min_red_bright2, h_max_red_bright2)

        cv2.imshow('webcam', img)
        k = cv2.waitKey(1)
        if k == 27:
            break

    # erases cap
    cap.release()
    cv2.destroyAllWindows()