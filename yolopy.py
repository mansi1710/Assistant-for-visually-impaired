import cv2
import time
import numpy as np

class yolo:
    def __init__(self,labelsPath, weightsPath, configPath):
        # load the COCO class labels our YOLO model was trained on
        self.LABELS = open(labelsPath).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
                                   dtype="uint8")
        # derive the paths to the YOLO weights and model configuration
        # load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] loading YOLO from disk...")
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        # determine only the *output* layer names that we need from YOLO
        ln = self.net.getLayerNames()
        self.ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]


    def detectYolo(self,frame,args):
        (H, W) = frame.shape[:2]
        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))
        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > args["confidence"]:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxesg
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                                args["threshold"])

        return idxs, boxes, classIDs, confidences


    def detectAndShow(self, frame, args):
        idxs, boxes, classIDs, confidences = self.detectYolo(frame, args)
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

        # show the output image
        cv2.imshow("Image", frame)
        cv2.waitKey(1000)

    def detectAndPrint(self, frame, args):
        idxs, boxes, classIDs, confidences = self.detectYolo(frame, args)
        lbl = []

        if len(idxs)>0:
            for i,num in enumerate(classIDs):
                text = "{}".format(self.LABELS[num])
                lbl.append(text)
        return lbl