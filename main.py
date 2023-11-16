import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
posicion_jugador = set()
posiciones_ganadoras = [
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9},
    {1, 4, 7},
    {2, 5, 8},
    {3, 6, 9},
    {1, 5, 9},
    {3, 5, 7}
]
juegaX = True
pnt = [False, False, False, False, False, False, False, False, False]


def getFinger(hand_landmarks):
    lms = hand_landmarks.landmark
    return lms[8]


def decidePosition(point):
    if 0 <= abs(point.x) <= 0.33 and 0 <= abs(point.y) <= 0.33:
        return 1
    elif 0.34 <= abs(point.x) <= 0.66 and 0 <= abs(point.y) <= 0.33:
        return 2
    elif 0.67 <= abs(point.x) <= 1 and 0 <= abs(point.y) <= 0.33:
        return 3
    elif 0 <= abs(point.x) <= 0.33 and 0.34 <= abs(point.y) <= 0.66:
        return 4
    elif 0.34 <= abs(point.x) <= 0.66 and 0.34 <= abs(point.y) <= 0.66:
        return 5
    elif 0.67 <= abs(point.x) <= 1 and 0.34 <= abs(point.y) <= 0.66:
        return 6
    elif 0 <= abs(point.x) <= 0.33 and 0.67 <= abs(point.y) <= 1:
        return 7
    elif 0.34 <= abs(point.x) <= 0.66 and 0.67 <= abs(point.y) <= 1:
        return 8
    elif 0.67 <= abs(point.x) <= 1 and 0.67 <= abs(point.y) <= 1:
        return 9


def dibujaX(num, ptn):
    if num == 1:
        pnt[0] = True
    elif num == 2:
        pnt[1] = True
    elif num == 3:
        pnt[2] = True
    elif num == 4:
        pnt[3] = True
    elif num == 5:
        pnt[4] = True
    elif num == 6:
        pnt[5] = True
    elif num == 7:
        pnt[6] = True
    elif num == 8:
        pnt[7] = True
    elif num == 9:
        pnt[8] = True


while True:
    success, image = cap.read()
    image = cv2.resize(image, (300, 300))
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    # <editor-fold desc="grilla<
    image = cv2.line(image, (100, 0), (100, 300), (0, 0, 0), 1)
    image = cv2.line(image, (200, 0), (200, 300), (0, 0, 0), 1)
    image = cv2.line(image, (0, 100), (300, 100), (0, 0, 0), 1)
    image = cv2.line(image, (0, 200), (300, 200), (0, 0, 0), 1)

    if pnt[0] is True:
        image = cv2.line(image, (5, 5), (95, 95), (0, 0, 255), 2)
        image = cv2.line(image, (5, 95), (95, 5), (0, 0, 255), 2)
    if pnt[1] is True:
        image = cv2.line(image, (105, 5), (195, 95), (0, 0, 255), 2)
        image = cv2.line(image, (105, 95), (195, 5), (0, 0, 255), 2)
    if pnt[2] is True:
        image = cv2.line(image, (205, 5), (295, 95), (0, 0, 255), 2)
        image = cv2.line(image, (205, 95), (295, 5), (0, 0, 255), 2)
    if pnt[3] is True:
        image = cv2.line(image, (5, 105), (95, 195), (0, 0, 255), 2)
        image = cv2.line(image, (5, 195), (95, 105), (0, 0, 255), 2)
    if pnt[4] is True:
        image = cv2.line(image, (105, 105), (195, 195), (0, 0, 255), 2)
        image = cv2.line(image, (105, 195), (195, 105), (0, 0, 255), 2)
    if pnt[5] is True:
        image = cv2.line(image, (205, 105), (295, 195), (0, 0, 255), 2)
        image = cv2.line(image, (205, 195), (295, 105), (0, 0, 255), 2)
    if pnt[6] is True:
        image = cv2.line(image, (5, 205), (95, 295), (0, 0, 255), 2)
        image = cv2.line(image, (5, 295), (95, 205), (0, 0, 255), 2)
    if pnt[7] is True:
        image = cv2.line(image, (105, 205), (195, 295), (0, 0, 255), 2)
        image = cv2.line(image, (105, 295), (195, 205), (0, 0, 255), 2)
    if pnt[8] is True:
        image = cv2.line(image, (205, 205), (295, 295), (0, 0, 255), 2)
        image = cv2.line(image, (205, 295), (295, 205), (0, 0, 255), 2)
    # </editor-fold<

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for _id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if _id == 8:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

            # if juegaX:
                f = getFinger(handLms)
                if f is not None:
                    p = decidePosition(f)
                    posicion_jugador.add(p)
                    dibujaX(p, pnt)
                for x in range(len(posiciones_ganadoras)):
                    if posiciones_ganadoras[x].issubset(posicion_jugador):
                        print("Gano")
                # juegaX = not juegaX

    cv2.imshow("Output", image)
    key = cv2.waitKey(1)
