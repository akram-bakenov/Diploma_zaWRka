from __future__ import print_function
import cv2
import numpy as np

# Red bright color
h_min_red_bright = np.array((0, 0, 109), np.uint8)
h_max_red_bright = np.array((183, 24, 161), np.uint8)

# Red color
h_min_red1 = np.array((0, 155, 174), np.uint8)
h_max_red1 = np.array((255, 183, 201), np.uint8)

# Red color
h_min_red = np.array((0, 88, 12), np.uint8)
h_max_red = np.array((14, 255, 255), np.uint8)

def steering_angle(img, center):
    # coefficient
    k = 0.091
    b = -29.14
    angle = (center[0] * k + b)
    if angle > 20:
        angle = 20
    elif angle < -20:
        angle = -20
    color_yellow = (2, 255, 5)
    cv2.putText(img, "Steering Angle = %ddeg" % (angle), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 3)

#
# # Blue color
# h_min_blue = np.array((97, 127, 0), np.uint8)
# h_max_blue = np.array((121, 255, 255), np.uint8)
#
# restriction of compilation if being imported
if __name__ == '__main__':

#     def hsv_filter(img, hsv, thresh):
#         print('HSV!!!')
#         contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#
#         # the biggest contour
#         c = max(contours, key=cv2.contourArea)
#
#         # rect = ((center_x,center_y),(width,height),angle)
#         rect = cv2.minAreaRect(c)
#
#         center = int(rect[0][0]), int(rect[0][1])
#
#         # little center circle
#         cv2.circle(img, center, 3, (0, 255, 0), 2)
#
#         # 4 corners to draw rectangle
#         b = cv2.boxPoints(rect)
#         b = np.int0(b)
#
#         cv2.drawContours(img, [b], 0, (0, 255, 0), 2)
#
#         cv2.imshow('HSV', img)

    def hough_circle(img):
        try:
            # img = cv2.imread('red_things.jpg', cv2.IMREAD_REDUCED_COLOR_2)

            # convert from BGR to HSV

            kernel = np.ones((7, 7), np.uint8)

            # applying colour filter (one channel)
            blur = cv2.GaussianBlur(img, (5, 5), 0)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(hsv, h_min_red, h_max_red)
            erode = cv2.erode(thresh, kernel)
            dilation = cv2.dilate(erode, kernel)
            cv2.imshow('dil', dilation)
            cv2.waitKey()
            cv2.imshow('hsv', thresh)
            cv2.waitKey()
            opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
            canny = cv2.Canny(image = thresh, threshold1 = 245, threshold2 = 255, apertureSize = 3, L2gradient = True)
            cv2.imshow('canny', canny)
            cv2.waitKey()
            circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=250, param2=20, minRadius=50, maxRadius=500)

            # search all circles
            for i in circles[0, :]:
                center = (i[0], i[1])
                # steering_angle(img, center)
                radius = i[2]
                # draw big cirlce
                cv2.circle(img, center, radius, (0, 255, 0), 3)
                # draw little circle
                cv2.circle(img, center, 1, (0, 255, 0), 5)
            res = cv2.bitwise_and(img, img, mask=thresh)
            cv2.imshow('Hough_circle', img)
        except TypeError:
            print('hsv')
            # hsv_filter(img, hsv, thresh)


    original = cv2.imread('red_things.jpg', cv2.IMREAD_REDUCED_COLOR_2)
    hough_circle(original)
    cv2.waitKey(0)

