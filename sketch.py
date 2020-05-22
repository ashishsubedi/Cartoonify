import numpy as np
import cv2
import argparse

'''
    1) Convert to grayscale
    2) Invert the image
    3) Blur using Gaussian filter
    4) Divide original by blurred image

'''

ap = argparse.ArgumentParser()
ap.add_argument('-r', '--realtime', action='store_true',
                help="Use this flag if you want to sketch realtime using default webcam")
ap.add_argument('-i', '--image', default="me.jpg",
                help="Path to the image")
args = vars(ap.parse_args())


def sketch(image, realTime=False):
    # gray = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    gray = cv2.filter2D(gray, -1, kernel_sharpening)

    blurred = cv2.GaussianBlur(gray, (21, 21), 5, sigmaY=5)

    ITERATIONS = 5 if realTime else 15
    for _ in range(ITERATIONS):

        blurred = cv2.bilateralFilter(blurred, 21, 150, 150)

    divided = dodge(gray, blurred)

    return divided


def dodge(gray, blurred):
    return cv2.divide(gray, blurred, scale=256)


def sketch_live():
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        ret = True
        while(ret):
            ret, frame = cap.read()

            img = cv2.resize(frame, (300, 300))
            img = sketch(frame, True)
            img = cv2.resize(img, (frame.shape[1], frame.shape[0]))
            cv2.imshow("Sketch using threshold", img)
            if cv2.waitKey(1) == 27:
                break

    cv2.destroyAllWindows()
    cap.release()


def sketch_image(imgPath):

    img = cv2.imread(imgPath)
    sketched = sketch(img)
    cv2.imshow("Sketch", sketched)
    cv2.waitKey(0)


if __name__ == "__main__":
    if(args['realtime']):
        sketch_live()
    else:
        sketch_image(args['image'])
