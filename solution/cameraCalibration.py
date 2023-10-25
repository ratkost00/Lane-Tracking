import numpy as np
import cv2
import glob
import os

def calculateCameraCoeffs(rows, cols, imgPath):
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
    objectPoints = np.zeros((rows * cols, 3), np.float32)
    objectPoints[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2)
    objectPointsArray = []
    imgPointsArray = []
    count = 0

    for path in glob.glob(imgPath):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        count += 1
        ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)
        if ret:
            # print("ret condition")
            # Refine the corner position
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Add the object points and the image points to the arrays
            objectPointsArray.append(objectPoints)
            imgPointsArray.append(corners)

            # Draw the corners on the image
        # name = "image" + str(count)
            cv2.drawChessboardCorners(img, (rows, cols), corners, ret)
        # cv2.imshow(name, gray)
        # cv2.imshow('ches_board', gray)
        cv2.waitKey(20)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPointsArray, imgPointsArray, gray.shape[::-1], None, None)
    error = 0

    for i in range(len(objectPointsArray)):
        imgPoints, _ = cv2.projectPoints(objectPointsArray[i], rvecs[i], tvecs[i], mtx, dist)
        error += cv2.norm(imgPointsArray[i], imgPoints, cv2.NORM_L2) / len(imgPoints)

    print("Total error: ", error / len(objectPointsArray))

    return ret, mtx, dist, rvecs, tvecs

def undistortImage(imgPath, output, mtx, dist):
    count = 0
    for path in glob.glob(imgPath):
        #os.chdir(imgPathAbs)
        # print(path)
        count += 1
        img = cv2.imread(path)
        h, w = img.shape[:2]

        # Obtain the new camera matrix and undistort the image
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        undistortedImg = cv2.undistort(img, mtx, dist, None, newCameraMtx)

        filename = output + '/' + path.split('/')[-1]

        # Display the final result
        # cv2.imshow('chess board', undistortedImg)
        #filename = 'undistorted' + str(count) + '.jpg'
        #print(filename)
        #os.chdir(destPath)
        cv2.imwrite(filename, undistortedImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()