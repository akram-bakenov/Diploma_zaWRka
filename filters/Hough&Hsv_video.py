import cv2
import numpy as np


if __name__ == '__main__':
    # webcam window
    cv2.namedWindow("webcam")

    # webcam capture
    cap = cv2.VideoCapture(0)

    # Red color
    h_min_red = np.array((0, 88, 12), np.uint8)
    h_max_red = np.array((14, 255, 255), np.uint8)

    # Blue color
    h_min_blue = np.array((97, 127, 0), np.uint8)
    h_max_blue = np.array((121, 255, 255), np.uint8)

    # Green color
    h_min_green = np.array((65, 77, 69), np.uint8)
    h_max_green = np.array((84, 255, 136), np.uint8)

    def hsv_filter(img, hsv):
        print('HSV!!!')
        # applying colour filter (one channel)
        thresh = cv2.inRange(hsv, h_min_green, h_max_green)

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

        #cv2.imshow('HSV', img)

    def hough_circle(img):
        try:

            # convert from BGR to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            kernel = np.ones((5, 5), np.uint8)

            # applying colour filter (one channel)
            thresh = cv2.inRange(hsv, h_min_red, h_max_red)

            blur = cv2.GaussianBlur(thresh, (3, 3), 0)
            erode = cv2.erode(blur, kernel)
            dilation = cv2.dilate(blur, kernel)
            canny = cv2.Canny(image = dilation, threshold1 = 245, threshold2 = 255, apertureSize = 3, L2gradient = True)
            circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=250, param2=20, minRadius=20, maxRadius=500)
            # cv2.imshow("HSV", img)
            # print(np.shape(circles))
            # search all circles
            for i in circles[0, :]:
                center = (i[0], i[1])
                # coefficient
                k = 0.091
                b = -29.14
                angle = (center[0]*k + b)
                if angle > 20:
                    angle = 20
                if angle < -20:
                    angle = -20
                color_yellow = (0, 255, 255)
                cv2.putText(img, "Steering Angle = %d" % (angle), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
                radius = i[2]
                # draw big cirlce
                cv2.circle(img, center, radius, (0, 255, 0), 2)
                # draw little circle
                cv2.circle(img, center, 1, (0, 255, 0), 2)

            # cv2.imshow('Hough_circle', img)
        except TypeError:
            # hsv_filter(img, hsv)

            print('999')

    while (cap.isOpened()):
        _, img = cap.read()
        hough_circle(img)
        cv2.imshow('webcam', img)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cv2.destroyAllWindows()
    # erases cap
    cap.release()