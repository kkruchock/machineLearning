import cv2
import random

video_path = r"C:\Users\Дмитрий\Downloads\sample-5s-360p.mp4"  # видео с ноута (без r надо париться с экранированием)

# открываем видко
capture = cv2.VideoCapture(video_path)
# получаем параметры
w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = capture.get(cv2.CAP_PROP_FPS)

# создаем видео с теми же параметрами
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h))

while True:
    # есть ли кадр, сам кадр
    ret, frame = capture.read()
    # конец
    if not ret:
        break
    # рандомная позиция
    x = random.randint(0, w - 50)
    y = random.randint(0, h - 50)
    frame[y:y + 50, x:x + 50] = [255, 255, 255]  # белый квадрат
    # записываем квадрат
    out.write(frame)

capture.release()
out.release()

#показ видео
result_video = cv2.VideoCapture('output.mp4')

while True:
    ret, frame = result_video.read()
    if not ret:
        break

    # Показываем кадр в окне
    cv2.imshow('Результат: белые квадраты', frame)

    # Ждем 30 мс. Если нажата ESC (код 27) - выходим
    if cv2.waitKey(30) == 27:  # 27 = ESC
        break

result_video.release()
cv2.destroyAllWindows()