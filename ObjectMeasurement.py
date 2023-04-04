import cv2
import numpy as np
import utils

webcam = False
image_path = './assets/image.jpg'
# Webcam capture settings
capture = cv2.VideoCapture(0)
# brightness
capture.set(10, 160)
# width
capture.set(3, 1920)
# height
capture.set(4, 1080)

torun = True;
while torun:
    if webcam:
        success, image = capture.read()
    else:
        image = cv2.imread(image_path)

    image, contours = utils.getCountours(image, minArea=90000, filter=4, draw=True)
    if len(contours) != 0:
        biggest = contours[0][2]
        print(biggest)

    image = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam Source', image)

    key = cv2.waitKey(1)
    # Press Q on keyboard to exit
    if key & 0xFF == ord('q'):
        break
