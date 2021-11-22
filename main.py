import cv2
import sys
import cv2.aruco as aruco
from apriltag import apriltag
import srt
import re

FIDUCIAL_TYPE = 0  # 0 ARUCO 1 APRIL
STEP = 1
START_H = 13.0
BASE_VIDEO_PATH = "/mnt/d/workspace/Personale/Tesi/Video Drone/Aruco/Raw/DJI_0005"
DEST_FOLDER = "framesRect/"



subtitles = []

class ascdescperiod:
    def __init__(self, start, end, h, speed, asc):
        self.start = start
        self.end = end
        self.h = h
        self.speed = speed
        self.asc = asc


def findArucoMarkers(img, h, frameNo):
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
    tagFamily = "Aruco_original"
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict2, parameters=arucoParam)
        tagFamily = "Aruco_Dict_4X4"
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict3, parameters=arucoParam)
        tagFamily = "Aruco_Dict_5X5"
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict4, parameters=arucoParam)
        tagFamily = "Aruco_Dict_6X6"
    if ids is None:
        bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict5, parameters=arucoParam)
        tagFamily = "Aruco_Dict_7X7"
    if ids is None:
        tagFamily = "Aruco_none"
    cv2.putText(img, "{:.2f}".format(h)+"m", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 10, cv2.LINE_AA)
    if ids is not None and 1 in ids:
        cv2.putText(img, 'FOUND', (30, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 255, 0), 10, cv2.LINE_AA)
    logFrame(frameNo, h, ids, tagFamily)
    return aruco.drawDetectedMarkers(img.copy(), bboxs, ids)

def findAprilMarker(img, h, frameNo):
    tagFamily = "tag16h5"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = apriltag(tagFamily)
    results = detector.detect(gray)
    if not any(r['id'] == 1 for r in results):
        tagFamily = "tag36h11"
        detector = apriltag(tagFamily)
        results = detector.detect(gray)
        if not any(r['id'] == 1 for r in results):
            tagFamily = "tagCircle21h7"
            detector = apriltag(tagFamily)
            results = detector.detect(gray)
            if not any(r['id'] == 1 for r in results):
                tagFamily = "tagStandard41h12"
                detector = apriltag(tagFamily)
                results = detector.detect(gray)
    for r in results:
        if r['id'] == 1:
            (ptA, ptB, ptC, ptD) = r['lb-rb-rt-lt']
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
            cv2.line(image, ptA, ptB, (0, 255, 0), 2)
            cv2.line(image, ptB, ptC, (0, 255, 0), 2)
            cv2.line(image, ptC, ptD, (0, 255, 0), 2)
            cv2.line(image, ptD, ptA, (0, 255, 0), 2)
            (cX, cY) = (int(r['center'][0]), int(r['center'][1]))
            cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
            cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(img, 'FOUND', (30, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 255, 0), 10, cv2.LINE_AA)
    cv2.putText(img, "{:.2f}".format(h)+"m", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 10, cv2.LINE_AA)
    ids = [r['id'] for r in results]
    logFrame(frameNo, h, ids, "april_" + tagFamily)
    return image

def initSrt():
    global subtitles
    srt_file_text = open(BASE_VIDEO_PATH+".SRT", 'r').read()
    subtitle_generator = srt.parse(srt_file_text)
    subtitles = list(subtitle_generator)

def calculateHeight(frameNo):
    regex = "(?<=\[altitude\:\ )(.*)(?=\])"
    result = re.search(regex, subtitles[frameNo].content)
    return float(result.group(1)) - START_H

def logFrame(frameNo, h, ids, tagFamily):
    logFile = open(DEST_FOLDER+"/log.csv", "a+")
    if ids is not None:
        idsStr = ",".join([str(element) for element in ids])
    else:
        idsStr = ""
    line = str(frameNo)+";"+ idsStr + ";" + str(h) + ";" + tagFamily + "\n"
    logFile.write(line)
    logFile.close()

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
    recImg = findArucoMarkers(image, h, count+9021) if FIDUCIAL_TYPE == 0 else findAprilMarker(image, h, count+9021)
    cv2.imwrite(DEST_FOLDER+"frame%d.jpg" % (count+9021), recImg)
    count += STEP
    print("{:.2f}".format(count / length * 100) + "%]")
