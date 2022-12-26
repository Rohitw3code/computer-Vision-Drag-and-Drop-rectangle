import math
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(maxHands=1,detectionCon=0.8)

color = (255,0,255)

cx,cy,w,h = 100,100,200,200

def findDistance(p1,p2,img):
    disColor = (255,146,51)
    x1, y1 = p1[:2]
    x2, y2 = p2[:2]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)
    info = (x1, y1, x2, y2, cx, cy)
    if img is not None:
        cv2.circle(img, (x1, y1), 15, disColor, cv2.FILLED)
        cv2.circle(img, (x2, y2), 15,disColor, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2),disColor, 3)
        cv2.circle(img, (cx, cy), 15,disColor, cv2.FILLED)
        return length, info, img
    else:
        return length, info

class DrawRect():
    def __init__(self,posCenter,size=(100,100)):
        self.posCenter = posCenter
        self.size = size
        self.rectColor = (18,156,243)
        self.color = self.rectColor

    def update(self,cursor):
        cx, cy = self.posCenter
        w, h = self.size
        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor
            self.color = (0,255,0)


fingerDistance = 40

rectList = []
numberOfRect = 10
for x in range(numberOfRect):
    rectList.append(DrawRect([x * 150 + 10, 150]))

while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hand,img = detector.findHands(img)

    if hand:
        lmList = hand[0]["lmList"]
        l = findDistance(lmList[8],lmList[12],img)
        print(lmList)
        if lmList:
            if l[0] < fingerDistance:
                cursor = lmList[8]
                cx, cy = cursor[:2]
                for rec in rectList:
                    rec.update(cursor[:2])
            else:
                for rec in rectList:
                    rec.color = rec.rectColor

    # To Draw Rect
    for rec in rectList:
        cx, cy = rec.posCenter
        w, h = rec.size
        color = rec.color
        cv2.rectangle(img, (cx-w//2, cy-h//2),(cx+w//2,cy+h//2),color, cv2.FILLED)

    cv2.imshow("Image",img)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
