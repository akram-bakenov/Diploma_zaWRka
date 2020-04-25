import numpy as np
import cv2

def nothing(x):
    pass

cv2.namedWindow( "trackbars" )   # window for trackbars
cv2.namedWindow( "webcam" ) # webcam window

cap = cv2.VideoCapture(0)     # webcam capture

cv2.createTrackbar('h1', 'trackbars', 0, 255, nothing)
cv2.createTrackbar('s1', 'trackbars', 0, 255, nothing)
cv2.createTrackbar('v1', 'trackbars', 0, 255, nothing)
cv2.createTrackbar('h2', 'trackbars', 255, 255, nothing)
cv2.createTrackbar('s2', 'trackbars', 255, 255, nothing)
cv2.createTrackbar('v2', 'trackbars', 255, 255, nothing)


while (cap.isOpened()):  # while true
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert

    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'trackbars')
    s1 = cv2.getTrackbarPos('s1', 'trackbars')
    v1 = cv2.getTrackbarPos('v1', 'trackbars')
    h2 = cv2.getTrackbarPos('h2', 'trackbars')
    s2 = cv2.getTrackbarPos('s2', 'trackbars')
    v2 = cv2.getTrackbarPos('v2', 'trackbars')

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)

    res = cv2.bitwise_and(frame, frame, mask=thresh)

    cv2.imshow('webcam', res)

    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release() # erases cap