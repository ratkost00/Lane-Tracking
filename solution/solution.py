# Calibrate camera
# ROI
# Binary image
# Filter if neded
# Edge detection
# Perspective transformation
# Filter if neded
# Lane detection, curvature radius, center offset
import numpy as np
import cv2
import glob
import roi
import matplotlib.pyplot as plt

import cameraCalibration as cc
import hsvSpace as hs
import lineFit as lf
import videoLoad as vl
import imageHist as ih


rows = 6
cols = 9
imgPath = '../camera_cal/calibration*'
imgPathAbs = '/home/rstikovic/Documents/dosivuav/Zadatak/camera_cal'
destPath = '/home/rstikovic/Documents/dosivuav/Zadatak/solution/undistorted'
testImgPath = '../test_images/*'
testImgUndistPath = '../test_images_undistorted/*'
testVideosPath = '../test_videos/project_video*'
# testVideosPath = '../test_videos/challenge03*'


print("solutions ")

def imageProcessing(img):
    # hsv color filter - filter out everything except yellow and white
        hsimage = hs.colorFilterForLane(img)

        # get gray scale image
        gray = cv2.cvtColor(hsimage, cv2.COLOR_BGR2GRAY)

        # apply gaussian blur
        blured = cv2.GaussianBlur(gray, (7, 7), 0)

        edges = cv2.Canny(blured, 200, 230)



        ret, binary = cv2.threshold(edges, 200, 255, cv2.THRESH_BINARY)
        # print(binary)

        # roided like a mike o hearn
        warped, unwarped = roi.findROI(binary, path)

        # calculate histogram for warped image
        #ih.calculateImageHist(warped)
        out_img, curves, lanes, ploty = ih.sliding_window(warped)
        curv = ih.get_curve(img, curves[0], curves[1])


        lines = cv2.HoughLinesP(unwarped, rho=6, theta=np.pi/60, threshold=1)

        linedImage = np.zeros_like(img)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(linedImage, (x1, y1), (x2, y2), (255, 0, 0), 1)
        markedLines = cv2.addWeighted(img, 0.8, linedImage, 1, 0)

        # cv2.imshow('img', binary)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #warped, unwarped = roi.findROI(img, path)


        return unwarped, warped, lines, markedLines, binary, out_img


if __name__ == "__main__":
    ret, mtx, dist, rvecs, tvecs = cc.calculateCameraCoeffs(rows, cols, imgPath)
    #cc.undistortImage(imgPath, mtx, dist)

    # Undistort test images
    cc.undistortImage(testImgPath, testImgUndistPath, mtx, dist)

    for path in glob.glob(testImgUndistPath):
        img = cv2.imread(path)

        # hsv color filter - filter out everything except yellow and white
        hsimage = hs.colorFilterForLane(img)

        # get gray scale image
        gray = cv2.cvtColor(hsimage, cv2.COLOR_BGR2GRAY)

        # apply gaussian blur
        blured = cv2.GaussianBlur(gray, (3, 3), 0)

        edges = cv2.Canny(blured, 10, 200)

        # roided like a mike o hearn
        warped, unwarped = roi.findROI(edges, path)

        # lf.lineFit(warped)


        #cv2.imshow(path, warped)
        #cv2.imshow('path', unwarped)
        # cv2.imshow('img', img)
        #cv2.waitKey(0)
        # cv2.destroyAllWindows()

    count = 0
    for path in glob.glob(testVideosPath):
        cap = cv2.VideoCapture(path)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                unw, wr, lines, markedLines, binary, outImg = imageProcessing(frame)

                cv2.imshow(path, outImg)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
