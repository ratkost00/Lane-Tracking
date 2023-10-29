import cv2
import numpy as np

def findROI(img, path):
    mask = np.zeros_like(img)
    height, width = img.shape[:2]

    # print('height' + str(height))
    roiVert = [(width/2 - 50, height/2 + 70), (200, height), (width - 80, height), (width/2 + 50, height/2 + 70)]
    # roiVert = [(0, height), (0, height - 50), (width/2 - 50, height/2 + 50), (width/2 + 50, height/2 + 50), (width, height-50), (width, height)]


    blackColor = 255
    cv2.fillPoly(mask, np.array([roiVert], dtype=np.int32), blackColor)
    maskedImg = cv2.bitwise_and(img, mask)

    # src = np.float32([[100, height], [width/2 - 50, height/2 + 50], [width/2 + 50, height/2 + 50], [width - 80, height]])
    # dst = np.float32([[300, 720], [980, 720], [300, 0], [980, 0]])

    src = np.float32([[width/2 + 20, height/2 + 60], [300, height],  [width - 150,  height], [width/2 + 50, height/2 + 60]])
    dst = np.float32([[width/4 , 0], [width/4 , height], [width/4*3, height],  [width/4*3 , 0]])
    if width == 1280 and height == 720:
        # print('hd image')
        src = np.float32([[540, 450], [200, height],  [1150,  height], [720, 450]])
        dst = np.float32([[width/4 , 0], [width/4 , height], [width/4*3, height],  [width/4*3 , 0]])
    elif width == 960 and height == 540:
        # print('less than hd image')
        src = np.float32([[430, 350], [200, height],  [890, height], [590, 350]])
        dst = np.float32([[width/4 , 0], [width/4 , height], [width/4*3, height],  [width/4*3 , 0]])

    pt = cv2.getPerspectiveTransform(src, dst)
    ptInv = cv2.getPerspectiveTransform(dst, src)
    # print(pt)

    warped = cv2.warpPerspective(img, pt, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
    unwarped = cv2.warpPerspective(warped, ptInv, (warped.shape[1], warped.shape[0]), flags=cv2.INTER_LINEAR)

    # cv2.imshow('warped', warped)
    # cv2.imshow(path, np.hstack((warped, unwarped)))
    # cv2.imshow('roi', maskedImg)
    return warped, unwarped

def invWarp(img):
    height, width = img.shape[:2]
    src = np.float32([[width/2 + 20, height/2 + 60], [300, height],  [width - 150,  height], [width/2 + 50, height/2 + 60]])
    dst = np.float32([[width/4 , 0], [width/4 , height], [width/4*3, height],  [width/4*3 , 0]])
    if width == 1280 and height == 720:
        # print('hd image')
        src = np.float32([[540, 450], [200, height],  [1150,  height], [720, 450]])
        dst = np.float32([[width/4 , 0], [width/4 , height], [width/4*3, height],  [width/4*3 , 0]])
    elif width == 960 and height == 540:
        # print('less than hd image')
        src = np.float32([[430, 350], [200, height],  [890, height], [590, 350]])
        dst = np.float32([[width/4 , 0], [width/4 , height], [width/4*3, height],  [width/4*3 , 0]])

    ptInv = cv2.getPerspectiveTransform(dst, src)
    unwarped = cv2.warpPerspective(img, ptInv, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
    return unwarped