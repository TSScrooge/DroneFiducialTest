import cv2

FRAME = 745
BASE_VIDEO_PATH = "D:\workspace\Personale\Tesi\Video Drone\Aruco\Raw\DJI_0008"

vidcap = cv2.VideoCapture(BASE_VIDEO_PATH+".MP4")
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(length)
vidcap.set(1, FRAME)
success, image = vidcap.read()
cv2.imwrite("frameAprilSingle/frame%d.jpg" % FRAME, image)