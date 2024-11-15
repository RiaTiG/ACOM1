import cv2 as cv2
import numpy as np

# Задание 1-2
# img1 = cv2.imread('AdMech.png',cv2.IMREAD_GRAYSCALE)
# img2 = cv2.imread('AdMech.png',cv2.IMREAD_REDUCED_COLOR_4)
# img3 = cv2.imread('AdMech.png',cv2.IMREAD_ANYCOLOR)
# cv2.namedWindow('Display1',cv2.WINDOW_NORMAL)
# cv2.namedWindow('Display2',cv2.WINDOW_FULLSCREEN)
# cv2.namedWindow('Display3',cv2.WINDOW_FREERATIO)
# cv2.imshow('Display3',img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Задание 3
# cap = cv2.VideoCapture('o-velikiy-sup-navarili.mp4',cv2.CAP_ANY)
# while True:
#     ret, frame = cap.read()
#     if not(ret):
#         break
#     gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame',gray)
#     #cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()

# Задание 4
# cap = cv2.VideoCapture("video.mp4",cv2.CAP_ANY)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video_writer = cv2.VideoWriter("output.mp4", fourcc, 25, (width, height))
# while True:
#     ret, frame = cap.read()
#     if not(ret):
#         break
#     cv2.imshow('frame',frame)
#     video_writer.write(frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()

# Задание 5
# img = cv2.imread("AdMech.png",cv2.IMREAD_COLOR)
# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# cv2.imshow('original_frame',img)
# cv2.imshow('hsv_frame',hsv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Задание 6
# cap=cv2.VideoCapture(0)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))/2
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))/2
# size = 100

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     points1 = np.array([[width, height - size],
#         [width - size * np.sqrt(3)/2, height + size/2],
#         [width + size * np.sqrt(3)/2, height + size/2]], np.int32)
#     points2 = np.array([[width, height + size],
#         [width - size * np.sqrt(3)/2, height - size/2],
#         [width + size * np.sqrt(3)/2, height - size/2]], np.int32)
#     cv2.polylines(frame,[points1, points2], isClosed=True, color=(255, 0, 0), thickness=5)

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()

# Задание 7
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('motion_video.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# Задание 8
# cap=cv2.VideoCapture(0)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))//2
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))//2
# size = 100

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     points1 = np.array([[width, height - size],
#         [width - size * np.sqrt(3)/2, height + size/2],
#         [width + size * np.sqrt(3)/2, height + size/2]], np.int32)
#     points2 = np.array([[width, height + size],
#         [width - size * np.sqrt(3)/2, height - size/2],
#         [width + size * np.sqrt(3)/2, height - size/2]], np.int32)
#     cv2.polylines(frame,[points1, points2], isClosed=True, color=(255, 0, 0), thickness=5)

#     center_pixel = frame[height, width]
#     r, g, b = center_pixel
#     if r > g and r > b:
#         star_color = (0, 0, 255)  
#     elif g > r and g > b:
#         star_color = (0, 255, 0)  
#     else:
#         star_color = (255, 0, 0)  

#     cv2.fillPoly(frame, [points1], star_color)
#     cv2.fillPoly(frame, [points2], star_color)
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()

#Задание 9
# cap=cv2.VideoCapture("rtsp://192.168.1.64:8080/h264_pcm.sdp")
# while True:
#     ret, frame = cap.read()
#     if not(ret):
#         break
#     cv2.imshow('mp4',frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

