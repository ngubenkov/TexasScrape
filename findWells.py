import cv2
import numpy as np
from matplotlib import pyplot as plt

def searcWells():

    img_rgb = cv2.imread('screenshots/testScreenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('src/well.png',0)
    w, h = template.shape[::-1]
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for i in methods:
        res = cv2.matchTemplate(img_gray,template,eval(i))
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv2.imwrite('{}_res.png'.format(i),img_rgb)


if __name__ == "__main__":
    searcWells()