import cv2
import mediapipe as mp

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


def getFinger(hand_landmarks):
    lms = hand_landmarks.landmark
    return lms[8]


def decidePosition(point):
    if 0 <= abs(point.x) >= 0.33 and 0 <= abs(point.y) >= 0.33:
        return 1
    elif 0.34 <= abs(point.x) >= 0.66 and 0 <= abs(point.y) >= 0.33:
        return 2
    elif 0.67 <= abs(point.x) >= 1 and 0 <= abs(point.y) >= 0.33:
        return 3
    elif 0 <= abs(point.x) >= 0.33 and 0.34 <= abs(point.y) >= 0.66:
        return 4
    elif 0.34 <= abs(point.x) >= 0.66 and 0.34 <= abs(point.y) >= 0.66:
        return 5
    elif 0.67 <= abs(point.x) >= 1 and 0.34 <= abs(point.y) >= 0.66:
        return 6
    elif 0 <= abs(point.x) >= 0.33 and 0.67 <= abs(point.y) >= 1:
        return 7
    elif 0.34 <= abs(point.x) >= 0.66 and 0.67 <= abs(point.y) >= 1:
        return 8
    elif 0.67 <= abs(point.x) >= 1 and 0.67 <= abs(point.y) >= 1:
        return 9


while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    # <editor-fold desc="grilla>
    image = cv2.resize(image, (300, 300))
    image = cv2.line(image, (100, 0), (100, 300), (0, 0, 0), 1)
    image = cv2.line(image, (200, 0), (200, 300), (0, 0, 0), 1)
    image = cv2.line(image, (0, 100), (300, 100), (0, 0, 0), 1)
    image = cv2.line(image, (0, 200), (300, 200), (0, 0, 0), 1)
    # </editor-fold>

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for _id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if _id == 8:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

            f = getFinger(handLms)
            print(f.x, f.y)
            print(decidePosition(f))
            # if f is not None:
                # posicion_jugador.add(decidePosition(f))
            for x in range(len(posiciones_ganadoras)):
                if posiciones_ganadoras[x].issubset(posicion_jugador):
                    print("Gano")

                # print(posicion_jugador)

    cv2.imshow("Output", image)
    key = cv2.waitKey(1)
