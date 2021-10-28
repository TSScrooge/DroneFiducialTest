import cv2
import cv2.aruco as aruco
import numpy as np
import os

def findArucoMarkers(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    print(ids)

cap = cv2.VideoCapture('D:\workspace\Personale\Tesi\Video Drone\Aruco\Raw\DJI_0001.MP4')
counter = 0
while True:
    cap.set(1, counter)
    success, img = cap.read()
    findArucoMarkers(img)
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    counter += 30
cap.release()
cv2.destroyAllWindows()