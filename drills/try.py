from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'

image = cv2.imread('test_form.jpg', 1)
cv2.imshow('image', image)
cv2.waitKey()

text = pytesseract.image_to_string(image)
print(text)