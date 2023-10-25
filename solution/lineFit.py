import numpy as np
import cv2
import matplotlib.pyplot as plt

def lineFit(img):
    hist = np.sum(img[img.shape[0]//2:, :], axis=0)
    # cv2.imshow('hist', hist)
    output = (np.dstack((img, img, img))*255).astype('uint8')

    cv2.imshow('out', output)

    midpoint = np.int32(hist.shape[0]/2)
    leftx_base = np.argmax(hist[100:midpoint]) + 100
    rightx_base = np.argmax(hist[midpoint:-100]) + midpoint
    print('left base: ' + str(leftx_base))
    print('right base: ' + str(rightx_base))