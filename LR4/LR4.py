import cv2 as cv
import numpy as np

def Kenny(image, size, sigma, low, high):
    img=cv.imread(image, cv.IMREAD_GRAYSCALE)
    blur=cv.GaussianBlur(img, (size, size), sigma)
    lengths=np.zeros(blur.shape)
    angles=np.zeros(blur.shape)

    for x in range (1,(len(blur)-1)):
        for y in range (1,len(blur[0])-1):
            Gx = blur[x+1][y+1]-blur[x-1][y-1]+blur[x+1][y-1]-blur[x-1][y+1]+2*(blur[x+1][y]-blur[x-1][y])
            Gy = blur[x + 1][y + 1] - blur[x - 1][y - 1] + blur[x - 1][y + 1] - blur[x + 1][y - 1] + 2 * (
                    blur[x][y + 1] - blur[x][y - 1])
            lengths[x][y]=np.sqrt(Gx*Gx+Gy*Gy)
            tan=np.arctan(Gy/Gx)
            if (0 < Gx and Gy < 0 and tan < -2.414) or (Gx < 0 and Gy < 0 and tan > 2.414):
                angles[x][y] = 0
            elif (Gx > 0 and Gy < 0 and tan < -0.414):
                angles[x][y] = 1
            elif (Gx > 0 and Gy < 0 and tan > -0.414) or (Gx > 0 and Gy > 0 and tan < 0.414):
                angles[x][y] = 2
            elif (Gx > 0 and Gy > 0 and tan < 2.414):
                angles[x][y] = 3
            elif (Gx > 0 and Gy > 0 and tan > 2.414) or (Gx < 0 and Gy > 0 and tan < -2.414):
                angles[x][y] = 4
            elif (Gx < 0 and Gy > 0 and tan < -0.414):
                angles[x][y] = 5
            elif (Gx < 0 and Gy > 0 and tan > -0.414) or (Gx < 0 and Gy < 0 and tan < 0.414):
                angles[x][y] = 6
            elif (Gx < 0 and Gy < 0 and tan < 2.414):
                angles[x][y] = 7


    filt=np.zeros(blur.shape)
    for x in range(1, (len(blur) - 1)):
        for y in range(1, len(blur[0]) - 1):
            ix = 0
            iy = 0
            if (angles[x][y] == 0):
                iy = -1
            if (angles[x][y] == 1):
                iy = -1
                ix = 1
            if (angles[x][y] == 2):
                ix = 1
            if (angles[x][y] == 3):
                iy = 1
                ix = 1
            if (angles[x][y] == 4):
                iy = 1
            if (angles[x][y] == 5):
                iy = 1
                ix = -1
            if (angles[x][y] == 6):
                ix = -1
            if (angles[x][y] == 7):
                iy = -1
                ix = -1
            if (lengths[x][y]>lengths[x+ix][y+iy] and lengths[x][y]>lengths[x-ix][y-iy]):
                    filt[x][y]=255
            else:
                    filt[x][y]=0

    max = np.max(lengths)
    lower=max//low
    higher=max//high
    for x in range(1, (len(blur) - 1)):
        for y in range(1, len(blur[0]) - 1):
            if(filt[x][y]==255):
                if(lengths[x][y]<lower):
                    filt[x][y]=0

    for x in range(1, (len(blur) - 1)):
        for y in range(1, len(blur[0]) - 1):
            if(filt[x][y]==255):
                if(lengths[x][y]<=higher):
                    if(filt[x-1][y-1]==255 or filt[x-1][y]==255 or filt[x-1][y+1]==255 or filt[x][y+1]==255 or filt[x+1][y+1]==255 or filt[x+1][y]==255 or filt[x+1][y-1]==255 or filt[x][y-1]==255):
                        filt[x][y] = 255
                    else:
                        filt[x][y] = 0

    cv.imshow('original', img)
    cv.imshow('blur', blur)
    cv.imshow("length",lengths)
    cv.imshow("angl",angles)
    cv.imshow("filtered",filt)
    cv.waitKey(0)
    cv.destroyAllWindows()
Kenny("LR3\kot.jpg", 3, 1, 1.1, 1.022)