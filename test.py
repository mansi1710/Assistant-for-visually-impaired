import cv2 as cv


cam = cv.VideoCapture(3)

while(True):
    ret, frame = cam.read()
    cv.imshow('Test', frame)
    cv.waitKey(5)