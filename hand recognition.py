import cv2
from cvzone.HandTrackingModule import HandDetector

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(maxHands=2, detectionCon=0.8)


window_name = 'HandRec'
w, h = capture.get(3), capture.get(4)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, int(w * 1.5), int(h * 1.5))
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    _, img = capture.read()
    hands, img = detector.findHands(img)
    if hands:
        lmList = hands[0]['lmList']
        l, i, img = detector.findDistance(lmList[4], lmList[8], img)
        print(l)
        fingers = detector.fingersUp(hands[0])
        print(fingers)

    cv2.imshow(window_name, img)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
capture.release()
cv2.destroyAllWindows()