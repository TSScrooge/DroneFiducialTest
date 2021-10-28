import cv2
import sys
import cv2.aruco as aruco
import srt
import re

START_H = 13.0
subtitles = []
BASE_VIDEO_PATH = "D:\workspace\Personale\Tesi\Video Drone\Aruco\Raw\DJI_0005"

class ascdescperiod:
    def __init__(self, start, end, h, speed, asc):
        self.start = start
        self.end = end
        self.h = h
        self.speed = speed
        self.asc = asc


def findArucoMarkers(img, h):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict1 = aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    arucoDict2 = aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoDict3 = aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    arucoDict4 = aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
    arucoDict5 = aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_50)
    arucoParam = aruco.DetectorParameters_create()
    arucoParam.maxMarkerPerimeterRate = 90
    arucoParam.minMarkerPerimeterRate = 0.002
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict1, parameters=arucoParam)
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict2, parameters=arucoParam)
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict3, parameters=arucoParam)
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict4, parameters=arucoParam)
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict5, parameters=arucoParam)
    cv2.putText(img, "{:.2f}".format(h)+"m", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 10, cv2.LINE_AA)
    if ids is not None and 1 in ids:
        cv2.putText(img, 'FOUND', (30, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 255, 0), 10, cv2.LINE_AA)
    return aruco.drawDetectedMarkers(img.copy(), bboxs, ids)

def initSrt():
    global subtitles
    srt_file_text = open(BASE_VIDEO_PATH+".SRT", 'r').read()
    subtitle_generator = srt.parse(srt_file_text)
    subtitles = list(subtitle_generator)

def calculateHeight(frameNo):
    regex = "(?<=\[altitude\:\ )(.*)(?=\])"
    result = re.search(regex, subtitles[frameNo].content)
    return float(result.group(1)) - START_H

initSrt()
vidcap = cv2.VideoCapture(BASE_VIDEO_PATH+".MP4")
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
count = 0
success = True
while success:
    vidcap.set(1, count)
    success, image = vidcap.read()
    h = calculateHeight(count)
    cv2.imwrite("framesRect30b/frame%d.jpg" % (count+9030), findArucoMarkers(image, h))
    count += 30
    print("{:.2f}".format(count / length * 100) + "%]")
