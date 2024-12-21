import cv2
import numpy as np

image = cv2.imread('C:/ACOM/LR3/kot.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gauss(size, sigma: float):
    size = abs(size)
    ker = np.zeros((size, size))
    a = size // 2 + 1 
    b = size // 2 + 1

    for x in range(size):
        for y in range(size):
            ker[x, y] = (1 / (2 * np.pi * sigma ** 2)) * np.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sigma ** 2))
    return ker

# Вывод матриц
sigma = 0.1
val = [3, 5, 7]
for size in val:
    ker = gauss(size, sigma)
    norm_ker = ker / np.sum(ker)
    print(f"Матрица {size}*{size} :\n{ker}\n")
    print(f"Нормированная {size}*{size} :\n{norm_ker}\n")

def filter(image, size, sigma:float):
    size = abs(size)
    ker = gauss(size, sigma)
    norm_ker = ker / np.sum(ker)
    image_copy = image.copy()
    mean = size // 2 +1
    h = image_copy.shape[0]
    w = image_copy.shape[1]
    test = np.zeros_like(image)
    
    for i in range(h):
        for j in range(w):
            sum = 0
            for k in range(-mean, mean + 1):
                for l in range(-mean, mean + 1):
                    sum += image_copy[i + k, j + l] * norm_ker[k + mean, l + mean]
            image_copy[i, j] = sum     
    return image_copy

result = filter(gray, 5, 1.0)
gauss_cv = cv2.GaussianBlur(gray, (5, 5), 1.0)
cv2.imshow('Filter', result)
cv2.imshow('FilterCV2', gauss_cv)
cv2.imshow('Image', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()