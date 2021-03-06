import cv2
import numpy as np

# здесь может быть узкое место, т.к. сейчас пороговые значения у тебя 
# это константы, т.е. если что-то изменится - освещение, положение или
# добавятся объекты, то настройки могут поплыть. 
# Это основная проблема с которой борются в компьютерном зрении. 
# пока что предлагаю оставить это так, но если спросят (а скорее всего спросят)
# то сказать, что пока что мы расскатриваем упрощённые условия, 
# с постоянным освещение и окружением 

# Red color
h_min_red = np.array((0, 137, 167), np.uint8)
h_max_red = np.array((9, 206, 245), np.uint8)

# Blue color
h_min_blue = np.array((97, 127, 0), np.uint8)
h_max_blue = np.array((121, 255, 255), np.uint8)

def hsv_filter(img, hsv, thresh):
        print('HSV!!!')
        # Почему ты используешь thresh.copy() ? 
        # можно ведь просто thresh из аргументов? 
        # вроде copy() - это поверхностное копирование, т.е. 
        # это ссылка на объект, а не настоящая его копия
        # есть ещё deepcopy() - это настоящая копия
        # Но тем не менее, не вижу смысла здесь это использовать (=
        # contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # А если вообще контуров не обнаружится на картинке? 
        # Может добавить проверку? 
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
        canny = cv2.Canny(image = blur, threshold1 = 245,
                          threshold2 = 255, apertureSize = 3,
                          L2gradient = True)
        circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT,
                                   dp=1, minDist=300, param1=250,
                                   param2=20, minRadius=10, maxRadius=300)

        # Что если кругов вообще не надётся? Также, лучше проверку запилить
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

# restriction of compilation if being imported 
if __name__ == '__main__': 
    hough_circle()

    cv2.waitKey(0)
