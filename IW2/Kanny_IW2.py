import cv2
import numpy as np

# image = cv2.imread('IW1\MPT_1.jpg', cv2.IMREAD_GRAYSCALE) # идеал - threshold1=50, threshold2=100
# image = cv2.imread('C:\ACOM\IW1\MPT_2.jpg', cv2.IMREAD_GRAYSCALE) # идеал - threshold1=50, threshold2=250
image = cv2.imread('C:\ACOM\IW1\MPT_3.jpg', cv2.IMREAD_GRAYSCALE) # идеал - threshold1=50, threshold2=100
# image = cv2.imread('C:\ACOM\IW1\MPT_4.jpg', cv2.IMREAD_GRAYSCALE) # идеал - threshold1=50, threshold2=270
# image = cv2.imread('C:\ACOM\IW1\MPT_5.jpg', cv2.IMREAD_GRAYSCALE) # идеал - threshold1=100, threshold2=200(250)


# Предобработка: выравнивание контраста с помощью гистограммы (но мы об это не скажем)
image_eq = cv2.equalizeHist(image)
blurred = cv2.GaussianBlur(image, (3, 3), 1)

# Gauss ___
# blurred2 = cv2.GaussianBlur(image, (3, 3), 1)
# cv2.imwrite('3x3.png', blurred2)
# blurred3 = cv2.GaussianBlur(image, (5, 5), 1)
# cv2.imwrite('5x5.png', blurred3)
# blurred4 = cv2.GaussianBlur(image, (7, 7), 1)
# cv2.imwrite('7x7.png', blurred4)

# Применение алгоритма Канни
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
# 4. Нормализация значений результата лапласиана в диапазон (0, 255)
laplacian_normalized = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX)
laplacian_normalized = np.uint8(laplacian_normalized)

# 5. Применение порогового преобразования для выделения границ
# Пороговые значения 40 и 255 можно настроить:
_, thresholded_laplacian = cv2.threshold(laplacian, 5, 30, cv2.THRESH_BINARY)


# cv2.imwrite('50-150.png', edges)
# ---------------------------------------------------------------------------------
# МОРФОЛОГИЧЕСКАЯ ОБРАБОТКА  (можно нахуй делетнуть, я просто игрался)
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=2)
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filled_mask = np.zeros_like(image)
cv2.drawContours(filled_mask, contours, -1, (255), thickness=cv2.FILLED)
highlights = cv2.bitwise_and(image, image, mask=filled_mask)
# ---------------------------------------------------------------------------------

cv2.imshow('Original', image)
cv2.imshow('Границы засветов (Канни)', edges)
# cv2.imwrite('Laplacian3.jpg', thresholded_laplacian)
# cv2.imshow('Detection', highlights)5
cv2.waitKey(0)
cv2.destroyAllWindows()
