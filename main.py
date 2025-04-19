import mediapipe as mp
import cv2

camera = cv2.VideoCapture(0)

mpHands=  mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

p = [0 for i in range(21)]              # создаем массив из 21 ячейки для хранения высоты каждой точки
finger = [0 for i in range(5)]
def distance(point1, point2):
    return abs(point1 - point2)

while True:
    good, img = camera.read()
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    results = hands.process(imgrgb)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, point in enumerate(handLms.landmark):
                # получаем размеры изображения с камеры и масштабируем
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)
                p[id] = height
            distanceGood = distance(p[0], p[5]) + (distance(p[0], p[5]) / 2)
        # заполняем массив 1 (палец поднят) или 0 (палец сжат)
            finger[1] = 1 if distance(p[0], p[8]) > distanceGood else 0
            finger[2] = 1 if distance(p[0], p[12]) > distanceGood else 0
            finger[3] = 1 if distance(p[0], p[16]) > distanceGood else 0
            finger[4] = 1 if distance(p[0], p[20]) > distanceGood else 0
            finger[0] = 1 if distance(p[0], p[4]) > distanceGood else 0

            if  not(finger[1]) and not (finger[2]) and not (finger[3]) and not(finger[4]) :
                cv2.putText(img,'А',(20,50),cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255))
            if finger[1] and finger[2] and finger[3] and finger[4] :
                cv2.putText(img, 'В', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
            if finger[1] and  finger[2] and not (finger[3]) and not (finger[4]) :
                cv2.putText(img, 'К', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
            if finger[1] and finger[2] and not(finger[3]) and finger[4]:
                 cv2.putText(img, 'Н', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
            if finger[1] and not (finger[2]) and finger[3] and finger[4]:
                 cv2.putText(img, 'Р', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
            if not(finger[1]) and not(finger[2]) and not(finger[3]) and finger[4]:
                 cv2.putText(img, 'У', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
            if finger[1] and finger[2] and finger[3] and not(finger[4]):
                cv2.putText(img, 'Ш', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
            if finger[1] and not (finger[2]) and not (finger[3]) and finger[4]:
                cv2.putText(img, 'Ы', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord(' '):
        break