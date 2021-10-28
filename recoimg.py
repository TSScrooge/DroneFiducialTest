import time

import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import numpy as np
import os

def findArucoMarkers(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    arucoDict = aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParam = aruco.DetectorParameters_create()
    # arucoParam.minDistanceToBorder = 7
    # arucoParam.cornerRefinementMaxIterations = 149
    # arucoParam.minOtsuStdDev = 4.0
    # arucoParam.adaptiveThreshWinSizeMin = 7
    # arucoParam.adaptiveThreshWinSizeStep = 49
    # arucoParam.minMarkerDistanceRate = 0.014971725679291437
    arucoParam.maxMarkerPerimeterRate = 90
    arucoParam.minMarkerPerimeterRate = 0.001
    arucoParam.polygonalApproxAccuracyRate = 0.1
    # arucoParam.cornerRefinementWinSize = 9
    # arucoParam.adaptiveThreshConstant = 9.0
    # arucoParam.adaptiveThreshWinSizeMax = 369
    # arucoParam.minCornerDistanceRate = 0.09167132584946237
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    print(ids)
    markerToDraw = aruco.drawDetectedMarkers(frame.copy(), bboxs)
    cv2.imwrite("view.png", markerToDraw)

frame = cv2.imread("framesRect30b/frame14040.jpg")
findArucoMarkers(frame)