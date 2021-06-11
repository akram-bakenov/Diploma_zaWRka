import cv2
import numpy as np

IMG_PATH = "./data/me.JPG"
VIDEO_PATH = "./data/test_video.mp4"


def video_test(video):
    cap = cv2.VideoCapture(video)
    while (cap.isOpened()):
        _, vid = cap.read()
        # convert from BGR to GRAY
        grayscale_video = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        detected_video_faces = cascade_classifier_face_detection(grayscale_video)
        for (column, row, width, height) in detected_video_faces:
            cv2.rectangle(
                vid,
                (column, row),
                (column + width, row + height),
                (0, 255, 0),
                2
            )
        cv2.imshow('video', vid)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


    cap.release()



def cascade_classifier_face_detection(gray_img):
    '''
        Get numpy array with all detected faces on grayscaled image
        Use:
            haarcascade_frontalface_default
            haarcascade_frontalface_alt
    '''
    face_cascade = cv2.CascadeClassifier(
        './haarcascades/haarcascade_frontalface_default.xml'
    )
    detected_faces = face_cascade.detectMultiScale(gray_img)
    if detected_faces is ():
        print("NO FACES!")
    # face_cascade_alt = cv2.CascadeClassifier(
    #     './haarcascades/haarcascade_frontalface_alt.xml'
    # )
    # detected_alt_faces = face_cascade_alt.detectMultiScale(gray_img)
    # detected_faces = np.concatenate((detected_faces, detected_alt_faces))
    return detected_faces


def image_test(img):
    # Read image from your local file system
    original_image = cv2.imread(IMG_PATH, cv2.IMREAD_REDUCED_COLOR_4)
    # Convert color image to grayscale for Viola-Jones
    grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    detected_faces = cascade_classifier_face_detection(grayscale_image)
    for (column, row, width, height) in detected_faces:

        cv2.rectangle(
            original_image,
            (column, row),
            (column + width, row + height),
            (0, 255, 0),
            2
        )
    cv2.imshow('Image', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    image_test(IMG_PATH)
    video_test(VIDEO_PATH)