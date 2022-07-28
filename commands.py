import sys
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class WebBrowserApp(QMainWindow):
    def __init__(self):
        super(WebBrowserApp, self).__init__()
        self.webEngineView = QWebEngineView(self)
        self.setCentralWidget(self.webEngineView)

    def start(self, link):
        url = QUrl.fromUserInput(link)
        self.webEngineView.setUrl(url)
        if url.isValid():
            self.webEngineView.load(url)

import cv2
from cvzone.HandTrackingModule import HandDetector

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(maxHands=2, detectionCon=0.8)

while True:
    _, img = capture.read()
    hands, img = detector.findHands(img)
    if hands:
        lmList = hands[0]['lmList']
        fingers = detector.fingersUp(hands[0])
        print(fingers)

        l, _, _ = detector.findDistance(lmList[4], lmList[8], img)
        print(l)
        if fingers == [0, 0, 1, 1, 1] and l < 15:
            break

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()

# import webbrowser
# webbrowser.open_new_tab('https://google.com')

from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('C:/Users/ARTURIO/Desktop/python/parser/web bot/chromedriver/chromedriver.exe')
driver.get("http://google.com")
sleep(4)
driver.execute_script("window.open('http://vk.com','_blank');")
driver.execute_script("window.close('','_blank');")
driver.execute_script("window.open('','_blank');")
sleep(2)
driver.close()

# app = QApplication(sys.argv)
# ex = WebBrowserApp()
# ex.start('google.com')
# ex.setWindowTitle('Web Browser')
# ex.resize(800, 600)
# # ex.show()
# ex.showMaximized()
# print(ex.isActiveWindow())
# app.exec_()
# print(ex.isActiveWindow())
#sys.exit(app.exec_())