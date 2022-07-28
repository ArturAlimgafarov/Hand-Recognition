import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui as pag

def checkInsideFrame(x, y, t, l, r, d):
    return (l < x < r) and (t < y < d)

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(maxHands=2, detectionCon=0.8)

# windows & frames
scale = 0.4
screenWidth, screenHeight = pag.size()
frameWidth, frameHeight = screenWidth * scale, screenHeight * scale
capWidth, capHeight = capture.get(3), capture.get(4)

# resize
windowName = 'Mouse Control'
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
cv2.resizeWindow(windowName, int(capWidth / 2), int(capHeight / 2))

smoothening = 5
curX, curY = 0, 0
prevX, prevY = 0, 0

while True:
    _, img = capture.read()

    # center of image
    cX, cY = int(capWidth // 2), int(capHeight // 2) - 70

    # frame rectangle coordinates
    top = int(cY - frameHeight // 2)
    left = int(cX - frameWidth // 2)
    right = int(cX + frameWidth // 2)
    down = int(cY + frameHeight // 2)

    # add frame to image
    img = cv2.rectangle(img, (left, top), (right, down), (0, 255, 255), 2)

    hands, _ = detector.findHands(img.copy())
    if hands:
        if hands[0]['type'] == 'Right':
            lmList = hands[0]['lmList']
            x, y = lmList[8] # index finger
            if (checkInsideFrame(x, y, top, left, right, down)):
                # show finger
                img = cv2.circle(img, (x, y), 8, (255, 255, 255), -1)

                # convert coordinates
                mouseX, mouseY = int(screenWidth - (x - left) / scale), int((y - top) / scale)
                # pag.moveTo(mouseX, mouseY)
                curX = prevX + (mouseX - prevX) / smoothening
                curY = prevY + (mouseY - prevY) / smoothening

                pag.moveTo(curX, curY)

                prevX, prevY = curX, curY

            fingers = detector.fingersUp(hands[0])
            if fingers[1] == 1 and fingers[2] == 1:
                dist, info, _ = detector.findDistance(lmList[12], lmList[8], img.copy())
                if dist < 40:
                    pag.click()

    # mirror view
    img = cv2.flip(img, 1)

    # resize
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, int(capWidth / 2), int(capHeight / 2))

    # output
    cv2.imshow(windowName, img)

    # 'Escape' key for exit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
capture.release()
cv2.destroyAllWindows()