from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'

image = cv2.imread("bank.jpg", 1)
cv2.imshow('image', image)
cv2.waitKey()

text = pytesseract.image_to_string(image)
text = text.replace('\n',' ')
#print(text)
text2 = ""
dot = 0
text_str=[];
for i in range(len(text)):
    if (text[i] != ' '):
        text2 += text[i];
        dot = 0
    elif (text[i] == ' '):
        if (dot == 0):
            text2 += text[i]
            dot = dot + 1
        elif(dot == 1):
            text_str.append(text2)
            text2 = ""
            dot = dot+ 1
engine = pyttsx3.init();
for i, j in enumerate(text_str):
    if(i == 0):
        engine.say("The form is titled as:")
        engine.runAndWait();
        engine.say(j);
        engine.runAndWait();
        engine.say("Enter Yes if you want further details")
        engine.runAndWait()
        c = input()
        if (c != 'Y'):
            break
    print(j);
    if(j=="Official Use" or j =="For Official Purposes"):
        break;
    if(i!=0):
        engine.say(j);
        engine.runAndWait();


