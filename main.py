import numpy as np
import cv2


class Cartoonify:
    def __init__(self, bilateralIterations=5):
        self.iterations = bilateralIterations
        self.edges = None
        self.colored = None

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


img = cv2.imread('me.jpg')
cartoonify = Cartoonify(20)
edges = cartoonify.findEdges(img)
colors = cartoonify.findColors(img)

cartoon = cartoonify.cartoonify()
cv2.imshow('cartoon', cartoon)
cv2.waitKey(0)
