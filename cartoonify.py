import numpy as np
import cv2
import argparse
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default="me.jpg", help="Path to the image")
ap.add_argument("-r", "--realtime", action='store_true',
                help="Put this if you want to cartoonify webcam feed")
ap.add_argument('-o', '--output', default="cartoon.jpg",
                help="Path to save the image with filename")
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
        print("Finding Edges", end='\r', flush=True)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 7, 55, 175)

        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 13, 9)
        self.edges = img

        print("Finding Edges... Done", flush=True)

        return img

    def findColors(self, img):
        '''Find linear colors in an image'''

        for _ in range(self.iterations):
            img = cv2.bilateralFilter(img, 5, 40, 40)

        self.colored = img
        return img

    def findColorsV2(self, img, K=16):
        '''Find Colors by dividing into subcubes'''
        print("Finding Color", end='\r', flush=True)

        img = cv2.bilateralFilter(img, 11, 75, 150)

        Z = img.reshape((-1, 3))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        ret, label, center = cv2.kmeans(
            Z, K, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res = res.reshape((img.shape))
        print("Finding Color... Done", flush=True)

        self.colored = res
        return img

    def cartoonify(self):
        '''Cartoonify the image'''
        print("Cartoonifying Image", end='\r', flush=True)
        sys.stdout.flush()
        if(not self.edges is None and not self.colored is None):
            print("Cartoonifying Image... Done", flush=True)

            return cv2.bitwise_and(self.colored, self.colored, mask=self.edges)
        else:
            raise Exception('No edged and colored images found')


def cartoonify_live():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        if not ret:
            break

        cartoonify = Cartoonify(10)

        edges = cartoonify.findEdges(img)
        colors = cartoonify.findColors(img)

        cartoon = cartoonify.cartoonify()

        cv2.imshow('cartoon', cartoon)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def cartoonify_img(img):
    cartoonify = Cartoonify(30)

    edges = cartoonify.findEdges(img)
    # colors = cartoonify.findColors(img)
    colors = cartoonify.findColorsV2(img, 16)

    cartoon = cartoonify.cartoonify()
    cv2.imwrite(args['output'], cartoon)
    print('Saved to '+args['output'])
    cv2.imshow('cartoon', cartoon)
    cv2.waitKey(0)


if __name__ == "__main__":
    if(args['realtime']):
        cartoonify_live()
    else:
        img = cv2.imread(args['image'])
        cartoonify_img(img)
