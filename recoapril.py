# USAGE
# python detect_apriltag.py --image images/example_01.png

# import the necessary packages
from apriltag import apriltag
import argparse
import cv2

ID = 1
FRAME = 745

tagFamily = "tag1g6h5"
# load the input image and convert it to grayscale
print("[INFO] loading image...")
image = cv2.imread("frameAprilSingle/frame%d.jpg" % FRAME)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# define the AprilTags detector options and then detect the AprilTags
# in the input image
print("[INFO] detecting AprilTags...")
detector = apriltag(tagFamily)
results = detector.detect(gray)
print("[INFO] {} total AprilTags detected".format(len(results)))
if len(results) == 0:
	exit()
print(results)

for r in results:
	if r['id'] == ID:
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
		print("[INFO] tag family: {}".format(tagFamily))
if not any(r['id'] == 1 for r in results):
	cv2.putText(image, 'FOUND', (30, 2160 - 30), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 255, 0), 10, cv2.LINE_AA)

cv2.imwrite("frameAprilSingle/frame%d_detected.jpg" % FRAME, image)