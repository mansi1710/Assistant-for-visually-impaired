import functions
import yolopy
import cv2


labelsPath = "yolo/coco.names"
weightsPath = "yolo/yolov3.weights"
configPath = "yolo/yolov3.cfg"
args = {"threshold":0.3, "confidence":0.5}

cam = cv2.VideoCapture(1)

model = yolopy.yolo(labelsPath, weightsPath, configPath)

while True:
    ret, frame = cam.read()
    print(model.detectAndPrint(frame, args))
