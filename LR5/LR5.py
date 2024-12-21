import cv2

def main(path_to_file, kernel_size, standart_deviation, treshLow, min_area):
    video = cv2.VideoCapture(path_to_file, cv2.CAP_ANY)
    ret, frame = video.read()
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    outputVideo = cv2.VideoWriter("new_test_video.mp4", fourcc, 25, (width, height))

    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    oldFrame = cv2.GaussianBlur(gray, (kernel_size, kernel_size), standart_deviation)
    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurGray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), standart_deviation)
        frame_diff = cv2.absdiff(oldFrame, blurGray)
        thresh = cv2.threshold(frame_diff, treshLow, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            contour = contours[0]
            area = cv2.contourArea(contour)
            if area > min_area:
                outputVideo.write(frame)
        except:
            pass

        oldFrame = blurGray
    outputVideo.release()

main("C:\ACOM\LR5\ЛР4_main_video.mov", 3, 60, 120, 20)