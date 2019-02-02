import functions
import yolopy
import cv2
import speech

labelsPath = "yolo/coco.names"
weightsPath = "yolo/yolov3.weights"
configPath = "yolo/yolov3.cfg"
args = {"threshold":0.3, "confidence":0.5}

cam = cv2.VideoCapture(1)
engine = speech.speech_to_text()
model = yolopy.yolo(labelsPath, weightsPath, configPath)

while True:
    ret, frame = cam.read()
    label = model.detectAndPrint(frame, args)
    print(label)
    lbldict = {}
    for i in label:
        if i in lbldict:
            lbldict[i] += 1
        else:
            lbldict[i] = 1
    once = True
    length = len(lbldict)
    r = 0
    for i,j in lbldict.items():
        if once:
            if j!= 1:
                engine.text_speech("There are")
            else:
                engine.text_speech("There is")
            once = False
        engine.text_speech("{} {}".format(j, i))
        r+=1
        if r!=length:
            engine.text_speech("and")
