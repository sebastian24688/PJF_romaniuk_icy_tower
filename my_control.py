import cv2
import numpy as np

class Control:
    def __init__(self):
        self.lower_red = np.array([170, 120, 120], dtype=np.uint8)  # wrażliwość koloru
        self.upper_red = np.array([180, 255, 255], dtype=np.uint8)
        self.cap = cv2.VideoCapture(0)   # źródło video
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # pobranie rozmiaru obrazu
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.parts = 7  # podział ekranu na części
        self.part_width = self.frame_width // self.parts

        self.contours = None
        self.x = None

    def tick(self):
        ret, frame = self.cap.read()  # odczytanie ramki
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # zmiana formatu kolorów na hsv
        mask = cv2.inRange(hsv, self.lower_red, self.upper_red)  # maska koloru czerwonego
        mask = cv2.flip(mask, 1)
        self.contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # wyodrębnienie czerwonych obiektów

        # linie pomocnicze dzielące ekran
        for i in range(1, self.parts):
            cv2.line(mask, (i * self.part_width, 0), (i * self.part_width, self.frame_height), (255, 255, 255), 1)

        # Sprawdzenie położenia konturu położonego najbardziej na lewo
        self.x = self.frame_width
        for contour in self.contours:
            x_, y_, w_, h_ = cv2.boundingRect(contour)
            if x_ < self.x:
                self.x = x_ + w_/2

        # Zaznaczanie wykrytych obiektów na obrazie
        for contour in self.contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            cv2.circle(mask, (int(x), int(y)), int(radius), (255, 255, 255), 2)

        # Wyświetlanie ramki
        cv2.imshow('Wykryte czerwone koła', mask)

        # self.cap.release()
        # cv2.destroyAllWindows()

    def pozycja(self):
        if len(self.contours) == 0:
            # print("Brak wykrytego czerwonego koła. Obiekt jest w drugiej części")
            polozenie = 'S'

        if self.x < self.parts // 2 * self.part_width:
            polozenie = 'L'
            # print("Lewo")
        elif self.x < (self.parts // 2 + 1) * self.part_width:
            polozenie = 'S'
            # print("Środek")
        else:
            polozenie = 'P'
            # print("Prawo")

        return polozenie