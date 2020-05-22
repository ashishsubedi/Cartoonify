import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default="me.jpg", help="Path to the image")
ap.add_argument("-r", "--realtime", action='store_true',
                help="Put this if you want to cartoonify webcam feed")
args = vars(ap.parse_args())


class Cartoonify:
    def __init__(self, bilateralIterations=5):
        self.iterations = bilateralIterations
        self.edges = None
        self.colored = None
        self.H = 640
        self.W = 480

    def resize(self, img, size):
        self.H, self.W, self.n_C = img.shape
        return cv2.resize(img, size)

    def findEdges(self, img):
        '''Find Edges of an image'''
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 2)
        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 31, 11)

        self.edges = img

        return img

    def findColors(self, img):
        '''Find linear colors in an image'''
        for _ in range(self.iterations):
            img = cv2.bilateralFilter(img, 5, 50, 50)
        self.colored = img
        return img

    def cartoonify(self):
        '''Cartoonify the image'''
        if(not self.edges is None and not self.colored is None):
            return cv2.bitwise_and(self.colored, self.colored, mask=self.edges)
        else:
            raise Exception('No edged and colored images found')


def cartoonify_live():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        if not ret:
            break

        cartoonify = Cartoonify(30)

        edges = cartoonify.findEdges(img)
        colors = cartoonify.findColors(img)

        cartoon = cartoonify.cartoonify()

        cv2.imshow('cartoon', cartoon)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def cartoonify_img(img):
    cartoonify = Cartoonify(10)

    edges = cartoonify.findEdges(img)
    colors = cartoonify.findColors(img)

    cartoon = cartoonify.cartoonify()
    cv2.imshow('cartoon', cartoon)
    cv2.waitKey(0)


if __name__ == "__main__":
    if(args['realtime']):
        cartoonify_live()
    else:
        img = cv2.imread(args['image'])
        cartoonify_img(img)
