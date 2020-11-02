import cv2
import numpy as np


cv2.namedWindow("webcam")

# webcam capture
cap = cv2.VideoCapture(0)

# Blue color
h_min = np.array((97, 127, 0), np.uint8)
h_max = np.array((121, 255, 255), np.uint8)

while (cap.isOpened()):
    _, frame = cap.read()

    # convert from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # applying colour filter
    thresh = cv2.inRange(hsv, h_min, h_max)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # the biggest contour
    c = max(contours, key = cv2.contourArea)

    # rect = ((center_x,center_y),(width,height),angle)
    rect = cv2.minAreaRect(c)

    center = int(rect[0][0]), int(rect[0][1])

    # little center circle
    cv2.circle(frame, center, 3, (0, 255, 0), 2)

    # 4 corners to draw rectangle
    b = cv2.boxPoints(rect)
    b = np.int0(b)

    cv2.drawContours(frame, [b], 0, (0, 255, 0), 2)

    cv2.imshow('webcam', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


