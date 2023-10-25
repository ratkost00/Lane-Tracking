import cv2
import glob
import numpy as np

def colorFilterForLane(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    #mask for white
    lower = np.array([0, 0, 200])
    upper = np.array([255, 30, 255])
    maskW = cv2.inRange(hsv, lower, upper)
    # cv2.imshow('white mask', maskW)

    #mask for yellow color
    lower = np.array([10, 100, 100])
    upper = np.array([30, 255, 255])
    maskY = cv2.inRange(hsv, lower, upper)
    #cv2.imshow('yellow mask', mask)

    mask = cv2.bitwise_xor(maskW, maskY)

    filteredImage = cv2.bitwise_and(img, img, mask = mask)
    # cv2.imshow('hsv filtered', np.hstack((img, filteredImage)))
    #cv2.imshow('mask', mask)

    return filteredImage