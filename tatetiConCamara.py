import random
import cv2
import mediapipe as mp
import time

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
tiempo_en_posicion = 0
posicion_actual = None
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
turnoJugador = True
juegoTerminado = False

class Jugada:
    def __init__(self, usado=False, player="ninguno"):
        self.usado = usado
        self.player = player

# Array con 9 jugadas, seteadas en default, que es usado en false y player ninguno
jugadas = [Jugada() for _ in range(9)]

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

def dibujaX(num, jugadas_a_dibujar):
    if num == 1:
        jugadas_a_dibujar[0].usado = True
        jugadas_a_dibujar[0].player = "humano"
    elif num == 2:
        jugadas_a_dibujar[1].usado = True
        jugadas_a_dibujar[1].player = "humano"
    elif num == 3:
        jugadas_a_dibujar[2].usado = True
        jugadas_a_dibujar[2].player = "humano"
    elif num == 4:
        jugadas_a_dibujar[3].usado = True
        jugadas_a_dibujar[3].player = "humano"
    elif num == 5:
        jugadas_a_dibujar[4].usado = True
        jugadas_a_dibujar[4].player = "humano"
    elif num == 6:
        jugadas_a_dibujar[5].usado = True
        jugadas_a_dibujar[5].player = "humano"
    elif num == 7:
        jugadas_a_dibujar[6].usado = True
        jugadas_a_dibujar[6].player = "humano"
    elif num == 8:
        jugadas_a_dibujar[7].usado = True
        jugadas_a_dibujar[7].player = "humano"
    elif num == 9:
        jugadas_a_dibujar[8].usado = True
        jugadas_a_dibujar[8].player = "humano"

def dibujaO(num, jugadas_a_dibujar):
    if num == 1:
        jugadas_a_dibujar[0].usado = True
        jugadas_a_dibujar[0].player = "IA"
    elif num == 2:
        jugadas_a_dibujar[1].usado = True
        jugadas_a_dibujar[1].player = "IA"
    elif num == 3:
        jugadas_a_dibujar[2].usado = True
        jugadas_a_dibujar[2].player = "IA"
    elif num == 4:
        jugadas_a_dibujar[3].usado = True
        jugadas_a_dibujar[3].player = "IA"
    elif num == 5:
        jugadas_a_dibujar[4].usado = True
        jugadas_a_dibujar[4].player = "IA"
    elif num == 6:
        jugadas_a_dibujar[5].usado = True
        jugadas_a_dibujar[5].player = "IA"
    elif num == 7:
        jugadas_a_dibujar[6].usado = True
        jugadas_a_dibujar[6].player = "IA"
    elif num == 8:
        jugadas_a_dibujar[7].usado = True
        jugadas_a_dibujar[7].player = "IA"
    elif num == 9:
        jugadas_a_dibujar[8].usado = True
        jugadas_a_dibujar[8].player = "IA"

def esGanador(jugador):
    for conjunto in posiciones_ganadoras:
        if all(jugadas[i - 1].player == jugador for i in conjunto):
            return True
    return False

def jugadaIA():
    casillas_disponibles = [i + 1 for i, jugada in enumerate(jugadas) if not jugada.usado]
    if casillas_disponibles:
        casilla_ia = random.choice(casillas_disponibles)
        dibujaO(casilla_ia, jugadas)

while True:
    success, image = cap.read()
    image = cv2.resize(image, (300, 300))
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    image = cv2.line(image, (100, 0), (100, 300), (0, 0, 0), 1)
    image = cv2.line(image, (200, 0), (200, 300), (0, 0, 0), 1)
    image = cv2.line(image, (0, 100), (300, 100), (0, 0, 0), 1)
    image = cv2.line(image, (0, 200), (300, 200), (0, 0, 0), 1)

    #Codigo horrendooooooooooo (pero anda) para que dibuje las cosas!
    if jugadas[0].usado is True and jugadas[0].player == "humano":
        image = cv2.line(image, (5, 5), (95, 95), (0, 0, 255), 2)
        image = cv2.line(image, (5, 95), (95, 5), (0, 0, 255), 2)
    elif jugadas[0].usado is True and jugadas[0].player == "IA":
        image = cv2.circle(image, (50, 50), 50, (255, 0, 0), 2)
    if jugadas[1].usado is True and jugadas[1].player == "humano":
        image = cv2.line(image, (105, 5), (195, 95), (0, 0, 255), 2)
        image = cv2.line(image, (105, 95), (195, 5), (0, 0, 255), 2)
    elif jugadas[1].usado is True and jugadas[1].player == "IA":
        image = cv2.circle(image, (150, 50), 50, (255, 0, 0), 2)
    if jugadas[2].usado is True and jugadas[2].player == "humano":
        image = cv2.line(image, (205, 5), (295, 95), (0, 0, 255), 2)
        image = cv2.line(image, (205, 95), (295, 5), (0, 0, 255), 2)
    elif jugadas[2].usado is True and jugadas[2].player == "IA":
        image = cv2.circle(image, (250, 50), 50, (255, 0, 0), 2)
    if jugadas[3].usado is True and jugadas[3].player == "humano":
        image = cv2.line(image, (5, 105), (95, 195), (0, 0, 255), 2)
        image = cv2.line(image, (5, 195), (95, 105), (0, 0, 255), 2)
    elif jugadas[3].usado is True and jugadas[3].player == "IA":
        image = cv2.circle(image, (50, 150), 50, (255, 0, 0), 2)
    if jugadas[4].usado is True and jugadas[4].player == "humano":
        image = cv2.line(image, (105, 105), (195, 195), (0, 0, 255), 2)
        image = cv2.line(image, (105, 195), (195, 105), (0, 0, 255), 2)
    elif jugadas[4].usado is True and jugadas[4].player == "IA":
        image = cv2.circle(image, (150, 150), 50, (255, 0, 0), 2)
    if jugadas[5].usado is True and jugadas[5].player == "humano":
        image = cv2.line(image, (205, 105), (295, 195), (0, 0, 255), 2)
        image = cv2.line(image, (205, 195), (295, 105), (0, 0, 255), 2)
    elif jugadas[5].usado is True and jugadas[5].player == "IA":
        image = cv2.circle(image, (250, 150), 50, (255, 0, 0), 2)
    if jugadas[6].usado is True and jugadas[6].player == "humano":
        image = cv2.line(image, (5, 205), (95, 295), (0, 0, 255), 2)
        image = cv2.line(image, (5, 295), (95, 205), (0, 0, 255), 2)
    elif jugadas[6].usado is True and jugadas[6].player == "IA":
        image = cv2.circle(image, (50, 250), 50, (255, 0, 0), 2)
    if jugadas[7].usado is True and jugadas[7].player == "humano":
        image = cv2.line(image, (105, 205), (195, 295), (0, 0, 255), 2)
        image = cv2.line(image, (105, 295), (195, 205), (0, 0, 255), 2)
    elif jugadas[7].usado is True and jugadas[7].player == "IA":
        image = cv2.circle(image, (150, 250), 50, (255, 0, 0), 2)
    if jugadas[8].usado is True and jugadas[8].player == "humano":
        image = cv2.line(image, (205, 205), (295, 295), (0, 0, 255), 2)
        image = cv2.line(image, (205, 295), (295, 205), (0, 0, 255), 2)
    elif jugadas[8].usado is True and jugadas[8].player == "IA":
        image = cv2.circle(image, (250, 250), 50, (255, 0, 0), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for _id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if _id == 8:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                f = getFinger(handLms)
                if f is not None and turnoJugador:
                    p = decidePosition(f)
                    if p is not None and (jugadas[p - 1].usado or jugadas[p - 1].player == "IA"):
                        continue  # Casilla ya ocupada.

                if p != posicion_actual:
                    tiempo_en_posicion = time.time()
                    posicion_actual = p

                    # Verificar pasaste 3 segundos en la misma posición
                elif time.time() - tiempo_en_posicion >= 3 and f is not None and turnoJugador and not juegoTerminado:
                    p = decidePosition(f)
                    if p is not None and jugadas[p - 1].usado:
                        continue  # Casilla ya ocupada, no se puede
                    if p is not None:
                        posicion_jugador.add(p)
                        dibujaX(p, jugadas)
                        turnoJugador = False
                        tiempo_en_posicion = 0
                        posicion_actual = None

    if not turnoJugador and not juegoTerminado:
        jugadaIA()
        turnoJugador = True

    #chequea el ganador y termina  la partida
    if esGanador("humano"):
        cv2.putText(image, "Ganaste", (85, 150), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)
        juegoTerminado = True
        print("¡Ganaste!")
    elif esGanador("IA"):
        cv2.putText(image, "Gana la IA", (50, 150), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)
        juegoTerminado = True
        print("¡Gana la IA!")

    cv2.imshow("Output", image)
    key = cv2.waitKey(1)