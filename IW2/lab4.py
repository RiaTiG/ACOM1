import cv2
import numpy as np

# задание 1

# def Cam():
#
#     image = cv2.imread('D:\draw\iz2\people5.jpg',cv2.IMREAD_GRAYSCALE)
#
#     kernl = (7,7)
#     sigma = 1;
#     razm = cv2.GaussianBlur(image,kernl,sigma)
#
#     cv2.namedWindow('Blurring',cv2.WINDOW_KEEPRATIO)
#     cv2.imshow('Blurring',razm)
#
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# Cam()

# задание 2

def Cam():


    image = cv2.imread('C:\ACOM\IW1\MPT_3.jpg',cv2.IMREAD_GRAYSCALE)
    kernl = (7,7)
    sigma = 1
    size = 3
    razm = cv2.GaussianBlur(image,kernl,sigma)

    cv2.namedWindow('Blurring',cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Blurring',razm)

    sobX = cv2.Sobel(razm, cv2.CV_64F, 1, 0, ksize=3)
    sobY = cv2.Sobel(razm, cv2.CV_64F, 0, 1, ksize=3)

    #матрица значений длин

    G = np.sqrt(sobX**2 + sobY**2)

    #матрица значений углов

    corner = np.atan(sobY, sobX)
    corner_2 = np.arctan2(sobY,sobX)


    cv2.namedWindow('gradient', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('gradient', sobX)
    cv2.namedWindow('Corner', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Corner', corner)

    # задание 3

    row,col = G.shape
    corner2 = np.zeros((row,col))
    BW = np.zeros((row, col), dtype=np.uint8)
    BW2 = np.zeros((row, col), dtype=np.uint8)

    for i in range(1, row - 1):
        for j in range(1, col - 1):
            if (sobX[i, j] < 0 and sobY[i, j] < 0 and np.tan(corner[i, j]) < -2.414) or (sobY[i, j] < 0 and sobX[i, j] < 0 and np.tan(corner[i, j]) > 2.414):
                if (sobX[i, j] < 1 and sobY[i, j] < 0 and np.tan(corner[i, j]) < -0.414):
                    BW[i, j] = G[i, j]

            elif (2 - sobX[i, j] > 0 and sobY[i, j] < 0 and np.tan(corner[i, j]) < -0.414) or (sobY[i, j] > 0 and sobX[i, j] > 0 and np.tan(corner[i, j]) < 0.414):
                if (3 - sobX[i, j] > 0 and sobY[i, j] > 0 and np.tan(corner[i, j]) < 2.414):
                    BW[i, j] = G[i, j]

            elif (4 - sobX[i, j] > 0 and sobY[i, j] < 0 and np.tan(corner[i, j]) > 2.414) or (sobY[i, j] > 0 and sobX[i, j] < 0 and np.tan(corner[i, j]) < -2.414):
                if (sobY[i, j] > 0 and 5 - sobX[i, j] < 0 and np.tan(corner[i, j]) < -0.414):
                    BW[i, j] = G[i, j]

            elif (sobY[i, j] > 0 and 6 - sobX[i, j] < 0 and np.tan(corner[i, j]) > -0.414) or (sobY[i, j] < 0 and sobX[i, j] < 0 and np.tan(corner[i, j]) < 0.414):
                if (sobY[i, j] < 0 and 7 - sobX[i, j] < 0 and np.tan(corner[i, j]) < 2.414):
                    BW[i, j] = G[i, j]

    for i in range(1, row):
        for j in range(1, col):
            # Получаем угол градиента
            corner2[i, j] = corner_2[i, j] * 180.0 / np.pi


            # Направление градиента
            if 0 <= corner2[i, j] < 22.5 or 157.5 <= corner2[i, j] < 202.5 or corner2[i, j] >= 337.5:
                corner2[i, j] = 0
            elif 22.5 <= corner2[i, j] < 67.5 or 202.5 <= corner2[i, j] < 247.5:
                corner2[i, j] = 45
            elif 67.5 <= corner2[i, j] < 112.5 or 247.5 <= corner2[i, j] < 292.5:
                corner2[i, j] = 90
            elif 112.5 <= corner2[i, j] < 157.5 or 292.5 <= corner2[i, j] < 337.5:
                corner2[i, j] = 135

    for i in range(1, row - 1):
        for j in range(1, col - 1):
            if corner2[i, j] == 0:
                if G[i,j] >= G[i,j + 1] and G[i,j] >= G[i,j - 1]:
                    BW2[i, j] = G[i,j]
            elif corner2[i, j] == 45:
                if G[i,j] >= G[i + 1,j + 1] and G[i,j] >= G[i - 1,j - 1]:
                    BW2[i, j] = G[i, j]
            elif corner2[i, j] == 90:
                if G[i, j] >= G[i + 1, j] and G[i, j] >= G[i - 1, j]:
                    BW2[i, j] = G[i, j]
            elif corner2[i, j] == 135:
                if G[i, j] >= G[i - 1, j + 1] and G[i, j] >= G[i + 1, j - 1]:
                    BW2[i, j] = G[i, j]

    cv2.namedWindow('No-max-LK', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('No-max-LK', BW)

    # for i in range(1, row-1):
    #     for j in range(1, col-1):
    #         # Получаем угол градиента
    #         corn = corner_2[i, j] * 180.0 / np.pi
    
    
    #         # Направление градиента
    #         if 0 <= corn < 22.5 or 157.5 <= corn < 202.5 or corn >= 337.5:
    #             if G[i, j] >= G[i, j + 1] and G[i, j] >= G[i, j - 1]:
    #                 BW[i, j] = G[i,j]
    #         elif 22.5 <= corn < 67.5 or 202.5 <= corn < 247.5:
    #             if G[i,j] >= G[i + 1,j + 1] and G[i,j] >= G[i - 1,j - 1]:
    #                 BW[i, j] = G[i, j]
    #         elif 67.5 <= corn < 112.5 or 247.5 <= corn < 292.5:
    #             if G[i, j] >= G[i + 1, j] and G[i, j] >= G[i - 1, j]:
    #                 BW[i, j] = G[i, j]
    #         elif 112.5 <= corn < 157.5 or 292.5 <= corn < 337.5:
    #             if G[i, j] >= G[i - 1, j + 1] and G[i, j] >= G[i + 1, j - 1]:
    #                 BW[i, j] = G[i, j]

    # cv2.namedWindow('No-max', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('No-max', BW)

    # rows, cols = G.shape

    # image = np.zeros((rows, cols), dtype=np.uint8)

    # for i in range(1, rows - 1):
    #     for j in range(1, cols - 1):
    #         angle = corner_2[i, j] * 180.0 / np.pi

    #         right = 255.0
    #         left = 255.0

    #         if 0 <= angle < 22.5 or 157.5 <= angle < 202.5 or angle >= 337.5:
    #             right = G[i, j + 1]
    #             left = G[i, j - 1]
    #         elif 22.5 <= angle < 67.5 or 202.5 <= angle < 247.5:
    #             right = G[i + 1, j + 1]
    #             left = G[i - 1, j - 1]
    #         elif 67.5 <= angle < 112.5 or 247.5 <= angle < 292.5:
    #             right = G[i + 1, j]
    #             left = G[i - 1, j]
    #         elif 112.5 <= angle < 157.5 or 292.5 <= angle < 337.5:
    #             right = G[i - 1, j + 1]
    #             left = G[i + 1, j - 1]

    #         if G[i, j] >= right and G[i, j] >= left:
    #             image[i, j] = G[i, j]

    # cv2.namedWindow('No-max-mod', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('No-max-mod', image)



    max_grad = np.max(G)

    low_level = 30
    high_level = 40
    threshold = np.zeros((row, col), dtype= np.uint8)

    for i in range(1, row):
        for j in range(1, col):
            if BW[i, j] >= high_level:
                threshold[i, j] = 255
            elif BW[i, j] >= low_level and BW[i, j] < high_level:
                if BW[i + 1, j] >= high_level or BW[i - 1, j] >= high_level or BW[i, j + 1] >= high_level or BW[i, j - 1] >= high_level or BW[i + 1, j + 1] >= high_level or BW[i - 1, j - 1] >= high_level or BW[i + 1, j - 1] >= high_level or BW[i - 1, j + 1] >= high_level:
                    threshold[i, j] = 255

    cv2.namedWindow('Double_TH', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Double_TH', threshold)
    # cv2.imwrite('1-3x3.png', threshold)
    # cv2.imwrite('3-3x3.png', threshold)
    cv2.imwrite('1-7x7.png', threshold)
    # cv2.imwrite('3-7x7.png', threshold)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

Cam()