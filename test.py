import cv2
import numpy as np
import math
import time
from cvzone.ClassificationModule import Classifier
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier=Classifier('model/keras_model.h5','model/labels.txt')
offset = 20
imgsize = 300

folder= "Data/C"
counter=0
labels=['a','b','SWAG']
while True:
    success, img = cap.read()
    imgOutput= img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0
        ]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgsize, imgsize, 3), np.uint8) * 255

        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape

        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgsize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgsize))
            imgResizeShape = imgResize.shape
            wGap= math.ceil((imgsize -wCal)/2)
            imgWhite[:,wGap:wCal+wGap]= imgResize
            prediction, index=classifier.getPrediction(imgWhite)
            print(prediction,index)

        else:
            k = imgsize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgsize,hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgsize - hCal) / 2)
            imgWhite[hGap:hCal + hGap,:] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)
        cv2.putText(imgOutput,labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("imgwhite", imgWhite)
    cv2.imshow("imgae", imgOutput)
    cv2.waitKey(1)


