import cv2
print(cv2.__version__)
# Открываем видеофайл
video_path = 'IW1\motion_video.mp4'  # Укажите путь к вашему видео
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: не удалось открыть видео.")
    exit()

ret, frame = cap.read()
if not ret:
    print("Ошибка: не удалось прочитать первый кадр.")
    exit()

bbox = cv2.selectROI("Выберите объект для трекинга", frame, fromCenter=False, showCrosshair=True)

# Создаем трекер MedianFlow
tracker = cv2.legacy.TrackerMedianFlow_create()
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, bbox = tracker.update(frame)

    if success:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        cv2.putText(frame, "Объект не найден", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Трекинг объектов", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()